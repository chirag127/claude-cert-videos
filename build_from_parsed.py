#!/usr/bin/env python3
"""
Convert a parsed module (.parsed/mN.json from parse_module.py) into the
make_video.py course JSON (text/<slug>.json), assembling COMPLETE slides in
screen order: teaching prose + every tab (label+panel) + every MCQ (question,
options, correct answer, feedback) + glossary.

Usage: python build_from_parsed.py .parsed/m3.json <slug> "<Title>" <module_no>
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def clean_text(t):
    """Fix mojibake, strip residual HTML, normalize whitespace/punctuation for TTS."""
    if not t:
        return ""
    # repair common UTF-8-decoded-as-latin1 mojibake
    if "�" in t or "Ã" in t or "â€" in t:
        try:
            t = t.encode("latin-1", "ignore").decode("utf-8", "ignore")
        except Exception:
            pass
    # strip any leftover HTML tags
    t = re.sub(r"<[^>]+>", " ", t)
    # normalize smart punctuation to ASCII (cleaner narration)
    t = (t.replace("’", "'").replace("‘", "'")
          .replace("“", '"').replace("”", '"')
          .replace("—", " - ").replace("–", "-")
          .replace("…", "...").replace("·", ". ")
          .replace("�", ""))
    t = re.sub(r"\s+", " ", t).strip()
    return t


SEC_TYPES = ["Orientation", "Teaching", "Watch Out", "Checkpoint",
             "Cumulative", "Recap", "Glossary", "Module Complete"]


def split_meta(meta):
    """'TeachingPermission Modes & Human Gates 17 min' -> (type, section)."""
    meta = re.sub(r"^Module[\s-]*\w+\s*", "", meta).strip()
    meta = re.sub(r"[·∙•]?\s*\d+\s*min\s*$", "", meta).strip()
    for t in SEC_TYPES:
        if meta.startswith(t):
            return t, meta[len(t):].strip() or t
    return "", meta


def chunk(text, max_chars=900):
    """Clean, then split prose into <=max_chars sentence-grouped chunks."""
    t = clean_text(text)
    if len(t) <= max_chars:
        return [t] if t else []
    sents = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])", t)
    groups, cur = [], ""
    for s in sents:
        if cur and len(cur) + 1 + len(s) > max_chars:
            groups.append(cur)
            cur = s
        else:
            cur = (cur + " " + s).strip()
    if cur:
        groups.append(cur)
    return groups


def main():
    src, slug, title, mod = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
    data = json.loads(Path(src).read_text(encoding="utf-8"))
    screens = data["screens"]
    quiz_qs = data.get("quiz_questions", [])

    slides = []
    quiz_idx = 0
    for sc in screens:
        stype, section = split_meta(sc["meta"])
        # normalize noisy section labels
        section = re.sub(r"\bModule\s*\d+\b", "", section).strip()
        section = re.sub(r"\bDeveloper\s*Module\s*\d+\b", "", section).strip()
        if stype == "Glossary" or "Key Terms" in section:
            section = "Key Terms"
        if stype == "Recap":
            section = "Key Takeaways"
        if stype == "Module Complete" or section == "Developer Path":
            section = "Wrap-up"
        chapter = section or (stype if stype and stype != "Teaching" else title)
        heading = clean_text(sc["title"]) or section or stype
        # 1) teaching prose (joined then re-chunked so slides stay readable)
        prose = " ".join(p for p in sc["prose"] if p)
        # drop the title/meta echoes from prose start if duplicated
        parts = chunk(prose)
        for i, g in enumerate(parts, 1):
            h = heading if len(parts) == 1 else f"{heading} ({i}/{len(parts)})"
            slides.append({"chapter": chapter, "heading": h, "body": g})

        # 2) tabs
        for tb in sc.get("tabs", []):
            if not tb.get("label"):
                continue
            body = f"{tb['label']}. {tb.get('body','')}".strip()
            for i, g in enumerate(chunk(body), 1):
                slides.append({"chapter": chapter,
                               "heading": f"{section}: {tb['label']}",
                               "body": g})

        # 3) MCQ options + feedback captured on the screen (fb-style)
        if sc.get("options") or sc.get("feedback"):
            opt_txt = "  ".join(f"{o['letter']}) {o['text']}" for o in sc.get("options", []))
            fb_txt = ""
            for f in sc.get("feedback", []):
                if f["kind"] in ("correct", "pass"):
                    fb_txt = f"Correct answer. {f['text']}"
                    break
            if not fb_txt and sc.get("feedback"):
                fb_txt = sc["feedback"][0]["text"]
            body = " ".join(x for x in [
                "Checkpoint.", opt_txt and ("Options: " + opt_txt), fb_txt] if x)
            for i, g in enumerate(chunk(body), 1):
                slides.append({"chapter": chapter,
                               "heading": f"{heading} — answer" if i == 1 else f"{heading} — answer ({i})",
                               "body": g})

    # 4) standalone quiz questions ({opts,ans,rat}) — appended under a Quiz chapter
    for q in quiz_qs:
        opts = "  ".join(f"{chr(97+i)}) {o}" for i, o in enumerate(q["opts"]))
        body = f"{q['stem']} Options: {opts}. Correct answer: {q['letter']}. {q['rationale']}"
        for i, g in enumerate(chunk(body), 1):
            slides.append({"chapter": "Quiz",
                           "heading": "Quiz question" if i == 1 else f"Quiz question ({i})",
                           "body": g})

    course = {"title": title, "slug": slug, "module": mod,
              "voice": "en-US-AndrewNeural", "slides": slides}
    outp = ROOT / "text" / f"{slug}.json"
    outp.write_text(json.dumps(course, ensure_ascii=False, indent=2), encoding="utf-8")
    chapters = []
    for s in slides:
        if not chapters or chapters[-1] != s["chapter"]:
            chapters.append(s["chapter"])
    print(f"{slug}: {len(slides)} slides, {len(chapters)} chapters")
    print("  chapters:", " | ".join(chapters))


if __name__ == "__main__":
    main()
