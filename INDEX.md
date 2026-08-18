# Course index

The four tracks ship in `content/<track>/`, each module is one Markdown
outline. Videos, flashcards, quizzes, and per-track interactive pages are
generated into `videos/`, `flashcards/`, `quizzes/`, and `interactive/`.

## Tracks

| Track | Modules | Notes |
|-------|--------:|-------|
| `associate` | 7 | Operating Claude confidently |
| `developer` | 5 | Building production-grade Claude systems |
| `architect-foundations` | 6 | Architect-level foundations |
| `architect-professional` | 5 | Architect-level professional |

Module count totals 23 lessons plus an opening overview per track. Edit or
extend any Markdown file under `content/`, then run `python build_all.py
--force`.

## Per-track entrypoint

After building:

- Videos:        `videos/<track>/<slug>.mp4` and `.srt`
- Flashcards:    `flashcards/<track>/<slug>.html`
- Quizzes:       `quizzes/<track>/<slug>.html`
- Course shell:  `interactive/<track>/index.html`
- Upload meta:   `publish/<track>/upload.json` and `titles.tsv`

Open `interactive/<track>/index.html` in any browser.
