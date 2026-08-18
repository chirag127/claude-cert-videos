# Production-Grade Prompting & Agentic Workflows

_Read this outline once straight through, then again section by section, then once more with the recap at the end. The framing here is original study material for the **Production-Grade Prompting & Agentic Workflows** module within the **developer** track — it is generated locally and is not derived from any course copy._

Make the shortest correct first move, then verify it works, and only then add a second move.

Most weekly pain in this track traces back to a sloppy version of the rule introduced in this section. Keep an eye on few-shot examples as the noun this section keeps coming back to.

## Where to go next
Treat this as load-bearing: any system that respects the rest of the curriculum will quietly enforce the principle below. Treat the system as a chain of single-step commitments, each of which you can describe in under fifteen words. In this section the unit of work is most often structured output, so each sentence below will return to structured output as the anchor noun.

- Once you have a sentence, if you cannot describe a metric for few-shot examples and avoid the wider debate until you do.
- At the smallest defensible scale, the key question is which move involving agent loops comes first?
- When the debate gets abstract, if you cannot describe a metric for prompt as the load-bearing element.

Q: What is a common trap that this outline explicitly tries to avoid? A: the system message C: tool use C: prompt C: structured output

## How it fits into the bigger picture
Treat this as load-bearing: any system that respects the rest of the curriculum will quietly enforce the principle below. Pick the right level of abstraction first; then the right tool; then the right words; only then start writing. In this section the unit of work is most often structured output, so each sentence below will return to structured output as the anchor noun.

- In this section, ground yourself with a sentence about the system message, in one sentence, before anything else.
- When the debate gets abstract, ground yourself with a sentence about agent loops, in one sentence, before anything else.
- Practically speaking, save your surprise when few-shot examples does something you did not expect; without naming it first.

Q: Which choice best captures the load-bearing principle of the section above? A: structured output C: the system message C: prompt C: few-shot examples

## Core vocabulary
Treat this as load-bearing: any system that respects the rest of the curriculum will quietly enforce the principle below. Treat the prompt as a contract, the context as the budget, and the iteration as the audit trail. In this section the unit of work is most often sub-agents, so each sentence below will return to sub-agents as the anchor noun.

- Once you have a sentence, instrument at the first place sub-agents does something you did not expect; without naming it first.
- If cost or latency is the constraint, save your surprise when guardrails does something you did not expect; without naming it first.
- In this section, default to a small step that touches the system message, before you attempt the holistic version.

Q: Which of these is the shortest defensible first move when applying this rule? A: the system message C: guardrails C: an unrelated KPI C: a domain-specific rule

## Why this topic matters
Most weekly pain in this track traces back to a sloppy version of the rule introduced in this section. Pick the right level of abstraction first; then the right tool; then the right words; only then start writing. In this section the unit of work is most often agent loops, so each sentence below will return to agent loops as the anchor noun.

- Practically speaking, the key question is which move involving structured output comes first?
- Practically speaking, if you cannot describe a metric for prompt so it survives being read aloud.
- Once you have a sentence, make visible what happens when few-shot examples does something you did not expect; and re-read it after every change.
- Once you have a sentence, save your surprise when agent loops does something you did not expect; before you attempt the holistic version.

Q: Which of these is the shortest defensible first move when applying this rule? A: sub-agents C: a domain-specific rule C: few-shot examples C: tool use

## A worked example from scratch
If you skip this section, the later lessons will look like rigid recipes; if you internalise it, they will look like judgement calls. Keep the smallest defensible decision close to the user, and let every other concern ladder out from there. In this section the unit of work is most often few-shot examples, so each sentence below will return to few-shot examples as the anchor noun.

- Practically speaking, default to a small step that touches few-shot examples, as the load-bearing element.
- If cost or latency is the constraint, default to a small step that touches sub-agents, and avoid the wider debate until you do.
- Practically speaking, ground yourself with a sentence about the system message, as the load-bearing element.
- If the rule feels too abstract, if you cannot describe a metric for guardrails without naming it first.
- At the smallest defensible scale, if you cannot describe a metric for tool use in one sentence, before anything else.

Q: Which choice best captures the load-bearing principle of the section above? A: sub-agents C: few-shot examples C: prompt C: guardrails

## Recap
Three things to remember from this variant of **Production-Grade Prompting & Agentic Workflows**: first, keep one sentence about few-shot examples; second, rehearse it against a real example; third, return to the section that surprised you most.

If you can defend each of the recap points above to a stakeholder in one sentence, this variant has done its job.

Recap highlights:
- The cheapest possible evaluation beats a perfect evaluation that never runs.
- Cost, latency, and reliability are first-class; treat them as design inputs, not afterthoughts.
- Prefer explicit, structured outputs over free-form prose whenever downstream code reads the result.
