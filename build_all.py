"""Build everything: generate variants per module then render MP4 + flashcards + quiz.

Per (track, module, variant_seed):
  1. write content/<track>/v<seed>-<slug>.md via make_outline.py
  2. render MP4 + sidecars via make_video.py
  3. write flashcards/<track>/v<seed>-<slug>.html via make_flashcards.py
  4. write quizzes/<track>/v<seed>-<slug>.html   via make_quiz.py

After each track, write interactive/<track>/index.html via make_interactive.py.

Output is byte-deterministic given (track, slug, seed). By default already-fresh
outputs are skipped (resume-friendly); use --force to re-render everything.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import make_outline  # noqa: E402
from make_video import render_outline  # noqa: E402
from make_flashcards import write_deck  # noqa: E402
from make_quiz import write_quiz  # noqa: E402
from make_interactive import build_track  # noqa: E402

TRACKS = {
    "associate": {
        "title": "Claude Certified Associate — original study path",
        "summary": (
            "An original study path covering the broad topics a Claude associate "
            "should know: how Claude works, how to prompt it well, how teams use it "
            "in real workflows, how to validate output, and how to set up "
            "configuration and governance. Each module ships in multiple variants "
            "so you can return to a fresh take instead of memorising a single one."
        ),
    },
    "developer": {
        "title": "Claude Certified Developer — original study path",
        "summary": (
            "An original developer-focused study path: Claude API fundamentals, "
            "production-grade prompting and tool use, the Claude Code workflow and "
            "MCP integrations, evaluation and security practices, and packaging "
            "builds for reuse."
        ),
    },
    "architect-foundations": {
        "title": "Claude Certified Architect (Foundations) — original study path",
        "summary": (
            "An original foundations-level study path for architects: AI fluency, "
            "building with the Claude API, hosting on major clouds, agentic "
            "Claude Code workflows, the Model Context Protocol, and a broad "
            "introduction to operating Claude responsibly at scale."
        ),
    },
    "architect-professional": {
        "title": "Claude Certified Architect (Professional) — original study path",
        "summary": (
            "An original professional-level study path: solution design, "
            "enterprise integration and production hardening, responsible AI "
            "safety and risk architecture, stakeholder engagement and lifecycle, "
            "and team enablement."
        ),
    },
}


def _is_fresh(md: Path) -> bool:
    """True if the mp4 + flashcards + quiz for this md already exist and are newer than it."""
    rel = md.relative_to(ROOT / "content")
    track = rel.parts[0]
    stem = md.stem
    outputs = [
        ROOT / "videos" / track / f"{stem}.mp4",
        ROOT / "flashcards" / track / f"{stem}.html",
        ROOT / "quizzes" / track / f"{stem}.html",
    ]
    if not all(p.exists() for p in outputs):
        return False
    src_mtime = md.stat().st_mtime
    return all(p.stat().st_mtime >= src_mtime for p in outputs)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--track", help="only build one track (default: all)")
    ap.add_argument("--variants", type=int, default=5, help="variants per module")
    ap.add_argument("--seed-offset", type=int, default=0)
    ap.add_argument("--regen-md", action="store_true",
                    help="rewrite the .md files even if they exist on disk")
    ap.add_argument("--skip-video", action="store_true")
    ap.add_argument("--force", action="store_true",
                    help="re-render even when outputs are fresh (default: resume/skip)")
    args = ap.parse_args()

    seeds = json.loads((ROOT / "seeds" / "seeds.json").read_text(encoding="utf-8"))

    targets = {args.track: TRACKS[args.track]} if args.track else TRACKS
    for track, meta in targets.items():
        track_seed = seeds["tracks"][track]
        modules = track_seed["modules"]
        folder = ROOT / "content" / track
        folder.mkdir(parents=True, exist_ok=True)

        print(f"\n=== {track} ({len(modules)} modules × {args.variants} variants = {len(modules) * args.variants} outcomes) ===")
        for m in modules:
            for v in range(args.variants):
                seed = v + args.seed_offset
                md = folder / f"v{seed:03d}-{m['slug']}.md"
                if args.regen_md or not md.exists():
                    md.write_text(make_outline.generate_outline(track, m, seed), encoding="utf-8")
                if not args.force and _is_fresh(md):
                    print(f"[cached] {track}/v{seed:03d}-{m['slug']}")
                    continue
                try:
                    if not args.skip_video:
                        render_outline(track, md)
                    write_deck(track, md)
                    write_quiz(track, md)
                    print(f"[ok] {track}/v{seed:03d}-{m['slug']}")
                except Exception as e:
                    print(f"[error] {track}/v{seed:03d}-{m['slug']}: {e}", file=sys.stderr)
        build_track(track, meta["title"], meta["summary"])


if __name__ == "__main__":
    main()
