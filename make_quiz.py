"""Generate an HTML multiple-choice quiz per module from an original Markdown outline.

Reads the content/ Markdown files; honors blocks of the form:
    Q: Question text?
    A: correct
    C: distractor one
    C: distractor two
    C: distractor three
Falls back to producing 3 quizzes from the bullet takeaways if no Q/A block is
present: each bullet becomes a true/false styled prompt.

Self-contained HTML; no external assets; results scored client-side.
"""
from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT_DIR = ROOT / "content"
OUT_DIR = ROOT / "quizzes"


def parse_quiz(md_path: Path) -> tuple[str, list[dict]]:
    """Return (title, [questions])."""
    text = md_path.read_text(encoding="utf-8")
    title = (text.splitlines()[0].lstrip("# ").strip() if text else md_path.stem)
    questions: list[dict] = []

    # explicit Q/A/C blocks
    blocks = re.findall(
        r"Q:\s*(.+?)\n\s*A:\s*(.+?)(?:\n\s*C:\s*(.+?))(?:\n\s*C:\s*(.+?))?(?:\n\s*C:\s*(.+?))?",
        text,
        flags=re.M,
    )
    for q, a, *cs in blocks:
        choices = [a] + [c for c in cs if c]
        if len(choices) < 2:
            continue
        random_order = sorted(range(len(choices)), key=lambda _: __import__("random").random())
        questions.append({
            "q": q.strip(),
            "choices": [choices[i] for i in random_order],
            "answer": random_order.index(0),
        })

    if not questions:
        # fallback: derive true/false from takeaways
        sections = []
        ct, cb = None, []
        for ln in text.splitlines():
            if ln.startswith("## "):
                if ct is not None:
                    sections.append((ct, cb))
                ct = ln[3:].strip()
                cb = []
            elif ct is not None:
                cb.append(ln)
        if ct is not None:
            sections.append((ct, cb))
        for st, body in sections:
            for ln in body:
                ln = ln.strip()
                if ln.startswith(("- ", "* ")):
                    item = ln[2:].strip()
                    if not item:
                        continue
                    questions.append({
                        "q": f"True or False: {item}",
                        "choices": ["True", "False"],
                        "answer": 0,
                    })
                    if len(questions) >= 6:
                        break
            if len(questions) >= 6:
                break

    return title, questions


PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>{title} — quiz</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root{{color-scheme:light dark}}
body{{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;margin:0;background:#0f172a;color:#f1f5f9}}
.wrap{{max-width:760px;margin:40px auto;padding:0 20px}}
h1{{font-size:24px;margin:0 0 16px}}
.progress{{height:8px;background:#1e293b;border-radius:4px;overflow:hidden;margin-bottom:24px}}
.bar{{height:100%;background:linear-gradient(90deg,#3b82f6,#22d3ee);width:0;transition:width .25s}}
.q{{font-size:22px;line-height:1.45;margin:0 0 18px}}
.choices{{display:grid;gap:10px}}
.choice{{background:#1e293b;border:1px solid #334155;border-radius:10px;padding:14px 16px;cursor:pointer;text-align:left;font-size:16px;color:#e2e8f0}}
.choice:hover{{background:#334155}}
.choice.correct{{background:#14532d;border-color:#22c55e}}
.choice.wrong{{background:#7f1d1d;border-color:#ef4444}}
.toolbar{{display:flex;gap:8px;margin-top:18px}}
button{{background:#1e293b;color:#f1f5f9;border:1px solid #334155;border-radius:8px;padding:8px 14px;cursor:pointer;font-size:14px}}
button.primary{{background:#2563eb;border-color:#1d4ed8}}
.score{{font-size:18px;text-align:center;padding:24px;background:#1e293b;border-radius:12px}}
</style></head><body>
<div class="wrap">
  <h1>{title} — quiz</h1>
  <div class="progress"><div class="bar" id="bar"></div></div>
  <div id="root"></div>
</div>
<script>
const Q = {questions_json};
let i=0, score=0, answered=false;
const root=document.getElementById('root');
const bar=document.getElementById('bar');
function render(){{
  if(i>=Q.length){{
    const pct=Math.round(score/Q.length*100);
    root.innerHTML=`<div class="score">Score: ${{score}} / ${{Q.length}} (${{pct}}%)<br><br><button class="primary" onclick="location.reload()">Restart</button></div>`;
    bar.style.width='100%';
    return;
  }}
  bar.style.width=`${{Math.round(i/Q.length*100)}}%`;
  const q=Q[i];
  root.innerHTML=`<div class="q">${{i+1}}. ${{q.q}}</div><div class="choices" id="choices"></div>`;
  const ch=document.getElementById('choices');
  q.choices.forEach((c,idx)=>{{
    const b=document.createElement('button');
    b.className='choice'; b.textContent=c;
    b.onclick=()=>{{
      if(answered) return; answered=true;
      if(idx===q.answer){{b.classList.add('correct'); score++;}}
      else{{b.classList.add('wrong'); ch.children[q.answer].classList.add('correct');}}
      setTimeout(()=>{{answered=false; i++; render();}},900);
    }};
    ch.appendChild(b);
  }});
}}
render();
</script></body></html>
"""


def write_quiz(track: str, md_path: Path, out_dir: Path = OUT_DIR) -> Path:
    title, questions = parse_quiz(md_path)
    if not questions:
        raise SystemExit(f"no questions in {md_path}")
    out = out_dir / track / f"{md_path.stem}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    rendered = PAGE.format(
        title=html.escape(title),
        questions_json=json.dumps(questions),
    )
    out.write_text(rendered, encoding="utf-8")
    print(f"[ok] quizzes/{track}/{md_path.stem}.html  ({len(questions)} questions)")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("track")
    ap.add_argument("module")
    args = ap.parse_args()
    md = ROOT / "content" / args.track / (args.module if args.module.endswith(".md") else f"{args.module}.md")
    if not md.exists():
        raise SystemExit(f"missing: {md}")
    write_quiz(args.track, md)


if __name__ == "__main__":
    main()
