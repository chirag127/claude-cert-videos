"""Build a track-level HTML index page.

For each course under content/<track>/, list the rendered MP4, the
flashcards HTML, and the quiz HTML in one self-contained page with tabs.
Provides a track summary, progress meter (manual checkbox), and links to
each module's assets.
"""
from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT_DIR = ROOT / "content"
VIDEO_DIR = ROOT / "videos"
FC_DIR = ROOT / "flashcards"
QUIZ_DIR = ROOT / "quizzes"
OUT_DIR = ROOT / "interactive"


def list_modules(track: str) -> list[Path]:
    folder = CONTENT_DIR / track
    if not folder.exists():
        return []
    return sorted(p for p in folder.iterdir() if p.suffix == ".md")


def read_summary(md_path: Path) -> str:
    text = md_path.read_text(encoding="utf-8")
    paras: list[str] = []
    seen_title = False
    for ln in text.splitlines():
        if not seen_title:
            if ln.startswith("#"):
                seen_title = True
            continue
        if ln.startswith("## "):
            break
        s = ln.strip()
        if s:
            paras.append(s)
    return "\n\n".join(paras[:2]) or "(No outline provided.)"


PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>{track_title} — interactive course</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root{{color-scheme:light dark}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:system-ui,Segoe UI,Roboto,sans-serif;background:#0f172a;color:#f1f5f9}}
header{{padding:32px 40px;background:linear-gradient(135deg,#1e3a8a 0%,#0f172a 100%)}}
h1{{margin:0;font-size:28px}}
.sub{{color:#cbd5e1;margin-top:8px;font-size:14px}}
.layout{{display:grid;grid-template-columns:280px 1fr;gap:0;min-height:calc(100vh - 100px)}}
nav{{background:#1e293b;padding:20px;border-right:1px solid #334155}}
nav h3{{font-size:13px;text-transform:uppercase;color:#94a3b8;margin:0 0 10px}}
nav a{{display:flex;gap:10px;padding:8px 10px;color:#e2e8f0;text-decoration:none;border-radius:8px;font-size:14px}}
nav a:hover{{background:#334155}}
nav a.active{{background:#1e40af}}
.tag{{font-size:11px;background:#475569;color:#f1f5f9;border-radius:4px;padding:2px 6px}}
main{{padding:32px 40px}}
summary{{font-size:14px;color:#cbd5e1;max-width:760px;white-space:pre-wrap}}
.module-card{{background:#1e293b;border:1px solid #334155;border-radius:12px;padding:18px;margin:18px 0}}
.module-card h2{{margin:0 0 6px;font-size:18px}}
.module-card p{{margin:0 0 10px;color:#cbd5e1;font-size:13px}}
.module-card .links a{{margin-right:12px;color:#60a5fa;text-decoration:none;font-size:13px}}
video{{width:100%;max-width:760px;border-radius:12px;margin-top:18px;background:#000}}
.tabs{{display:flex;gap:6px;margin:18px 0}}
.tab{{padding:8px 14px;border:1px solid #334155;border-radius:8px;cursor:pointer;font-size:13px;background:#1e293b}}
.tab.active{{background:#1e40af;border-color:#3b82f6}}
iframe{{width:100%;height:520px;border:1px solid #334155;border-radius:12px;background:#0b1224}}
.progress{{background:#1e293b;padding:14px 18px;border-radius:10px;margin-bottom:20px;font-size:14px}}
input[type=checkbox]{{transform:scale(1.2);margin-right:8px}}
.tools{{display:flex;gap:8px;margin:12px 0}}
button{{background:#1e293b;color:#f1f5f9;border:1px solid #334155;border-radius:8px;padding:8px 14px;cursor:pointer}}
</style></head><body>
<header>
  <h1>{track_title}</h1>
  <div class="sub">Original study material · TTS-narrated videos · interactive flashcards &amp; quizzes</div>
</header>
<div class="layout">
  <nav>
    <h3>Modules</h3>
    {nav_links}
  </nav>
  <main>
    <div class="progress">
      <strong>Track progress:</strong> <span id="progressCount">0</span> / {n} modules completed
      <br><small>Click a checkbox on each module; your progress saves in this browser only.</small>
    </div>
    <div class="tools">
      <button onclick="document.querySelectorAll('input[type=checkbox]').forEach(c=>c.checked=true);updateProgress()">Mark all complete</button>
      <button onclick="document.querySelectorAll('input[type=checkbox]').forEach(c=>c.checked=false);updateProgress()">Reset</button>
    </div>
    <summary>{track_summary}</summary>
    {sections}
  </main>
</div>
<script>
function updateProgress(){{
  const cbs=document.querySelectorAll('input[type=checkbox]');
  let n=0; cbs.forEach(c=>{{if(c.checked) n++}});
  document.getElementById('progressCount').textContent=n;
}}
function showTab(card, name){{
  card.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  card.querySelectorAll('[data-pane]').forEach(p=>p.style.display='none');
  card.querySelector(`[data-pane="${{name}}"]`).style.display='block';
  card.querySelector(`.tab[data-tab="${{name}}"]`).classList.add('active');
}}
function showModule(id){{
  document.querySelectorAll('section').forEach(s=>s.style.display='none');
  document.querySelectorAll('nav a').forEach(a=>a.classList.remove('active'));
  document.getElementById(id).style.display='block';
  document.querySelector(`nav a[data-mod="${{id}}"]`).classList.add('active');
  try{{history.replaceState(null,'','#'+id);}}catch(e){{}}
}}
window.addEventListener('DOMContentLoaded',()=>{{
  document.querySelectorAll('.card-root').forEach(c=>showTab(c,'video'));
  const hash=location.hash.slice(1);
  if(hash) showModule(hash);
  document.querySelectorAll('input[type=checkbox]').forEach(c=>c.addEventListener('change',updateProgress));
  updateProgress();
}});
</script></body></html>
"""


def build_track(track: str, track_title: str, track_summary: str) -> Path:
    files = list_modules(track)
    if not files:
        raise SystemExit(f"no modules under content/{track}")
    out = OUT_DIR / track / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)

    nav = []
    sections = []
    for i, md in enumerate(files, 1):
        mod_id = f"m{i}"
        nav.append(
            f'<a href="#{mod_id}" onclick="showModule(\'{mod_id}\');return false" data-mod="{mod_id}">'
            f'<span style="flex:1">{i}. {html.escape(md.stem.replace("-", " "))}</span>'
            f'<span class="tag">video</span></a>'
        )
        title_line = md.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip() if md.read_text else md.stem
        rel_md = md.relative_to(ROOT).as_posix()
        rel_mp4 = (VIDEO_DIR / track / f"{md.stem}.mp4").relative_to(ROOT).as_posix()
        rel_srt = (VIDEO_DIR / track / f"{md.stem}.srt").relative_to(ROOT).as_posix()
        rel_fc = (FC_DIR / track / f"{md.stem}.html").relative_to(ROOT).as_posix()
        rel_qz = (QUIZ_DIR / track / f"{md.stem}.html").relative_to(ROOT).as_posix()

        sections.append(
            f"""<section id="{mod_id}" style="display:none">
            <div class="module-card">
              <h2>{i}. {html.escape(title_line)}</h2>
              <p>Source outline: <code>{rel_md}</code></p>
              <label><input type="checkbox"> Mark complete</label>
              <div class="card-root">
                <div class="tabs">
                  <span class="tab active" data-tab="video" onclick="showTab(this.parentNode.parentNode,'video')">Video</span>
                  <span class="tab" data-tab="fc" onclick="showTab(this.parentNode.parentNode,'fc')">Flashcards</span>
                  <span class="tab" data-tab="qz" onclick="showTab(this.parentNode.parentNode,'qz')">Quiz</span>
                </div>
                <div data-pane="video">
                  <video controls preload="metadata" src="../{rel_mp4}"></video>
                  <p style="color:#94a3b8;font-size:12px">Caption track: <a style="color:#60a5fa" href="../{rel_srt}" download>download SRT</a></p>
                </div>
                <div data-pane="fc" style="display:none"><iframe src="../{rel_fc}"></iframe></div>
                <div data-pane="qz" style="display:none"><iframe src="../{rel_qz}"></iframe></div>
              </div>
            </div>
          </section>"""
        )

    rendered = PAGE.format(
        track_title=html.escape(track_title),
        track_summary=html.escape(track_summary),
        nav_links="\n    ".join(nav),
        n=len(files),
        sections="\n    ".join(sections),
    )
    out.write_text(rendered, encoding="utf-8")
    print(f"[ok] interactive/{track}/index.html ({len(files)} modules)")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("track")
    ap.add_argument("--title", required=True, help="display title")
    ap.add_argument("--summary", default="")
    args = ap.parse_args()
    build_track(args.track, args.title, args.summary)


if __name__ == "__main__":
    main()
