#!/usr/bin/env python3
"""
Convert a persisted browser_evaluate tool-result (which wraps the extracted
screens JSON as {"type":"text","text":"### Result\n<json>"}) into the
make_video.py course JSON format.

Usage:
  python build_course_json.py <persisted_tool_result.json> <slug> "<Course Title>" <voice>
"""
import json, sys, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def main():
    src, slug, title, voice = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    raw = Path(src).read_text(encoding="utf-8")
    # The persisted file is a JSON array of content blocks; find the text block.
    outer = json.loads(raw)
    text = None
    if isinstance(outer, list):
        for blk in outer:
            if isinstance(blk, dict) and blk.get("type") == "text":
                text = blk["text"]
                break
    else:
        text = raw
    # strip leading "### Result\n" and anything after the JSON (e.g. "### Ran ...")
    text = text.strip()
    text = re.sub(r"^###\s*Result\s*", "", text)
    # cut off any trailing "### ..." section
    text = re.split(r"\n###\s", text)[0].strip()
    # the JSON is an object; grab from first { to matching last }
    start = text.find("{")
    if start > 0:
        text = text[start:]
    # trim to last closing brace
    end = text.rfind("}")
    if end != -1:
        text = text[:end+1]
    payload = json.loads(text)
    screens = payload["screens"]

    slides = []
    for s in screens:
        meta = s.get("meta", "")
        # meta looks like "Module 2TeachingPermission Modes & Human Gates·17 min"
        # Strip an optional leading "Module N" prefix, the leading type word,
        # and any trailing duration ("·17 min", " 7 min", "17 min").
        meta = re.sub(r"^Module[\s-]*\w+\s*", "", meta).strip()
        meta = re.sub(r"[·]?\s*\d+\s*min\s*$", "", meta).strip()
        m = re.match(r"(Orientation|Teaching|Watch Out|Checkpoint|Cumulative|Recap|Glossary|Module Complete)?(.*)$", meta)
        section = (m.group(2).strip() if m else meta).strip() or title
        slide_type = (m.group(1) or "").strip() if m else ""
        heading = s.get("title", "").strip()
        body = s.get("body", "").strip()
        # Skip pure interactive checkpoints in narration? No — user wants full teaching.
        # But checkpoints are quizzes; include a short note instead of the answer options.
        if slide_type == "Checkpoint":
            # keep the scenario prose but drop the multiple-choice noise for narration clarity
            body = body.split("Select ")[0].split("Choose ")[0].strip() or body
        slides.append({
            "chapter": f"{section}",
            "heading": heading,
            "body": body,
        })

    course = {"title": title, "slug": slug, "voice": voice, "slides": slides}
    outp = ROOT / "text" / f"{slug}.json"
    outp.write_text(json.dumps(course, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {outp}  ({len(slides)} slides)")
    # print chapter list
    seen = []
    for sl in slides:
        if sl["chapter"] not in seen:
            seen.append(sl["chapter"])
    print("chapters:", " | ".join(seen))

if __name__ == "__main__":
    main()
