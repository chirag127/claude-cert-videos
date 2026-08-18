"""Generate HTML flashcards for one outline module.

Reads the original Markdown under content/ and either:
  (a) extracts explicit `Q: ... | A: ...` pairs if present, or
  (b) treats the first sentence of each section as the term and the
      remaining bullets as the definition.

Writes a self-contained HTML page with click-to-flip cards, prev/next,
keyboard shortcuts, and an optional 'shuffle' button. No external assets.
"""
from __future__ import annotations

import argparse
import html
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT_DIR = ROOT / "content"
OUT_DIR = ROOT / "flashcards"


def extract_cards(md_path: Path) -> tuple[str, list[tuple[str, str]]]:
    text = md_path.read_text(encoding="utf-8")
    title = (text.splitlines()[0].lstrip("# ").strip() if text else md_path.stem)
    cards: list[tuple[str, str]] = []

    # explicit Q/A blocks
    for m in re.finditer(r"^\s*Q:\s*(.+?)\n\s*A:\s*(.+?)(?=\n\s*(?:Q:|$))", text, flags=re.M | re.S):
        cards.append((m.group(1).strip(), m.group(2).strip()))

    if not cards:
        # fallback: term from heading, def from bullets
        sections: list[tuple[str, list[str]]] = []
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
            bullets = [b[2:].strip() for b in body if b.strip().startswith(("- ", "* "))]
            if not bullets:
                continue
            term = st
            # first bullet becomes definition; remaining become extended notes
            defn = bullets[0]
            extra = "\n".join(f"- {b}" for b in bullets[1:6])
            cards.append((term, defn + ("\n\nMore:\n" + extra if extra else "")))

    return title, cards


PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>{title} — flashcards</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root {{color-scheme:light dark}}
body{{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;margin:0;background:#0f172a;color:#f1f5f9}}
.wrap{{max-width:760px;margin:40px auto;padding:0 20px}}
h1{{font-size:24px;margin:0 0 16px}}
.toolbar{{display:flex;gap:8px;margin-bottom:20px;flex-wrap:wrap}}
button{{background:#1e293b;color:#f1f5f9;border:1px solid #334155;border-radius:8px;padding:8px 14px;cursor:pointer;font-size:14px}}
button:hover{{background:#334155}}
.card{{perspective:1200px;height:280px;margin-bottom:18px}}
.card-inner{{position:relative;width:100%;height:100%;transition:transform .6s;transform-style:preserve-3d}}
.card.flip .card-inner{{transform:rotateY(180deg)}}
.face{{position:absolute;inset:0;background:#1e293b;border:1px solid #334155;border-radius:14px;display:flex;align-items:center;justify-content:center;padding:24px;text-align:center;font-size:20px;line-height:1.4;backface-visibility:hidden}}
.back{{transform:rotateY(180deg);background:#0b1224;border-color:#475569}}
.meta{{font-size:13px;color:#94a3b8;margin-bottom:8px;display:flex;justify-content:space-between}}
.front-term{{font-weight:600;font-size:26px}}
.defn{{white-space:pre-wrap}}
</style></head><body>
<div class="wrap">
  <h1>{title} — flashcards</h1>
  <div class="toolbar">
    <button id="prev">◀ Prev (←)</button>
    <button id="flip">Flip (Space)</button>
    <button id="next">Next (→)</button>
    <button id="shuffle">Shuffle</button>
    <span style="flex:1"></span>
    <button id="export">Export JSON</button>
  </div>
  <div class="meta"><span id="pos">1 / {n}</span><span id="hint">click card or press Space to flip</span></div>
  <div class="card" id="card">
    <div class="card-inner">
      <div class="face front"><span class="front-term" id="front"></span></div>
      <div class="face back"><span class="defn" id="back"></span></div>
    </div>
  </div>
  <p style="color:#94a3b8;font-size:13px">Cards: {n} · Click any card to flip · Use ← / → to navigate</p>
</div>
<script>
const CARDS = {cards_json};
let i=0, order=[...CARDS.keys()];
const card=document.getElementById('card');
const front=document.getElementById('front');
const back=document.getElementById('back');
const pos=document.getElementById('pos');
function show(){{
  const idx=order[i];
  const c=CARDS[idx];
  front.textContent=c[0]; back.textContent=c[1];
  pos.textContent=`${{i+1}} / ${{CARDS.length}}`;
  card.classList.remove('flip');
}}
show();
card.onclick=()=>card.classList.toggle('flip');
document.getElementById('flip').onclick=()=>card.classList.toggle('flip');
document.getElementById('prev').onclick=()=>{{i=(i-1+CARDS.length)%CARDS.length;show()}};
document.getElementById('next').onclick=()=>{{i=(i+1)%CARDS.length;show()}};
document.getElementById('shuffle').onclick=()=>{{order=[...CARDS.keys()].sort(()=>Math.random()-0.5);i=0;show()}};
document.getElementById('export').onclick=()=>{{
  const blob=new Blob([JSON.stringify(CARDS,null,2)],{{type:'application/json'}});
  const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='{slug}.flashcards.json';a.click();
}};
document.addEventListener('keydown',e=>{{
  if(e.key==='ArrowLeft')document.getElementById('prev').click();
  else if(e.key==='ArrowRight')document.getElementById('next').click();
  else if(e.key===' '||e.key==='Enter'){{e.preventDefault();document.getElementById('flip').click();}}
}});
</script></body></html>
"""


def write_deck(track: str, md_path: Path, out_dir: Path = OUT_DIR) -> Path:
    title, cards = extract_cards(md_path)
    if not cards:
        raise SystemExit(f"no cards in {md_path}")
    out = out_dir / track / f"{md_path.stem}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    cards_json = "[%s]" % ",".join(
        '["%s","%s"]' % (html.escape(q).replace('"', '\\"'), html.escape(a).replace('"', '\\"'))
        for q, a in cards
    )
    rendered = PAGE.format(
        title=html.escape(title),
        n=len(cards),
        slug=md_path.stem,
        cards_json=cards_json,
    )
    out.write_text(rendered, encoding="utf-8")
    print(f"[ok] flashcards/{track}/{md_path.stem}.html  ({len(cards)} cards)")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("track")
    ap.add_argument("module")
    args = ap.parse_args()
    md = ROOT / "content" / args.track / (args.module if args.module.endswith(".md") else f"{args.module}.md")
    if not md.exists():
        raise SystemExit(f"missing: {md}")
    write_deck(args.track, md)


if __name__ == "__main__":
    main()
