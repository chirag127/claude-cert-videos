#!/usr/bin/env python3
"""
Parse a raw Anthropic course module HTML (the self-contained SCORM HTML) into
COMPLETE structured content:

  - every screen: meta (type + section), title, teaching prose IN ORDER
  - tab groups: each tab label paired with its full panel text
  - callouts (Cost/Complexity/Risk etc.), reveal blocks, flip cards
  - checkpoints / MCQs: question, all options (letter + text), the correct
    answer and the full feedback/explanation text (mined from the JS `fb(...)`
    calls and option arrays that the page uses to grade answers)
  - glossary terms + definitions

Output: JSON  {title, module, screens:[...]}  written next to the html as
        .parsed/<name>.json

Usage: python parse_module.py .source_html/m3.html 3
"""
import json
import re
import sys
from pathlib import Path
from html.parser import HTMLParser
from html import unescape

ROOT = Path(__file__).resolve().parent


# ---------------------------------------------------------------- JS feedback mining
def mine_js(html):
    """Return dict of feedback-id -> {kind, title, text} from fb('id','kind','Title','Text') calls,
    plus option arrays name -> [strings]."""
    scripts = re.findall(r"<script[^>]*>(.*?)</script>", html, re.S)
    js = "\n".join(scripts)

    fb = {}
    # fb('id','kind','title','explanation')  — args are single-quoted JS strings with \' escapes
    def _jsstr(s):
        # unescape common JS string escapes
        return (s.replace("\\'", "'").replace('\\"', '"')
                 .replace("\\n", " ").replace("\\t", " ").replace("\\\\", "\\")).strip()

    # scan for fb( ... ) with 4 single-quoted args, tolerant of escaped quotes
    i = 0
    call = re.compile(r"fb\(\s*'")
    for m in re.finditer(r"fb\(\s*", js):
        # manually parse up to 4 single-quoted args
        pos = m.end()
        args = []
        ok = True
        for _ in range(4):
            # skip whitespace/comma
            while pos < len(js) and js[pos] in " ,\n\t":
                pos += 1
            if pos >= len(js) or js[pos] != "'":
                ok = False
                break
            pos += 1
            buf = []
            while pos < len(js):
                c = js[pos]
                if c == "\\" and pos + 1 < len(js):
                    buf.append(js[pos:pos+2]); pos += 2; continue
                if c == "'":
                    pos += 1; break
                buf.append(c); pos += 1
            args.append("".join(buf))
        if ok and len(args) == 4:
            fbid, kind, title, text = (_jsstr(a) for a in args)
            # keep the "correct"/pass explanation preferentially
            entry = fb.setdefault(fbid, {})
            entry[kind] = {"title": title, "text": text}

    # option arrays:  const NAME = [ '...', '...' ];
    opt_arrays = {}
    for m in re.finditer(r"(?:const|let|var)\s+(\w+)\s*=\s*\[(.*?)\];", js, re.S):
        name, body = m.group(1), m.group(2)
        strs = re.findall(r"'((?:[^'\\]|\\.)*)'", body)
        if strs and ("OPT" in name.upper() or "CHOICE" in name.upper() or "ANSWER" in name.upper()):
            opt_arrays[name] = [_jsstr(s) for s in strs]

    # {s:'stem', opts:[...], ans:idx, rat:'rationale'} question objects (M1/M5 style)
    # Anchor on the s/opts/ans/rat run; tolerate any preceding keys (n:, id:, etc.)
    questions = []
    qpat = re.compile(
        r"s\s*:\s*'((?:[^'\\]|\\.)*)'\s*,\s*"
        r"opts\s*:\s*\[(.*?)\]\s*,\s*"
        r"ans\s*:\s*(\d+)\s*,\s*"
        r"rat\s*:\s*'((?:[^'\\]|\\.)*)'", re.S)
    for qm in qpat.finditer(js):
        stem = _jsstr(qm.group(1))
        opts = [_jsstr(s) for s in re.findall(r"'((?:[^'\\]|\\.)*)'", qm.group(2))]
        ans = int(qm.group(3))
        letter = chr(ord('a') + ans) if 0 <= ans < 26 else str(ans)
        questions.append({"stem": stem, "opts": opts, "ans": ans,
                          "letter": letter, "rationale": _jsstr(qm.group(4))})
    return fb, opt_arrays, questions


