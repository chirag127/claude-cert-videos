#!/usr/bin/env python3
"""
Text -> narrated MP4 (with chapters + .srt subtitles) for the Claude Certified
Developer courses.

Input JSON (one course):
{
  "title": "Course Title",
  "slug": "course-slug",
  "voice": "en-US-AndrewNeural",
  "slides": [ {"chapter": "...", "heading": "...", "body": "..."}, ... ]
}

Output:
  videos/<slug>.mp4            narrated video, embedded chapter markers, faststart
  videos/<slug>.srt            subtitles (one cue per slide)
  videos/<slug>.chapters.txt   human-readable chapter list

Speed: all TTS is generated concurrently via the edge_tts async API (the network
round-trips are the bottleneck), then slides render and ffmpeg encodes.

Usage:  python make_video.py text/<slug>.json
"""
import asyncio
import json
import os
import subprocess
import sys
import re
from pathlib import Path

import edge_tts
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent

# 960x540 static slides -> a few MB per course at CRF 32 + mono 48k audio, so the
# MP4s commit to plain git without Git LFS.
W, H = 960, 540
MARGIN = 60
BG = (23, 23, 27)
FG = (235, 235, 240)
ACCENT = (217, 119, 87)
MUTED = (150, 150, 160)


def _find_font(names, size):
    dirs = [r"C:\Windows\Fonts",
            os.path.expanduser(r"~\AppData\Local\Microsoft\Windows\Fonts")]
    for n in names:
        for d in dirs:
            p = os.path.join(d, n)
            if os.path.exists(p):
                return ImageFont.truetype(p, size)
    return ImageFont.load_default()


FONT_H1 = _find_font(["segoeuib.ttf", "arialbd.ttf"], 38)
FONT_BODY = _find_font(["segoeui.ttf", "arial.ttf"], 25)
FONT_SMALL = _find_font(["segoeui.ttf", "arial.ttf"], 18)
FONT_MONO = _find_font(["consola.ttf", "cour.ttf"], 21)


def _wrap(text, font, max_w, draw):
    lines = []
    for para in text.split("\n"):
        if not para.strip():
            lines.append("")
            continue
        cur = ""
        for wd in para.split():
            trial = (cur + " " + wd).strip()
            if draw.textlength(trial, font=font) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
    return lines


def render_slide(idx, heading, body, course_title, out_png):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 6], fill=ACCENT)
    d.text((MARGIN, 24), course_title.upper(), font=FONT_SMALL, fill=MUTED)
    y = 62
    for ln in _wrap(heading, FONT_H1, W - 2 * MARGIN, d):
        d.text((MARGIN, y), ln, font=FONT_H1, fill=ACCENT)
        y += 46
    y += 14
    line_h = 34
    body_lines = _wrap(body, FONT_BODY, W - 2 * MARGIN, d)
    max_lines = max(1, (H - y - 44) // line_h)
    for ln in body_lines[:max_lines]:
        mono = ln.strip().startswith(("{", "}", "\"", "-", "•", "$", "npm", "git", "cmi", "Bash", "Edit", "Read"))
        d.text((MARGIN, y), ln, font=(FONT_MONO if mono else FONT_BODY),
               fill=(FG if not mono else (180, 220, 200)))
        y += line_h
    if len(body_lines) > max_lines:
        d.text((MARGIN, y), "…  (full text is narrated)", font=FONT_SMALL, fill=MUTED)
    d.text((MARGIN, H - 32), f"Screen {idx}", font=FONT_SMALL, fill=MUTED)
    img.save(out_png)


async def _tts_one(text, voice, out_mp3):
    clean = re.sub(r"\s+", " ", text).strip() or "Continue."
    comm = edge_tts.Communicate(clean, voice)
    await comm.save(str(out_mp3))


async def narrate_all(items, voice):
    # items: list of (text, out_mp3). Bounded concurrency to be kind to the endpoint.
    sem = asyncio.Semaphore(12)
    async def worker(text, out):
        async with sem:
            for attempt in range(3):
                try:
                    await _tts_one(text, voice, out)
                    return
                except Exception as e:
                    if attempt == 2:
                        raise
                    await asyncio.sleep(1.5 * (attempt + 1))
    await asyncio.gather(*(worker(t, o) for t, o in items))


def audio_duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True)
    try:
        return max(float(out.stdout.strip()), 1.0)
    except ValueError:
        return 3.0


def _ts_srt(sec):
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def _ts_hms(sec):
    m, s = divmod(int(sec), 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def _split_sentences(text):
    """Split prose into sentences without breaking on decimals/abbreviations crudely."""
    # normalize whitespace, then split on sentence-final punctuation followed by space+capital
    t = re.sub(r"\s+", " ", text).strip()
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])", t)
    return [p.strip() for p in parts if p.strip()]


