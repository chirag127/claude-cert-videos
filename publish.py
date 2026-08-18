"""Generate per-track upload manifests for YouTube and Udemy, plus a
git-publish dry-run explanation. Never actually pushes or uploads; only prints.

Outputs:
    publish/<track>/titles.tsv        title, description, tags
    publish/<track>/upload.json      module -> mp4/srt/description
    publish/<track>/README.md        copy-pasteable upload instructions
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VIDEO_DIR = ROOT / "videos"
OUT_DIR = ROOT / "publish"


def slugify(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s+", "-", s).strip("-")
    return s or "module"


def list_modules(track: str) -> list[Path]:
    folder = ROOT / "content" / track
    if not folder.exists():
        return []
    return sorted(p for p in folder.glob("*.md"))


def md_title(md: Path) -> str:
    text = md.read_text(encoding="utf-8")
    for ln in text.splitlines():
        if ln.startswith("#"):
            return ln.lstrip("# ").strip()
    return md.stem.replace("-", " ").title()


def md_intro(md: Path) -> str:
    text = md.read_text(encoding="utf-8")
    out = []
    seen = False
    for ln in text.splitlines():
        if not seen:
            if ln.startswith("#"):
                seen = True
            continue
        if ln.startswith("## "):
            break
        s = ln.strip()
        if s:
            out.append(s)
        if len(out) >= 2:
            break
    return " ".join(out) or "Original study module."


def build_manifest(track: str, track_title: str) -> dict:
    rows = []
    manifest = {
        "track": track,
        "title": track_title,
        "generated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "modules": [],
    }
    for md in list_modules(track):
        title = md_title(md)
        intro = md_intro(md)
        slug = slugify(md.stem)
        rows.append({
            "slug": slug,
            "title": f"{title} — {track_title}",
            "description": (
                f"{intro}\n\n"
                f"Originally narrated study material. Refer to the official "
                f"course for the definitive exam preparation.\n\n"
                f"Tags: claude, certification, study, {track}"
            ),
            "tags": "claude, certification, study, " + track.replace("-", " "),
            "video": f"../../videos/{track}/{slug}.mp4",
            "srt": f"../../videos/{track}/{slug}.srt",
            "flashcards": f"../../flashcards/{track}/{slug}.html",
            "quiz": f"../../quizzes/{track}/{slug}.html",
        })
    manifest["modules"] = rows

    out = OUT_DIR / track
    out.mkdir(parents=True, exist_ok=True)
    (out / "upload.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    with (out / "titles.tsv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["slug", "title", "tags", "video", "srt"])
        for r in rows:
            w.writerow([r["slug"], r["title"], r["tags"], r["video"], r["srt"]])

    readme = out / "README.md"
    readme.write_text(
        f"# Upload manifest — {track_title}\n\n"
        f"Generated: {manifest['generated']}\n\n"
        "## YouTube upload\n"
        "1. Open https://studio.youtube.com → Upload video → select videos/<track>/<slug>.mp4\n"
        "2. Title, description, and tags are in `titles.tsv` (TSV columns: slug, title, tags, ...)\n"
        "3. Upload the matching `.srt` as a caption file (auto-sync should pick it up).\n"
        "4. Set visibility to Unlisted first; switch to Public once the description and tags look right.\n\n"
        "## Udemy upload\n"
        "1. Use Udemy Business course builder. Create a section per module.\n"
        f"2. Lecture title: `${{module.title}}`. Upload videos/{track}/<slug>.mp4 as the lecture video.\n"
        f"3. Lecture description: drop in `${{module.description}}` from upload.json.\n"
        f"4. Add the matching flashcards HTML and quiz HTML as downloadable resources.\n\n"
        "## GitHub upload (the repo itself)\n"
        "This script never pushes code. Run:\n\n"
        "```bash\n"
        "git add videos/ flashcards/ quizzes/ interactive/ publish/ content/ make_*.py build_all.py requirements.txt README.md LEGAL.md INDEX.md\n"
        'git commit -m "publish: regenerate narrated study videos"\n'
        "git push origin HEAD\n"
        "```\n\n"
        "## Important\n"
        "This pipeline produces *original* study material; it does not reproduce\n"
        "official course text. Review every uploaded video for copyright and\n"
        "platform terms before publishing to a public channel.\n",
        encoding="utf-8",
    )
    print(f"[ok] publish/{track}/upload.json titles.tsv README.md")
    return manifest


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--track", help="single track, default all known")
    args = ap.parse_args()

    from build_all import TRACKS  # late import to avoid ordering issues
    targets = {args.track: TRACKS[args.track]} if args.track else TRACKS
    for track, meta in targets.items():
        build_manifest(track, meta["title"])


if __name__ == "__main__":
    main()
