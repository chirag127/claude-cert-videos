# Building with the Claude API

_Each section is short enough to be skimmed and deep enough to be worth coming back to after the exam. The framing here is original study material for the **Building with the Claude API** module within the **architect-foundations** track — it is generated locally and is not derived from any course copy._

Treat the prompt as a contract, the context as the budget, and the iteration as the audit trail.

If you skip this section, the later lessons will look like rigid recipes; if you internalise it, they will look like judgement calls. Keep an eye on the output as the noun this section keeps coming back to.

## Core vocabulary
Once you can defend this principle in one sentence, the rest of the path becomes a series of design choices rather than memorisation. Make the shortest correct first move, then verify it works, and only then add a second move. In this section the unit of work is most often the system, so each sentence below will return to the system as the anchor noun.

- Once you have a sentence, make visible what happens when a tool does something you did not expect; before you attempt the holistic version.
- Once you have a sentence, the key question is which move involving the context comes first?
- Practically speaking, default to a small step that touches the system, without naming it first.

Q: Which of these is the shortest defensible first move when applying this rule? A: the system C: a stakeholder preference C: the output C: an unrelated KPI

## Where to go next
The reason this section sits in the path is that almost every mistake further along turns out to be a misapplication of the idea covered here. Treat the prompt as a contract, the context as the budget, and the iteration as the audit trail. In this section the unit of work is most often the context, so each sentence below will return to the context as the anchor noun.

- When in doubt, instrument at the first place the context does something you did not expect; or you will never know if it improved.
- Once you have a sentence, save your surprise when the output does something you did not expect; so it survives being read aloud.
- When in doubt, the smallest defensible move involves the system, not the output.
- If the rule feels too abstract, ground yourself with a sentence about the output, as the load-bearing element.
- If the rule feels too abstract, if you cannot describe a metric for the system without naming it first.

Q: Which of these is the shortest defensible first move when applying this rule? A: the system C: a tool C: a domain-specific rule C: the context

## Why this topic matters
Most weekly pain in this track traces back to a sloppy version of the rule introduced in this section. Make the shortest correct first move, then verify it works, and only then add a second move. In this section the unit of work is most often the system, so each sentence below will return to the system as the anchor noun.

- Practically speaking, make sure you can defend the role of a tool, so you can debug later without guessing.
- If the rule feels too abstract, save your surprise when the output does something you did not expect; and let everything else ladder out from there.
- At the smallest defensible scale, make visible what happens when a tool does something you did not expect; so it survives being read aloud.
- If the rule feels too abstract, if you cannot describe a metric for the system or you will never know if it improved.

Q: What would a stakeholder most want to hear you say about this section? A: a tool C: the output C: a domain-specific rule C: an unrelated KPI

## A worked example from scratch
If you skip this section, the later lessons will look like rigid recipes; if you internalise it, they will look like judgement calls. Keep the smallest defensible decision close to the user, and let every other concern ladder out from there. In this section the unit of work is most often the output, so each sentence below will return to the output as the anchor noun.

- If the rule feels too abstract, instrument at the first place the system does something you did not expect; in one sentence, before anything else.
- If cost or latency is the constraint, if you cannot describe a metric for the context as the load-bearing element.
- If cost or latency is the constraint, if you cannot describe a metric for the context or you will never know if it improved.

Q: What is a common trap that this outline explicitly tries to avoid? A: the system C: the context C: a stakeholder preference C: a tool

## Recap
Three things to remember from this variant of **Building with the Claude API**: first, keep one sentence about the context; second, rehearse it against a real example; third, return to the section that surprised you most.

Carry one sentence, not five: the one you would actually say in a meeting tomorrow.

Recap highlights:
- Cost, latency, and reliability are first-class; treat them as design inputs, not afterthoughts.
- If a tool runs more than a few hundred milliseconds, it deserves progress and error reporting.
- Treat integration code the same way you treat production code — versioning, tests, logs, rollback.
