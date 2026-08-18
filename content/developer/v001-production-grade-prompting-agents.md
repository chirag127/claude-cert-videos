# Production-Grade Prompting & Agentic Workflows

_This variant opens with the simplest framing and tightens it as it goes, so each section can be read in under two minutes. The framing here is original study material for the **Production-Grade Prompting & Agentic Workflows** module within the **developer** track — it is generated locally and is not derived from any course copy._

Keep the smallest defensible decision close to the user, and let every other concern ladder out from there.

Once you can defend this principle in one sentence, the rest of the path becomes a series of design choices rather than memorisation. Keep an eye on sub-agents as the noun this section keeps coming back to.

## Why this topic matters
The reason this section sits in the path is that almost every mistake further along turns out to be a misapplication of the idea covered here. Treat the prompt as a contract, the context as the budget, and the iteration as the audit trail. In this section the unit of work is most often few-shot examples, so each sentence below will return to few-shot examples as the anchor noun.

- Practically speaking, save your surprise when tool use does something you did not expect; so it survives being read aloud.
- If the rule feels too abstract, the key question is which move involving agent loops comes first?
- In this section, save your surprise when prompt does something you did not expect; and re-read it after every change.
- In this section, make sure you can defend the role of the system message, before you attempt the holistic version.

Q: Which of these is the shortest defensible first move when applying this rule? A: guardrails C: a stakeholder preference C: prompt C: structured output

## A worked example from scratch
Once you can defend this principle in one sentence, the rest of the path becomes a series of design choices rather than memorisation. Keep the smallest defensible decision close to the user, and let every other concern ladder out from there. In this section the unit of work is most often prompt, so each sentence below will return to prompt as the anchor noun.

- When in doubt, if you cannot describe a metric for prompt without naming it first.
- If the rule feels too abstract, instrument at the first place structured output does something you did not expect; and let everything else ladder out from there.
- If the rule feels too abstract, ground yourself with a sentence about structured output, and avoid the wider debate until you do.

Q: Which of these is the shortest defensible first move when applying this rule? A: guardrails C: agent loops C: a domain-specific rule C: few-shot examples

## Core vocabulary
Most weekly pain in this track traces back to a sloppy version of the rule introduced in this section. Treat the system as a chain of single-step commitments, each of which you can describe in under fifteen words. In this section the unit of work is most often guardrails, so each sentence below will return to guardrails as the anchor noun.

- When in doubt, make sure you can defend the role of the system message, and re-read it after every change.
- In this section, make visible what happens when prompt does something you did not expect; in one sentence, before anything else.
- If the rule feels too abstract, the key question is which move involving the system message comes first?
- When in doubt, the smallest defensible move involves structured output, not prompt.

Q: Pick the statement that is most consistent with the framing of this outline. A: guardrails C: structured output C: sub-agents C: prompt

## Common traps and edge cases
If you skip this section, the later lessons will look like rigid recipes; if you internalise it, they will look like judgement calls. Keep the smallest defensible decision close to the user, and let every other concern ladder out from there. In this section the unit of work is most often sub-agents, so each sentence below will return to sub-agents as the anchor noun.

- Practically speaking, make sure you can defend the role of prompt, as the load-bearing element.
- If the rule feels too abstract, instrument at the first place guardrails does something you did not expect; so you can debug later without guessing.
- If the rule feels too abstract, the smallest defensible move involves agent loops, not guardrails.
- In this section, make visible what happens when sub-agents does something you did not expect; and avoid the wider debate until you do.

Q: Which choice best captures the load-bearing principle of the section above? A: structured output C: agent loops C: sub-agents C: few-shot examples

## Where to go next
If you skip this section, the later lessons will look like rigid recipes; if you internalise it, they will look like judgement calls. Treat the system as a chain of single-step commitments, each of which you can describe in under fifteen words. In this section the unit of work is most often tool use, so each sentence below will return to tool use as the anchor noun.

- When in doubt, ground yourself with a sentence about tool use, and re-read it after every change.
- If cost or latency is the constraint, make visible what happens when agent loops does something you did not expect; as the load-bearing element.
- Once you have a sentence, if you cannot describe a metric for the system message and avoid the wider debate until you do.
- In this section, default to a small step that touches few-shot examples, so you can debug later without guessing.

Q: Which choice best captures the load-bearing principle of the section above? A: the system message C: a stakeholder preference C: agent loops C: tool use

## Recap
Three things to remember from this variant of **Production-Grade Prompting & Agentic Workflows**: first, keep one sentence about the system message; second, rehearse it against a real example; third, return to the section that surprised you most.

Carry one sentence, not five: the one you would actually say in a meeting tomorrow.

Recap highlights:
- The cheapest possible evaluation beats a perfect evaluation that never runs.
- Lead with the user's question and the smallest unit of value they need back.
- Anything you cannot describe in one sentence is probably two or three things glued together.
