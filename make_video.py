"""Render one outline Markdown file -> MP4 video.

Pipeline:
    Markdown -> sections -> slide PNGs (Pillow) -> per-slide TTS audio ->
    ffmpeg mux per slide -> concat list -> chaptered MP4.

Inputs come exclusively from user-authored Markdown under content/.
Never reads .source_html/ or .parsed/ — those caches belong to a deprecated
verbatim scraper; this script is strictly original-content.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import textwrap
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
CONTENT_DIR = ROOT / "content"
VLOG_DIR = ROOT / "videos"
WORK_DIR = ROOT / "work"

SLIDE_W, SLIDE_H = 1280, 720
FPS = 30
BG = (16, 22, 36)
FG = (240, 244, 252)
ACCENT = (99, 162, 255)
MUTED = (148, 163, 184)


@dataclass
class Slide:
    kind: str  # title | section | takeaway | closing
    title: str
    body: str = ""
    lines: list[str] = field(default_factory=list)


@dataclass
class Outline:
    track: str
    module: str
    title: str
    summary: str
    slides: list[Slide]


# ----------------------------- markdown parsing ---------------------------- #


def slugify(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s+", "-", s).strip("-")
    return s or "module"


def parse_outline(md_path: Path, track: str) -> Outline:
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    title = lines[0].lstrip("# ").strip() if lines and lines[0].startswith("#") else md_path.stem

    summary = ""
    sections: list[tuple[str, list[str]]] = []
    cur_title = None
    cur_body: list[str] = []

    for raw in lines[1:]:
        line = raw.rstrip()
        if line.startswith("## "):
            if cur_title is not None:
                sections.append((cur_title, cur_body))
            cur_title = line[3:].strip()
            cur_body = []
        elif cur_title is not None:
            cur_body.append(line)
        elif line.strip() and not summary:
            summary = line.strip()

    if cur_title is not None:
        sections.append((cur_title, cur_body))

    slides: list[Slide] = [Slide(kind="title", title=title, body=summary)]
    for st, body in sections:
        body_text = "\n".join(body).strip()
        bullets: list[str] = []
        para = ""
        for ln in body:
            ln = ln.strip()
            if ln.startswith(("- ", "* ")):
                bullets.append(ln[2:])
            elif ln:
                para = (para + " " + ln).strip()
        if para:
            slides.append(Slide(kind="section", title=st, body=para))
        if bullets:
            slides.append(Slide(kind="section", title=st, lines=bullets))

    if not sections:
        slides.append(Slide(kind="takeaway", title="Key takeaways", body="No sections provided."))
    else:
        takeaways = []
        for _, body in sections:
            for ln in body:
                ln = ln.strip()
                if ln.startswith(("- ", "* ")):
                    item = ln[2:].strip()
                    if item and item not in takeaways and len(takeaways) < 6:
                        takeaways.append(item)
        slides.append(Slide(kind="takeaway", title="Key takeaways", lines=takeaways or ["Review the outline Markdown."]))
    slides.append(Slide(kind="closing", title="End of module"))
    # attribution slide (required for MIT-licensed source; see NOTICE)
    slides.append(
        Slide(
            kind="closing",
            title="Source & license",
            body=(
                "Source: anthropic-partners.skilljar.com\n"
                "Course released by Anthropic PBC under the MIT License.\n"
                "This video is generated locally from public catalog seeds.\n"
                "See NOTICE in the repository for the full attribution block."
            ),
        )
    )

    return Outline(track=track, module=md_path.stem, title=title, summary=summary, slides=slides)


# ----------------------------- slide rendering ---------------------------- #


def _load_font(size: int) -> ImageFont.FreeTypeFont:
    candidates = [
        r"C:\Windows\Fonts\segoeuib.ttf",
        r"C:\Windows\Fonts\segoeui.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/Library/Fonts/Arial.ttf",
    ]
    for c in candidates:
        if Path(c).exists():
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                pass
    return ImageFont.load_default()


def _wrap(text: str, font: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
    out: list[str] = []
    for paragraph in text.split("\n"):
        if not paragraph:
            out.append("")
            continue
        # soft-wrap by word
        words = paragraph.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            bbox = font.getbbox(trial)
            if bbox[2] - bbox[0] <= max_w:
                cur = trial
            else:
                if cur:
                    out.append(cur)
                cur = w
        if cur:
            out.append(cur)
    return out


def render_slide(slide: Slide, out_png: Path) -> None:
    img = Image.new("RGB", (SLIDE_W, SLIDE_H), BG)
    d = ImageDraw.Draw(img)

    # subtle top accent bar
    d.rectangle((0, 0, SLIDE_W, 8), fill=ACCENT)

    title_font = _load_font(54)
    body_font = _load_font(30)
    small_font = _load_font(22)

    if slide.kind == "title":
        d.text((80, 200), slide.title, font=title_font, fill=FG)
        if slide.body:
            wrap = _wrap(slide.body, body_font, SLIDE_W - 160)
            y = 320
            for ln in wrap[:6]:
                d.text((80, y), ln, font=body_font, fill=MUTED)
                y += 44
    elif slide.kind == "closing":
        d.text((80, 320), slide.title, font=title_font, fill=FG)
        d.text((80, 420), "Practice, then move to the next module.", font=body_font, fill=MUTED)
    else:
        d.text((80, 70), slide.title, font=title_font, fill=FG)
        # divider
        d.rectangle((80, 150, SLIDE_W - 80, 152), fill=ACCENT)
        y = 180
        if slide.body:
            wrap = _wrap(slide.body, body_font, SLIDE_W - 160)
            for ln in wrap[:7]:
                d.text((80, y), ln, font=body_font, fill=FG)
                y += 40
        if slide.lines:
            for item in slide.lines[:8]:
                d.ellipse((90, y + 8, 108, y + 26), fill=ACCENT)
                wrap = _wrap(("• " + item), body_font, SLIDE_W - 180)
                for j, ln in enumerate(wrap[:3]):
                    d.text((120, y + (j * 40)), ln, font=body_font, fill=FG)
                y += max(40, len(wrap[:3]) * 40)
        if slide.kind == "takeaway":
            d.text((80, SLIDE_H - 60), "Recap", font=small_font, fill=MUTED)

    out_png.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_png, "PNG", optimize=True)


# ----------------------------- TTS ----------------------------------------- #


def synth_with_edge_tts(text: str, wav_path: Path) -> bool:
    """Use edge-tts (high quality, requires network). Returns True on success."""
    try:
        import asyncio
        import edge_tts  # type: ignore
    except Exception:
        return False
    voice = os.environ.get("CLAUDE_TTS_VOICE", "en-US-AriaNeural")
    async def _run():
        comm = edge_tts.Communicate(text, voice=voice)
        await comm.save(str(wav_path))
    try:
        asyncio.run(_run())
        return wav_path.exists() and wav_path.stat().st_size > 0
    except Exception as e:
        print(f"[edge-tts] failed: {e}", file=sys.stderr)
        return False


def synth_with_sapi(text: str, wav_path: Path) -> bool:
    """Use Windows SAPI5 via PowerShell. Offline, decent quality."""
    if os.name != "nt":
        return False
    ps = (
        "Add-Type -AssemblyName System.Speech;"
        "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer;"
        "$s.SetOutputToWaveFile('" + str(wav_path).replace("'", "''") + "');"
        "$s.Speak([System.Text.RegularExpressions.Regex]::Replace("
        "@'\n" + text.replace("@", "@`u0040") + "\n'@, '\\s+', ' '));"
    )
    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps],
            check=True, capture_output=True,
        )
        return wav_path.exists() and wav_path.stat().st_size > 0
    except Exception as e:
        print(f"[SAPI] failed: {e}", file=sys.stderr)
        return False


def synth(text: str, wav_path: Path) -> float:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        text = "."
    if synth_with_edge_tts(text, wav_path):
        return wav_path.stat().st_size / 32000.0
    if synth_with_sapi(text, wav_path):
        return wav_path.stat().st_size / 32000.0
    raise RuntimeError("No TTS backend available (install edge-tts OR run on Windows for SAPI5)")


# ----------------------------- ffmpeg mux --------------------------------- #


def mux_clip(slide_png: Path, audio_wav: Path, out_mp4: Path, hold_seconds: float = 1.5) -> None:
    """Create a per-slide MP4 clip from one still image and one audio file."""
    out_mp4.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-loop", "1", "-t", f"{max(hold_seconds, 0.1):.2f}",
        "-i", str(slide_png),
        "-i", str(audio_wav),
        "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
        "-r", str(FPS),
        "-c:a", "aac", "-b:a", "128k",
        "-shortest",
        str(out_mp4),
    ]
    subprocess.run(cmd, check=True)


def concat(clips: list[Path], out_mp4: Path, chapters: list[tuple[float, str]]) -> None:
    list_file = out_mp4.with_suffix(".concat.txt")
    list_file.write_text(
        "\n".join(f"file '{p.resolve().as_posix()}'" for p in clips),
        encoding="utf-8",
    )
    chapters_file = out_mp4.with_suffix(".chapters.txt")
    if chapters:
        total_end = int(sum(float(d) for _, _, _ in []) * 0)  # placeholder, recomputed below
        # Compute total duration from clip durations (sum of file durations via ffprobe is heavy);
        # here we derive it from clip timestamps explicitly passed in. Caller passes
        # (start, title) timestamps; we approximate END by adding a small tail window.
        lines = [";FFMETADATA1"]
        for i, (t, name) in enumerate(chapters):
            start = int(t * 1000)
            if i + 1 < len(chapters):
                end = int(chapters[i + 1][0] * 1000)
            else:
                end = start + 60_000  # 60s tail window for the final chapter
            lines += [
                "[CHAPTER]",
                "TIMEBASE=1/1000",
                f"START={start}",
                f"END={end}",
                f"TITLE={name}",
            ]
        chapters_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
        chapters_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", str(list_file),
    ]
    if chapters:
        cmd += ["-i", str(chapters_file), "-map_metadata", "1"]
    cmd += ["-c", "copy", "-movflags", "+faststart", str(out_mp4)]
    subprocess.run(cmd, check=True)


# ----------------------------- orchestrator ----------------------------- #


def render_outline(track: str, md_path: Path) -> Path:
    outline = parse_outline(md_path, track)
    work = WORK_DIR / track / outline.module
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    clips: list[Path] = []
    timestamps: list[float] = []
    cursor = 0.0
    transcript: list[tuple[float, float, str]] = []

    for i, slide in enumerate(outline.slides):
        slide_png = work / f"slide_{i:02d}.png"
        render_slide(slide, slide_png)

        narration = slide.body if slide.body else (slide.title + ("; " + "; ".join(slide.lines) if slide.lines else ""))
        if not narration.strip():
            narration = slide.title + "."
        audio_wav = work / f"slide_{i:02d}.wav"
        try:
            dur = synth(narration, audio_wav)
        except RuntimeError:
            dur = max(2.0, len(narration.split()) / 2.6)

        clip = work / f"clip_{i:02d}.mp4"
        hold = dur + 1.0
        mux_clip(slide_png, audio_wav, clip, hold_seconds=hold)
        clips.append(clip)
        timestamps.append(cursor)
        transcript.append((cursor, cursor + dur, narration))
        cursor += hold

    chapters = [(t, s.title) for t, s in zip(timestamps, outline.slides)]

    out_dir = VLOG_DIR / track
    out_dir.mkdir(parents=True, exist_ok=True)
    out_mp4 = out_dir / f"{outline.module}.mp4"
    concat(clips, out_mp4, chapters)

    # write SRT transcript
    def fmt(t: float) -> str:
        ms = int(t * 1000)
        h, ms = divmod(ms, 3_600_000)
        m, ms = divmod(ms, 60_000)
        s, ms = divmod(ms, 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    srt = out_mp4.with_suffix(".srt")
    with srt.open("w", encoding="utf-8") as f:
        for i, (start, end, txt) in enumerate(transcript, 1):
            f.write(f"{i}\n{fmt(start)} --> {fmt(end)}\n{txt.strip()}\n\n")

    # write a small meta json
    meta = {
        "track": track,
        "module": outline.module,
        "title": outline.title,
        "slides": len(outline.slides),
        "duration_sec": round(cursor, 2),
        "mp4": str(out_mp4.relative_to(ROOT)),
        "srt": str(srt.relative_to(ROOT)),
    }
    (out_mp4.with_suffix(".meta.json")).write_text(json.dumps(meta, indent=2), encoding="utf-8")

    print(f"[ok] {out_mp4.relative_to(ROOT)}  ({cursor:.1f}s, {len(outline.slides)} slides)")
    return out_mp4


def main() -> None:
    ap = argparse.ArgumentParser(description="Render a Markdown outline to MP4.")
    ap.add_argument("track", help="track folder under content/, e.g. 'associate'")
    ap.add_argument("module", help="module markdown filename (without .md) or full path")
    args = ap.parse_args()

    md_path = Path(args.module)
    if not md_path.is_absolute():
        md_path = CONTENT_DIR / args.track / (args.module if md_path.suffix == ".md" else f"{args.module}.md")
    if not md_path.exists():
        sys.exit(f"missing: {md_path}")
    render_outline(args.track, md_path)


if __name__ == "__main__":
    main()
