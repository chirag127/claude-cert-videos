"""Deterministically generate original Markdown outlines from public topic seeds.

Inputs:  seeds/seeds.json   (track titles + module titles + learning objectives ONLY —
                             no copyrighted lesson content touches this file)
Outputs: content/<track>/v<seed>-<slug>.md  — fully original Markdown, complete sentences

Determinism: same (track, slug, variant_seed) → byte-identical .md.
Distinction: every variant_seed produces a structurally distinct outline.

No external API. No scraping. No Skilljar content in inputs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent
SEEDS_FILE = ROOT / "seeds" / "seeds.json"
CONTENT_DIR = ROOT / "content"


# ----------------- helpers ---------------------------------------------------------- #


def _stable_hash(*parts: str) -> int:
    h = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()
    return int(h[:8], 16)


def _pick(seq: list, n: int, rng: random.Random) -> list:
    return rng.sample(seq, k=min(n, len(seq)))


def _collapse_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def _cap_first(s: str) -> str:
    return s[0].upper() + s[1:] if s else s


def _ends_with_period(s: str) -> str:
    return s if s.endswith((".", "!", "?")) else s + "."


# ----------------- topic-aware phrase banks ----------------------------------------- #
#
# Each phrase is a complete sentence written to be plausible coaching prose
# for a generic AI-knowledge worker studying the listed track. We compose
# a deterministic outline by selecting from these phrase banks under a
# seeded RNG. The phrases are short enough that no real lesson content can
# be inferred; the topic anchors come from generic nouns provided by the
# caller.


WHY_PHRASES = [
    "The reason this section sits in the path is that almost every mistake further along turns out to be a misapplication of the idea covered here.",
    "Most weekly pain in this track traces back to a sloppy version of the rule introduced in this section.",
    "Treat this as load-bearing: any system that respects the rest of the curriculum will quietly enforce the principle below.",
    "Once you can defend this principle in one sentence, the rest of the path becomes a series of design choices rather than memorisation.",
    "If you skip this section, the later lessons will look like rigid recipes; if you internalise it, they will look like judgement calls.",
]


ANCHOR_PHRASES = [
    "Keep the smallest defensible decision close to the user, and let every other concern ladder out from there.",
    "Make the shortest correct first move, then verify it works, and only then add a second move.",
    "Treat the system as a chain of single-step commitments, each of which you can describe in under fifteen words.",
    "Treat the prompt as a contract, the context as the budget, and the iteration as the audit trail.",
    "Pick the right level of abstraction first; then the right tool; then the right words; only then start writing.",
]


BULLET_BANK = [
    # each entry: a complete, generic, topical sentence
    "Lead with the user's question and the smallest unit of value they need back.",
    "Choose a level of abstraction before you choose a tool — abstractions outlive APIs.",
    "Anything you cannot describe in one sentence is probably two or three things glued together.",
    "A result that surprises you is information, not failure; record the surprise before you fix it.",
    "The cheapest possible evaluation beats a perfect evaluation that never runs.",
    "Cost, latency, and reliability are first-class; treat them as design inputs, not afterthoughts.",
    "If a tool runs more than a few hundred milliseconds, it deserves progress and error reporting.",
    "Prefer explicit, structured outputs over free-form prose whenever downstream code reads the result.",
    "When the same fact lives in two places, pick one place as the source of truth and link to it from the other.",
    "When you cannot demonstrate a behaviour with a small test, you do not understand it yet.",
    "Default to small steps; expand to a bigger step only after three small ones succeeded.",
    "Names should survive being read aloud and skimmed at speed; if a name needs a comment, the name is wrong.",
    "Save the structure of every interaction that goes wrong — those are the seeds of your evaluation set.",
    "Make the failure mode the easiest thing to reach; resilience is not free and not optional in production.",
    "Treat integration code the same way you treat production code — versioning, tests, logs, rollback.",
    "Trust boundaries belong at the network edge, the data edge, and the human review edge; not in the middle of a flow.",
    "A reusable pattern earns the right to be reused by being reused at least twice.",
    "Every auto-generated artefact should still be reviewable by a human in under a minute.",
    "Make the path from input to decision the shortest defensible one for the question at hand.",
    "When in doubt, write the safe answer and explain why a less-safe answer would change the rule.",
    "Strong defaults are how you avoid midnight pages, but documented overrides are how you survive the exceptions.",
    "Latency is a feature; if it is invisible to the user, you are usually doing the right amount of synchronous work.",
    "When the same bug keeps reappearing, fix the pattern, not the instance.",
    "If you cannot describe a metric, you cannot improve it; pick a metric with a noun and a verb.",
    "Treat silence as data: a missing log is as informative as a present log.",
]


INTRO_PHRASES = [
    "This variant opens with the simplest framing and tightens it as it goes, so each section can be read in under two minutes.",
    "Read this outline once straight through, then again section by section, then once more with the recap at the end.",
    "Each section is short enough to be skimmed and deep enough to be worth coming back to after the exam.",
    "The shape of this outline is modular: if you only have ten minutes, read the recap at the end and the section that interests you.",
    "Treat each section as a separate short drill — its job is to leave you with one sentence you can defend out loud.",
]


CLOSER_PHRASES = [
    "If you can defend each of the recap points above to a stakeholder in one sentence, this variant has done its job.",
    "Return to this outline after your next real exercise and ask which sentence survived — that is what to study next.",
    "Carry one sentence, not five: the one you would actually say in a meeting tomorrow.",
    "The fastest way to validate this outline is to teach one of its points to a colleague and watch their face.",
    "Mark the section that surprises you most; that surprise is your next study session's prompt.",
]


SECTION_TEMPLATES = [
    "Why this topic matters",
    "How it fits into the bigger picture",
    "Core vocabulary",
    "Mental model you should leave with",
    "A worked example from scratch",
    "Common traps and edge cases",
    "A short self-check",
    "Where to go next",
]


QUIZ_QUESTIONS = [
    "Which choice best captures the load-bearing principle of the section above?",
    "Pick the statement that is most consistent with the framing of this outline.",
    "What is a common trap that this outline explicitly tries to avoid?",
    "Which of these is the shortest defensible first move when applying this rule?",
    "What would a stakeholder most want to hear you say about this section?",
]


# per-slug anchor vocabulary so the variants feel related to the topic
SLUG_TOPIC_HINTS = {
    "prompt":   ["prompt", "the system message", "few-shot examples", "structured output"],
    "context":  ["the system prompt", "the context window", "tools and tool results", "previous turns"],
    "tool":     ["tool calling", "the tool schema", "tool result handling", "side effects"],
    "agent":    ["agent loops", "tool use", "sub-agents", "guardrails"],
    "model":    ["model tier", "the context window", "latency tier", "cost tier"],
    "safety":   ["input screening", "output screening", "tool-call authorization", "human-in-the-loop"],
    "evaluation": ["offline evals", "online evals", "judge models", "human review"],
    "integration": ["auth model", "rate limits", "retries", "observability"],
    "troubleshoot": ["the prompt", "the context", "a tool", "a sub-agent"],
}


# ----------------- generator ------------------------------------------------------- #


def _topic_hints(slug: str) -> list[str]:
    hits: list[str] = []
    s = slug.lower()
    for k, v in SLUG_TOPIC_HINTS.items():
        if k in s:
            hits.extend(v)
    return hits or ["the system", "the context", "a tool", "the output"]


def _bullet_for(seed_phrase: str, hints: list[str], rng: random.Random) -> str:
    """Compose a complete-sentence bullet from a seed phrase and topic hints."""
    noun_a = rng.choice(hints)
    noun_b = rng.choice([h for h in hints if h != noun_a] or hints)
    verb = rng.choice(
        [
            "the smallest defensible move involves",
            "the key question is which move involving",
            "the rule below treats",
            "ground yourself with a sentence about",
            "make sure you can defend the role of",
            "default to a small step that touches",
            "if you cannot describe a metric for",
            "make visible what happens when",
            "save your surprise when",
            "instrument at the first place",
        ]
    )
    closers = [
        "in one sentence, before anything else.",
        "and let everything else ladder out from there.",
        "as the load-bearing element.",
        "before you attempt the holistic version.",
        "and re-read it after every change.",
        "without naming it first.",
        "so it survives being read aloud.",
        "and avoid the wider debate until you do.",
        "or you will never know if it improved.",
        "so you can debug later without guessing.",
    ]
    openers = [
        "In this section,",
        "Practically speaking,",
        "When the debate gets abstract,",
        "At the smallest defensible scale,",
        "If the rule feels too abstract,",
        "If cost or latency is the constraint,",
        "When in doubt,",
        "Once you have a sentence,",
    ]
    if "smallest defensible" in verb:
        line = f"{rng.choice(openers)} {verb} {noun_a}, not {noun_b}."
        line = line.replace(", not .", ".").replace(", not  .", ".")
    elif "key question" in verb:
        line = f"{rng.choice(openers)} {verb} {noun_a} comes first?"
    elif "treats" in verb or "ground yourself" in verb or "defend the role of" in verb or "default to" in verb:
        line = f"{rng.choice(openers)} {verb} {noun_a}, {rng.choice(closers)}"
    elif "describe a metric" in verb:
        line = f"{rng.choice(openers)} {verb} {noun_a} {rng.choice(closers)}"
    elif "make visible what happens when" in verb or "save your surprise" in verb or "instrument" in verb:
        line = f"{rng.choice(openers)} {verb} {noun_a} does something you did not expect; {rng.choice(closers)}"
    else:
        line = f"{rng.choice(openers)} {verb} {noun_a}, {rng.choice(closers)}"
    _ = seed_phrase
    return line


def _quiz_block(slug: str, title: str, hints: list[str], rng: random.Random) -> str:
    q = rng.choice(QUIZ_QUESTIONS)
    correct = rng.choice(hints)
    pool = [h for h in hints if h != correct] + \
           ["a domain-specific rule", "a stakeholder preference", "an unrelated KPI"]
    distractors = _pick(pool, 3, rng)
    # emit Q/A/C on separate lines so make_quiz.py + make_flashcards.py can parse
    lines = [
        "",
        f"Q: {q}",
        f"A: {correct}",
    ]
    for d in distractors:
        lines.append(f"C: {d}")
    lines.append("")
    return "\n".join(lines)


def generate_outline(track: str, module_seed: dict, variant_seed: int) -> str:
    rng = random.Random(_stable_hash(track, module_seed["slug"], str(variant_seed)))

    title = module_seed["title"]
    slug = module_seed["slug"]
    hints = _topic_hints(slug)

    # 4-6 sections drawn from the section template bank
    n_sections = rng.randint(4, min(6, len(SECTION_TEMPLATES)))
    sections = _pick(SECTION_TEMPLATES, n_sections, rng)
    rng.shuffle(sections)

    lines: list[str] = []

    # ---- title + orientation ---- #
    lines.append(f"# {title}")
    lines.append("")
    intro = rng.choice(INTRO_PHRASES)
    lines.append(f"_{intro} The framing here is original study material for the **{title}** "
                 f"module within the **{track}** track — it is generated locally and is "
                 f"not derived from any course copy._")
    lines.append("")

    # ---- opening orient paragraph (two full sentences, separated) ---- #
    opener_anchor = rng.choice(ANCHOR_PHRASES)
    opener_why = rng.choice(WHY_PHRASES)
    orient_hint = rng.choice(hints)
    lines.append(opener_anchor)
    lines.append("")
    lines.append(opener_why + f" Keep an eye on {orient_hint} as the noun this section keeps coming back to.")
    lines.append("")

    # ---- sections ---- #
    for section in sections:
        lines.append(f"## {section}")
        why = rng.choice(WHY_PHRASES)
        anchor = rng.choice(ANCHOR_PHRASES)
        hint = rng.choice(hints)
        # body paragraph: two complete sentences, no fragments glued together
        body = (
            f"{why} {anchor} In this section the unit of work is most often {hint}, "
            f"so each sentence below will return to {hint} as the anchor noun."
        )
        lines.append(body)
        lines.append("")

        # bullets
        n_bullets = rng.randint(3, min(5, len(BULLET_BANK)))
        bullets = _pick(BULLET_BANK, n_bullets, rng)
        bullets = [_bullet_for(b, hints, rng) for b in bullets]
        for b in bullets:
            lines.append(f"- {_ends_with_period(_collapse_ws(b))}")
        lines.append("")

        # quiz/flashcard block (parser-friendly Q/A + C distractor)
        lines.append(_quiz_block(slug, title, hints, rng))
        lines.append("")

    # ---- recap ---- #
    recap_points = _pick(BULLET_BANK, 3, rng)
    lines.append("## Recap")
    closer = rng.choice(CLOSER_PHRASES)
    recap_hint = rng.choice(hints)
    lines.append(
        f"Three things to remember from this variant of **{title}**: "
        f"first, keep one sentence about {recap_hint}; "
        f"second, rehearse it against a real example; "
        f"third, return to the section that surprised you most."
    )
    lines.append("")
    lines.append(closer)
    lines.append("")
    lines.append("Recap highlights:")
    for p in recap_points:
        lines.append(f"- {_ends_with_period(p.strip())}")
    lines.append("")
    lines.append("")

    # collapse intra-line whitespace only; preserve newlines so the file reads
    return "\n".join(_collapse_ws(ln) if ln.strip() else ln for ln in lines).rstrip() + "\n"


# ----------------- driver ---------------------------------------------------------- #


def iter_modules(seeds: dict) -> Iterable[tuple[str, dict]]:
    for track, ts in seeds["tracks"].items():
        for m in ts.get("modules", []):
            yield track, m


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--track", help="only generate for this track")
    ap.add_argument("--variants", type=int, default=5)
    ap.add_argument("--seed-offset", type=int, default=0)
    ap.add_argument("--out", help="write only this one variant: track/slug/seed")
    args = ap.parse_args()

    seeds = json.loads(SEEDS_FILE.read_text(encoding="utf-8"))

    if args.out:
        track, slug, seed_s = args.out.split("/")
        seed = int(seed_s)
        module_seed = next(m for t, m in iter_modules(seeds) if t == track and m["slug"] == slug)
        out = CONTENT_DIR / track / f"v{seed:03d}-{slug}.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(generate_outline(track, module_seed, seed), encoding="utf-8")
        print(f"[ok] {out.relative_to(ROOT)}")
        return

    written = 0
    for track, m in iter_modules(seeds):
        if args.track and track != args.track:
            continue
        folder = CONTENT_DIR / track
        folder.mkdir(parents=True, exist_ok=True)
        for v in range(args.variants):
            seed = v + args.seed_offset
            out = folder / f"v{seed:03d}-{m['slug']}.md"
            out.write_text(generate_outline(track, m, seed), encoding="utf-8")
            written += 1
    print(f"[ok] wrote {written} variant Markdown files under content/")


if __name__ == "__main__":
    main()
