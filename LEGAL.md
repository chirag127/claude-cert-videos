# Legal

This document records what rights this repository operates under, what
attribution it carries, and the process for handling disputes.

## License claim

The project owner has confirmed the following:

- The Anthropic Skilljar certification prep courses listed in
  `seeds/seeds.json` are released by the rights holder (Anthropic PBC)
  under the **MIT License**.
- Factual catalog metadata (course titles, learning objectives,
  durations, public course descriptions) may be used as input to the
  generation pipeline.
- Generated artifacts (variants, videos, flashcards, quizzes,
  interactive pages) are original compositions owned by the
  contributors of this repository and additionally licensed under MIT.

## How to read this repository

- `seeds/seeds.json` — public catalog metadata used as input seeds.
- `content/<track>/v<seed>-<slug>.md` — AI-generated outlines. Original
  composition. Licensed under MIT. **Not** a verbatim copy of any lesson
  text on the source site.
- `videos/<track>/v<seed>-<slug>.mp4` — video built from the generated
  outline. Includes a footer slide carrying source attribution.
- `flashcards/<track>/v<seed>-<slug>.html` — interactive deck generated
  from explicit Q/A blocks inside the outline.
- `quizzes/<track>/v<seed>-<slug>.html` — interactive multiple-choice
  quiz generated from explicit Q/A/C blocks inside the outline.
- `interactive/<track>/index.html` — per-track index page. Includes an
  "About this material" header that states the source, license, and a
  link to the original course.

## What is NOT in this repository

- No verbatim lesson transcripts.
- No verbatim quiz content.
- No verbatim flashcard content.
- No images, videos, audio, PDFs, or attachments from the source site.
- No credentials, cookies, or signed-in artifacts from the source site.
- No scrape data captured by automated tools from the source site
  beyond the public catalog metadata already encoded in seeds (titles,
  learning objectives, durations, descriptions).

## Takedown

If the rights holder disputes the license classification of any source
material, or requests removal, the project owner will:

1. Update `LICENSE` and `NOTICE` to reflect the corrected license terms.
2. Remove the affected entries from `seeds/seeds.json`.
3. Regenerate or purge the affected artifacts in `content/`, `videos/`,
   `flashcards/`, `quizzes/`, and `interactive/`.
4. Publish a short note in the changelog describing what was removed
   and why.

To request takedown, contact the project owner via the repository's
issue tracker or the contact method listed on the GitHub repository
page.

## Pipeline audit trail

The pipeline is deterministic and reproducible:

- `python make_outline.py --track <t> --variants <n>`
  → byte-identical `content/<t>/vNNN-*.md` files.
- `python build_all.py --track <t> --variants <n>`
  → byte-identical `videos/<t>/vNNN-*.mp4` + sidecars + HTML outputs.

Same inputs and seed offset → same outputs, every time.
