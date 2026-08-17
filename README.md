# claude-cert-videos

Turns the **Claude Certified Developer — Foundations** course modules (hosted on
Skilljar) into small, chaptered, narrated MP4 videos you can watch instead of
reading the written lessons.

Each course module is a single interactive SCORM app. This repo extracts the
teaching text from every screen, narrates it with neural text-to-speech, renders
matching slides, and muxes everything into one MP4 per course — with **embedded
chapter markers** (visible in VLC and most players) so you can jump section to
section.

## Layout

```
text/                 one JSON per course: {title, slug, voice, slides:[{chapter,heading,body}]}
videos/               generated <slug>.mp4 + <slug>.chapters.txt   (committed, small)
work/                 scratch: per-slide PNG/MP3/segment files      (gitignored)
make_video.py         text JSON -> narrated MP4 with chapters
build_course_json.py  raw extracted screens -> course JSON
```

## The five modules

1. `mso-foundations` — MSO Foundations
2. `production-grade-prompting-agents-tool-use` — Production-Grade Prompting, Agents & Tool Use
3. `claude-code-mcp-integration` — Claude Code, MCP & Integration
4. `production-engineering-evals-security` — Production Engineering, Evals & Security
5. `accelerators-ip-contribution` — Accelerators & IP Contribution

## Generate

```bash
pip install edge-tts pillow          # ffmpeg must be on PATH
python make_video.py text/mso-foundations.json
# -> videos/mso-foundations.mp4  (+ .chapters.txt)
```

Regenerate all:

```bash
for j in text/*.json; do python make_video.py "$j"; done
```

## Encoding — small on purpose

Slides are static, so the file is dominated by the speech track. Settings keep
each MP4 well under Git's limits (no LFS needed):

- 960×540, H.264, CRF 32, `-tune stillimage`, 5 fps
- mono AAC @ 48 kbit/s
- `+faststart` for instant web playback

## Notes

Content is © Anthropic, reproduced here only as a personal
study-by-video aid for the author's own enrolled course.