# ---------------------------------------------------------------- HTML -> text with structure
class Block(HTMLParser):
    """Walk a fragment, emitting readable text; tracks tab panels, mc-opts, callouts."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []           # list of ("kind", text) tuples
        self.stack = []         # (tag, classattr)
        self._buf = []
        self._cur_class = ""

    def _flush(self, kind="p"):
        t = unescape("".join(self._buf)).strip()
        t = re.sub(r"[ \t]+", " ", t)
        if t:
            self.out.append((kind, t))
        self._buf = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        cls = d.get("class", "")
        self.stack.append((tag, cls))
        if tag in ("p", "li", "h1", "h2", "h3", "h4", "div", "button", "span", "code", "strong", "tr"):
            # boundaries that should break text
            if tag in ("p", "li", "h2", "h3", "h4", "tr", "div"):
                self._flush()
        if tag == "br":
            self._buf.append(" ")

    def handle_endtag(self, tag):
        # flush on block ends, tagging special ones
        cls = ""
        for t, c in reversed(self.stack):
            if t == tag:
                cls = c
                break
        kind = "p"
        if tag in ("h1", "h2", "h3", "h4"):
            kind = "h"
        if "mc-opt-label" in cls:
            kind = "opt"
        if "tab-btn" in cls:
            kind = "tab"
        if tag in ("p", "li", "h1", "h2", "h3", "h4", "div", "button"):
            self._flush(kind)
        # pop stack
        for idx in range(len(self.stack) - 1, -1, -1):
            if self.stack[idx][0] == tag:
                del self.stack[idx]
                break

    def handle_data(self, data):
        self._buf.append(data)


def frag_text(fragment_html):
    b = Block()
    b.feed(fragment_html)
    b._flush()
    return b.out


# ---------------------------------------------------------------- main parse
SEC_TYPES = ("Orientation", "Teaching", "Watch Out", "Checkpoint",
             "Cumulative", "Recap", "Glossary", "Module Complete")


def parse(html, module_no):
    title = ""
    mt = re.search(r"<title>(.*?)</title>", html, re.S)
    if mt:
        title = unescape(re.sub(r"\s+", " ", mt.group(1))).split(":")[0].strip()

    fb, opt_arrays, questions = mine_js(html)

    # split into .screen sections by locating each <section class="screen"...> ... balance
    screens = []
    for m in re.finditer(r'<section[^>]*class="[^"]*screen[^"]*"[^>]*>', html):
        start = m.start()
        # find matching close by scanning sections (they are siblings, not nested)
        nxt = html.find('<section', m.end())
        end = nxt if nxt != -1 else html.find("</main>", m.end())
        if end == -1:
            end = len(html)
        screens.append(html[start:end])

    parsed = []
    for sec in screens:
        meta_m = re.search(r'class="screen-meta"[^>]*>(.*?)</div>', sec, re.S)
        meta = unescape(re.sub(r"<[^>]+>", " ", meta_m.group(1))) if meta_m else ""
        meta = re.sub(r"\s+", " ", meta).strip()
        title_m = re.search(r'class="screen-title"[^>]*>(.*?)</h1>', sec, re.S)
        stitle = unescape(re.sub(r"<[^>]+>", " ", title_m.group(1))).strip() if title_m else ""
        stitle = re.sub(r"\s+", " ", stitle)

        # tabs: pair each tab-btn label with its tab-panel text in order
        tabs = []
        btns = re.findall(r'<button[^>]*class="tab-btn[^"]*"[^>]*>(.*?)</button>', sec, re.S)
        panels = re.findall(r'<div[^>]*class="tab-panel[^"]*"[^>]*>(.*?)</div>\s*(?=<div[^>]*class="tab-panel|</div>\s*</div>|$)', sec, re.S)
        # fallback simpler panel capture
        if not panels:
            panels = re.findall(r'class="tab-panel[^"]*"[^>]*>(.*?)</div>', sec, re.S)
        for i, bt in enumerate(btns):
            label = unescape(re.sub(r"<[^>]+>", "", bt)).strip()
            body = ""
            if i < len(panels):
                body = " ".join(t for _, t in frag_text(panels[i]))
            tabs.append({"label": label, "body": body})

        # mc options (checkpoint)
        opts = []
        for om in re.finditer(r'class="mc-opt"[^>]*data-i="(\d+)"[^>]*>(.*?)</div>\s*(?=<div class="mc-opt"|</)', sec, re.S):
            lbl = re.search(r'mc-opt-letter">(.*?)</span>.*?mc-opt-label">(.*?)</span>', om.group(2), re.S)
            if lbl:
                opts.append({"letter": unescape(lbl.group(1)).strip(),
                             "text": unescape(re.sub(r"<[^>]+>", "", lbl.group(2))).strip()})

        # feedback ids referenced in this screen
        fbids = re.findall(r'id="(fb\w+)"', sec)
        feedback = []
        for fid in fbids:
            if fid in fb:
                for kind, v in fb[fid].items():
                    feedback.append({"kind": kind, "title": v["title"], "text": v["text"]})

        # main prose: strip tabs/scripts/mc-opts, then extract readable blocks in order
        clean = sec
        clean = re.sub(r"<script.*?</script>", "", clean, flags=re.S)
        clean = re.sub(r'<div[^>]*class="tabs".*?</div>\s*</div>', "", clean, flags=re.S)  # rough
        blocks = frag_text(clean)
        prose = []
        for kind, t in blocks:
            if kind in ("h", "p") and len(t) > 1:
                prose.append(t)

        parsed.append({
            "meta": meta,
            "title": stitle,
            "prose": prose,
            "tabs": tabs,
            "options": opts,
            "feedback": feedback,
        })

    return {"title": title, "module": module_no, "screens": parsed,
            "quiz_questions": questions}


if __name__ == "__main__":
    src = sys.argv[1]
    mod = int(sys.argv[2]) if len(sys.argv) > 2 else None
    html = Path(src).read_text(encoding="utf-8")
    data = parse(html, mod)
    outdir = ROOT / ".parsed"
    outdir.mkdir(exist_ok=True)
    name = Path(src).stem
    outp = outdir / f"{name}.json"
    outp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    scr = data["screens"]
    print(f"{name}: {len(scr)} screens")
    print(f"  tabs total: {sum(len(s['tabs']) for s in scr)}")
    print(f"  mc options total: {sum(len(s['options']) for s in scr)}")
    print(f"  feedback blocks: {sum(len(s['feedback']) for s in scr)}")
    print(f"  quiz questions (opts/ans/rat): {len(data.get('quiz_questions', []))}")
    print(f"  prose blocks: {sum(len(s['prose']) for s in scr)}")
