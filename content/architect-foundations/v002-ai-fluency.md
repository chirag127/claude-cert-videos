# AI Fluency: Framework & Foundations

_The shape of this outline is modular: if you only have ten minutes, read the recap at the end and the section that interests you. The framing here is original study material for the **AI Fluency: Framework & Foundations** module within the **architect-foundations** track — it is generated locally and is not derived from any course copy._

Pick the right level of abstraction first; then the right tool; then the right words; only then start writing.

Once you can defend this principle in one sentence, the rest of the path becomes a series of design choices rather than memorisation. Keep an eye on a tool as the noun this section keeps coming back to.

## A short self-check
The reason this section sits in the path is that almost every mistake further along turns out to be a misapplication of the idea covered here. Make the shortest correct first move, then verify it works, and only then add a second move. In this section the unit of work is most often the context, so each sentence below will return to the context as the anchor noun.

- When in doubt, the rule below treats a tool, without naming it first.
- Practically speaking, the rule below treats the output, and let everything else ladder out from there.
- At the smallest defensible scale, ground yourself with a sentence about the context, and re-read it after every change.
- In this section, if you cannot describe a metric for the system or you will never know if it improved.
- If cost or latency is the constraint, save your surprise when the system does something you did not expect; and let everything else ladder out from there.

Q: What is a common trap that this outline explicitly tries to avoid? A: a tool C: an unrelated KPI C: the context C: a stakeholder preference

## How it fits into the bigger picture
If you skip this section, the later lessons will look like rigid recipes; if you internalise it, they will look like judgement calls. Treat the system as a chain of single-step commitments, each of which you can describe in under fifteen words. In this section the unit of work is most often a tool, so each sentence below will return to a tool as the anchor noun.

- Once you have a sentence, if you cannot describe a metric for the output so you can debug later without guessing.
- Practically speaking, make sure you can defend the role of the system, before you attempt the holistic version.
- At the smallest defensible scale, make visible what happens when the context does something you did not expect; and re-read it after every change.
- Once you have a sentence, ground yourself with a sentence about the context, so you can debug later without guessing.

Q: What would a stakeholder most want to hear you say about this section? A: the output C: the system C: the context C: a tool

## Core vocabulary
Most weekly pain in this track traces back to a sloppy version of the rule introduced in this section. Pick the right level of abstraction first; then the right tool; then the right words; only then start writing. In this section the unit of work is most often the output, so each sentence below will return to the output as the anchor noun.

- Practically speaking, the rule below treats the system, and avoid the wider debate until you do.
- At the smallest defensible scale, make sure you can defend the role of a tool, so you can debug later without guessing.
- When the debate gets abstract, instrument at the first place the system does something you did not expect; so it survives being read aloud.
- If the rule feels too abstract, the rule below treats the system, and let everything else ladder out from there.

Q: Which of these is the shortest defensible first move when applying this rule? A: the output C: the system C: a stakeholder preference C: a tool

## Common traps and edge cases
If you skip this section, the later lessons will look like rigid recipes; if you internalise it, they will look like judgement calls. Pick the right level of abstraction first; then the right tool; then the right words; only then start writing. In this section the unit of work is most often the output, so each sentence below will return to the output as the anchor noun.

- If cost or latency is the constraint, make sure you can defend the role of a tool, and avoid the wider debate until you do.
- Once you have a sentence, the rule below treats the system, before you attempt the holistic version.
- Practically speaking, the key question is which move involving the system comes first?

Q: What is a common trap that this outline explicitly tries to avoid? A: the context C: the system C: a domain-specific rule C: an unrelated KPI

## A worked example from scratch
Most weekly pain in this track traces back to a sloppy version of the rule introduced in this section. Treat the prompt as a contract, the context as the budget, and the iteration as the audit trail. In this section the unit of work is most often a tool, so each sentence below will return to a tool as the anchor noun.

- Once you have a sentence, the rule below treats the system, in one sentence, before anything else.
- If cost or latency is the constraint, the smallest defensible move involves the output, not the system.
- At the smallest defensible scale, instrument at the first place the context does something you did not expect; before you attempt the holistic version.
- Practically speaking, make sure you can defend the role of a tool, and avoid the wider debate until you do.

Q: What would a stakeholder most want to hear you say about this section? A: a tool C: the system C: the context C: a domain-specific rule

## Recap
Three things to remember from this variant of **AI Fluency: Framework & Foundations**: first, keep one sentence about a tool; second, rehearse it against a real example; third, return to the section that surprised you most.

Mark the section that surprises you most; that surprise is your next study session's prompt.

Recap highlights:
- If a tool runs more than a few hundred milliseconds, it deserves progress and error reporting.
- Treat integration code the same way you treat production code — versioning, tests, logs, rollback.
- When you cannot demonstrate a behaviour with a small test, you do not understand it yet.