def chunk_slides(slides, max_chars=900):
    """
    Split any slide whose body is longer than max_chars into several sub-slides at
    sentence boundaries, so each sub-slide has a short, readable body + short
    narration. Sub-slides keep the parent chapter and get a "(n/N)" heading.
    Boundaries are semantic (sentence ends). A single sentence longer than
    max_chars is hard-wrapped at a nearby comma/space so nothing runs away.
    """
    def _hard_wrap(sent):
        if len(sent) <= max_chars:
            return [sent]
        pieces, s = [], sent
        while len(s) > max_chars:
            # prefer breaking at the last comma/semicolon before the cap, else last space
            window = s[:max_chars]
            cut = max(window.rfind(", "), window.rfind("; "))
            if cut < max_chars * 0.5:
                cut = window.rfind(" ")
            if cut <= 0:
                cut = max_chars
            pieces.append(s[:cut + 1].strip())
            s = s[cut + 1:].strip()
        if s:
            pieces.append(s)
        return pieces

    out = []
    for s in slides:
        chapter = s.get("chapter") or s["heading"]
        heading = s["heading"]
        body = s.get("body", "").strip()
        if len(body) <= max_chars:
            out.append({"chapter": chapter, "heading": heading, "body": body})
            continue
        # expand sentences, hard-wrapping any monster sentence first
        sents = []
        for sent in _split_sentences(body):
            sents.extend(_hard_wrap(sent))
        groups, cur = [], ""
        for sent in sents:
            if cur and len(cur) + 1 + len(sent) > max_chars:
                groups.append(cur)
                cur = sent
            else:
                cur = (cur + " " + sent).strip()
        if cur:
            groups.append(cur)
        n = len(groups)
        for i, g in enumerate(groups, 1):
            h = heading if n == 1 else f"{heading}  ({i}/{n})"
            out.append({"chapter": chapter, "heading": h, "body": g})
    return out


def build(course_json):
    data = json.loads(Path(course_json).read_text(encoding="utf-8"))
    slug, title, voice = data["slug"], data["title"], data.get("voice", "en-US-AndrewNeural")
    slides = chunk_slides(data["slides"])

    wdir = ROOT / "work" / slug
    wdir.mkdir(parents=True, exist_ok=True)
    (ROOT / "videos").mkdir(exist_ok=True)

    # 1) narration text + audio paths
    narr = [(f"{s['heading']}. {s['body']}", wdir / f"audio_{i:04d}.mp3")
            for i, s in enumerate(slides, 1)]
    print(f"[{slug}] generating {len(narr)} narration clips ...", flush=True)
    asyncio.run(narrate_all(narr, voice))

    # 2) render slides + measure durations + build segments
    durations = []
    seg_files = []
    for i, s in enumerate(slides, 1):
        png = wdir / f"slide_{i:04d}.png"
        mp3 = wdir / f"audio_{i:04d}.mp3"
        seg = wdir / f"seg_{i:04d}.mp4"
        render_slide(i, s["heading"], s["body"], title, png)
        durations.append(audio_duration(mp3))
        subprocess.run([
            "ffmpeg", "-y", "-loop", "1", "-i", str(png), "-i", str(mp3),
            "-c:v", "libx264", "-preset", "medium", "-tune", "stillimage",
            "-crf", "32", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "48k", "-ac", "1", "-shortest",
            "-vf", f"scale={W}:{H}", "-r", "5", str(seg)
        ], check=True, capture_output=True)
        seg_files.append(seg)
    print(f"[{slug}] encoded {len(seg_files)} segments", flush=True)

    # 3) chapters (new chapter when the 'chapter' field changes)
    chapters = []
    t = 0.0
    cur, cur_start = None, 0.0
    for i, s in enumerate(slides):
        name = s.get("chapter") or s["heading"]
        if name != cur:
            if cur is not None:
                chapters.append((cur, cur_start, t))
            cur, cur_start = name, t
        t += durations[i]
    if cur is not None:
        chapters.append((cur, cur_start, t))

    meta = wdir / "chapters.meta"
    lines = [";FFMETADATA1", f"title={title}"]
    for name, st, en in chapters:
        lines += ["[CHAPTER]", "TIMEBASE=1/1000",
                  f"START={int(st*1000)}", f"END={int(en*1000)}", f"title={name}"]
    meta.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # 4) subtitles: cue per slide. Show the spoken body (wrapped to 2 lines);
    #    fall back to heading for slides with no body.
    srt = []
    t = 0.0
    for i, s in enumerate(slides):
        st, en = t, t + durations[i]
        t = en
        spoken = re.sub(r"\s+", " ", (s.get("body") or s["heading"])).strip()
        # wrap subtitle to <=2 lines of ~42 chars for readability
        words, line, cue_lines = spoken.split(), "", []
        for w in words:
            if len(line) + 1 + len(w) > 42:
                cue_lines.append(line)
                line = w
            else:
                line = (line + " " + w).strip()
            if len(cue_lines) == 2:
                break
        if line and len(cue_lines) < 2:
            cue_lines.append(line)
        cue = "\n".join(cue_lines[:2]) + ("…" if len(spoken) > 84 else "")
        srt.append(f"{i+1}\n{_ts_srt(st)} --> {_ts_srt(en)}\n{cue}\n")
    (ROOT / "videos" / f"{slug}.srt").write_text("\n".join(srt), encoding="utf-8")

    (ROOT / "videos" / f"{slug}.chapters.txt").write_text(
        "\n".join(f"{_ts_hms(st)}  {name}" for name, st, en in chapters) + "\n",
        encoding="utf-8")

    # 5) concat + mux chapters + faststart
    listf = wdir / "list.txt"
    listf.write_text("".join(f"file '{p.as_posix()}'\n" for p in seg_files), encoding="utf-8")
    concat_mp4 = wdir / "_concat.mp4"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listf),
                    "-c", "copy", str(concat_mp4)], check=True, capture_output=True)
    out_mp4 = ROOT / "videos" / f"{slug}.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(concat_mp4), "-i", str(meta),
                    "-map_metadata", "1", "-codec", "copy", "-movflags", "+faststart",
                    str(out_mp4)], check=True, capture_output=True)
    size_mb = out_mp4.stat().st_size / (1024 * 1024)
    print(f"[{slug}] DONE -> {out_mp4.name}  {len(chapters)} chapters  "
          f"{size_mb:.2f} MB  {_ts_hms(t)}", flush=True)
    return out_mp4


if __name__ == "__main__":
    build(sys.argv[1])
