# claude-cert-videos

Generate **original** narrated study videos, interactive flashcards, and
quizzes covering four Claude certification tracks:

- **Associate** — operating Claude for everyday work
- **Developer** — building production-grade Claude systems
- **Architect Foundations** — and the prelude to architect-level work
- **Architect Professional** — design, integration, governance, lifecycle

The pipeline is **not** a verbatim re-narrator of Skilljar courses. Every
slide, narration line, caption, flashcard, and quiz question comes from the
Markdown outlines in this repo, written in plain language from generic
knowledge of Claude. See `LEGAL.md` for the full legal posture.

## Prerequisites

- Python 3.11+
- `ffmpeg` on PATH (`ffmpeg -version` should print a version 6.0+)
- `pip install -r requirements.txt`  → installs Pillow and edge-tts
- An internet connection **only** if you want edge-tts (high-quality neural
  voices). Without it, the script falls back to Windows SAPI5 (offline).

## One-shot build (recommended)

```bash
python build_all.py --force
```

This walks every track under `content/`, renders MP4s, writes flashcards,
writes quizzes, and rebuilds the per-track interactive index pages.

## Build a single track or module

```bash
python make_video.py        associate        1-platform-foundations
python make_flashcards.py   associate        1-platform-foundations
python make_quiz.py         associate        1-platform-foundations
python make_interactive.py  associate        --title "..."   --summary "..."
```

## TTS engines

- `edge-tts` (recommended) — high-quality neural voice, requires internet:
  `set CLAUDE_TTS_VOICE=en-US-AriaNeural` to override voice.
- Windows SAPI5 (offline fallback) — used automatically when edge-tts is not
  installed. Install with `pip install pywin32` for better reliability, but
  the basic fallback works without extra deps.

## Output layout

```
content/<track>/<module>.md       ← your outline (source of truth)
videos/<track>/<module>.mp4       ← rendered MP4
videos/<track>/<module>.srt       ← captions (1 entry per slide)
videos/<track>/<module>.meta.json ← build metadata
flashcards/<track>/<module>.html  ← self-contained flashcard deck
quizzes/<track>/<module>.html     ← self-contained MCQ quiz
interactive/<track>/index.html    ← course shell with video + flashcards + quiz
work/<track>/<module>/             ← intermediates (PNG slides, WAV, clips)
publish/<track>/upload.json       ← upload manifest (YouTube / Udemy / GH)
publish/<track>/titles.tsv
publish/<track>/README.md         ← per-track upload instructions
```

## Publishing

The pipeline **never pushes or uploads** anything. It only writes local
artifacts and prints dry-run commands. To publish:

1. Open `publish/<track>/README.md` and follow its checklist.
2. For YouTube: paste title, description, and tags from `titles.tsv`.
3. For Udemy: copy `upload.json` descriptions into your course's lectures.
4. For GitHub: review `git status`, then `git push` yourself. The repo's
   `.gitignore` keeps `work/`, `__pycache__/`, and the legacy `.source_html/`,
   `.parsed/`, `.cache_*.json` out of the commit by default.

## Extending the library

Drop a new Markdown file into `content/<track>/`, then run
`python build_all.py --track <track>`. The outline supports:

- `# Title` — module title
- `## Section heading` — top-level slide group; everything before the next
  `##` is the section's body
- `- bullet` lines — rendered as one bullet point per line

For inline multiple choice, drop `Q:`, `A:`, and `C:` markers into the
Markdown and the quiz generator picks them up automatically. See
`make_quiz.py` for the exact grammar.

## Pinned dependency comments

- `Pillow>=10.0` — slide rendering.
- `edge-tts>=6.1` — high-quality neural TTS (optional).
- `ffmpeg` — external binary; verify with `ffmpeg -version`.
