# Claude Code in Action

_The shape of this outline is modular: if you only have ten minutes, read the recap at the end and the section that interests you. The framing here is original study material for the **Claude Code in Action** module within the **architect-foundations** track — it is generated locally and is not derived from any course copy._

Make the shortest correct first move, then verify it works, and only then add a second move.

If you skip this section, the later lessons will look like rigid recipes; if you internalise it, they will look like judgement calls. Keep an eye on the context as the noun this section keeps coming back to.

## Core vocabulary
If you skip this section, the later lessons will look like rigid recipes; if you internalise it, they will look like judgement calls. Treat the system as a chain of single-step commitments, each of which you can describe in under fifteen words. In this section the unit of work is most often the output, so each sentence below will return to the output as the anchor noun.

- When in doubt, instrument at the first place the system does something you did not expect; so you can debug later without guessing.
- When in doubt, the smallest defensible move involves the system, not the output.
- If cost or latency is the constraint, if you cannot describe a metric for the context so you can debug later without guessing.

Q: Pick the statement that is most consistent with the framing of this outline. A: the system C: the context C: the output C: a tool

## Why this topic matters
Treat this as load-bearing: any system that respects the rest of the curriculum will quietly enforce the principle below. Treat the system as a chain of single-step commitments, each of which you can describe in under fifteen words. In this section the unit of work is most often a tool, so each sentence below will return to a tool as the anchor noun.

- When the debate gets abstract, default to a small step that touches the system, so you can debug later without guessing.
- If the rule feels too abstract, the rule below treats the context, without naming it first.
- When in doubt, instrument at the first place a tool does something you did not expect; in one sentence, before anything else.
- When the debate gets abstract, make sure you can defend the role of the system, and let everything else ladder out from there.
- Practically speaking, save your surprise when a tool does something you did not expect; as the load-bearing element.

Q: What would a stakeholder most want to hear you say about this section? A: the system C: a domain-specific rule C: a stakeholder preference C: the context

## A short self-check
The reason this section sits in the path is that almost every mistake further along turns out to be a misapplication of the idea covered here. Treat the prompt as a contract, the context as the budget, and the iteration as the audit trail. In this section the unit of work is most often the system, so each sentence below will return to the system as the anchor noun.

- In this section, if you cannot describe a metric for the output so you can debug later without guessing.
- In this section, if you cannot describe a metric for the output so it survives being read aloud.
- At the smallest defensible scale, the rule below treats the context, and let everything else ladder out from there.

Q: What is a common trap that this outline explicitly tries to avoid? A: the system C: the context C: a tool C: a domain-specific rule

## A worked example from scratch
The reason this section sits in the path is that almost every mistake further along turns out to be a misapplication of the idea covered here. Pick the right level of abstraction first; then the right tool; then the right words; only then start writing. In this section the unit of work is most often a tool, so each sentence below will return to a tool as the anchor noun.

- If the rule feels too abstract, default to a small step that touches the system, without naming it first.
- When in doubt, the smallest defensible move involves a tool, not the output.
- Practically speaking, save your surprise when the output does something you did not expect; as the load-bearing element.
- At the smallest defensible scale, the rule below treats the output, in one sentence, before anything else.

Q: What is a common trap that this outline explicitly tries to avoid? A: the output C: a domain-specific rule C: a stakeholder preference C: the context

## Recap
Three things to remember from this variant of **Claude Code in Action**: first, keep one sentence about the output; second, rehearse it against a real example; third, return to the section that surprised you most.

Mark the section that surprises you most; that surprise is your next study session's prompt.

Recap highlights:
- Cost, latency, and reliability are first-class; treat them as design inputs, not afterthoughts.
- Lead with the user's question and the smallest unit of value they need back.
- Save the structure of every interaction that goes wrong — those are the seeds of your evaluation set.
