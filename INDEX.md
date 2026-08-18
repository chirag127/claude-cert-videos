# Course index

Four tracks, 25 modules, generated in 3 variants each = **75 original study
units**. Each unit produces a video, a flashcard deck, and a quiz.

## Tracks

| Track | Modules | Variants | Total units |
|-------|--------:|---------:|------------:|
| `associate` | 8 | 3 | 24 |
| `developer` | 5 | 3 | 15 |
| `architect-foundations` | 7 | 3 | 21 |
| `architect-professional` | 5 | 3 | 15 |
| **Total** | **25** | | **75** |

## Per-track entrypoints (after build)

| Track | Course shell |
|-------|-------------|
| `associate` | `interactive/associate/index.html` |
| `developer` | `interactive/developer/index.html` |
| `architect-foundations` | `interactive/architect-foundations/index.html` |
| `architect-professional` | `interactive/architect-professional/index.html` |

## Outputs per unit

- Video:      `videos/<track>/vNNN-<slug>.mp4` (+ `.srt`, `.meta.json`, `.chapters.txt`)
- Flashcards: `flashcards/<track>/vNNN-<slug>.html`
- Quiz:       `quizzes/<track>/vNNN-<slug>.html`
- Outline:    `content/<track>/vNNN-<slug>.md`

## Build

```bash
python build_all.py --variants 3            # full build, resumes automatically
python build_all.py --track developer --variants 3
python build_all.py --variants 3 --skip-video   # HTML only, no TTS
```

Regenerate the outlines at any time:

```bash
python make_outline.py --variants 3
python make_outline.py --variants 3 --seed-offset 100   # a different phrasing set
```

See `README.md` for the full pipeline and `LEGAL.md` for attribution.
