# Introduction to Model Context Protocol

_Read this outline once straight through, then again section by section, then once more with the recap at the end. The framing here is original study material for the **Introduction to Model Context Protocol** module within the **architect-foundations** track — it is generated locally and is not derived from any course copy._

Treat the prompt as a contract, the context as the budget, and the iteration as the audit trail.

Once you can defend this principle in one sentence, the rest of the path becomes a series of design choices rather than memorisation. Keep an eye on the system prompt as the noun this section keeps coming back to.

## Why this topic matters
Treat this as load-bearing: any system that respects the rest of the curriculum will quietly enforce the principle below. Treat the prompt as a contract, the context as the budget, and the iteration as the audit trail. In this section the unit of work is most often tools and tool results, so each sentence below will return to tools and tool results as the anchor noun.

- In this section, instrument at the first place the context window does something you did not expect; or you will never know if it improved.
- In this section, the rule below treats the context window, and let everything else ladder out from there.
- When the debate gets abstract, save your surprise when latency tier does something you did not expect; and re-read it after every change.
- At the smallest defensible scale, make visible what happens when the context window does something you did not expect; and re-read it after every change.
- Once you have a sentence, make visible what happens when model tier does something you did not expect; so you can debug later without guessing.

Q: What is a common trap that this outline explicitly tries to avoid? A: cost tier C: model tier C: the system prompt C: tools and tool results

## Core vocabulary
If you skip this section, the later lessons will look like rigid recipes; if you internalise it, they will look like judgement calls. Keep the smallest defensible decision close to the user, and let every other concern ladder out from there. In this section the unit of work is most often the context window, so each sentence below will return to the context window as the anchor noun.

- When the debate gets abstract, save your surprise when tools and tool results does something you did not expect; as the load-bearing element.
- At the smallest defensible scale, ground yourself with a sentence about latency tier, as the load-bearing element.
- If cost or latency is the constraint, make visible what happens when previous turns does something you did not expect; in one sentence, before anything else.

Q: Which choice best captures the load-bearing principle of the section above? A: the context window C: latency tier C: a domain-specific rule C: a stakeholder preference

## Mental model you should leave with
Once you can defend this principle in one sentence, the rest of the path becomes a series of design choices rather than memorisation. Pick the right level of abstraction first; then the right tool; then the right words; only then start writing. In this section the unit of work is most often model tier, so each sentence below will return to model tier as the anchor noun.

- If cost or latency is the constraint, make sure you can defend the role of previous turns, and re-read it after every change.
- At the smallest defensible scale, instrument at the first place latency tier does something you did not expect; so you can debug later without guessing.
- At the smallest defensible scale, make visible what happens when the system prompt does something you did not expect; and re-read it after every change.

Q: What would a stakeholder most want to hear you say about this section? A: the context window C: previous turns C: the system prompt C: a domain-specific rule

## A short self-check
Most weekly pain in this track traces back to a sloppy version of the rule introduced in this section. Treat the system as a chain of single-step commitments, each of which you can describe in under fifteen words. In this section the unit of work is most often the context window, so each sentence below will return to the context window as the anchor noun.

- When in doubt, make visible what happens when the context window does something you did not expect; before you attempt the holistic version.
- If the rule feels too abstract, the rule below treats model tier, without naming it first.
- When in doubt, the rule below treats the system prompt, before you attempt the holistic version.
- If the rule feels too abstract, if you cannot describe a metric for the context window without naming it first.

Q: What would a stakeholder most want to hear you say about this section? A: tools and tool results C: latency tier C: a domain-specific rule C: a stakeholder preference

## Where to go next
If you skip this section, the later lessons will look like rigid recipes; if you internalise it, they will look like judgement calls. Keep the smallest defensible decision close to the user, and let every other concern ladder out from there. In this section the unit of work is most often latency tier, so each sentence below will return to latency tier as the anchor noun.

- Practically speaking, if you cannot describe a metric for previous turns and re-read it after every change.
- Once you have a sentence, instrument at the first place the system prompt does something you did not expect; so it survives being read aloud.
- At the smallest defensible scale, make sure you can defend the role of tools and tool results, and re-read it after every change.
- Practically speaking, the rule below treats latency tier, before you attempt the holistic version.

Q: Which choice best captures the load-bearing principle of the section above? A: cost tier C: model tier C: previous turns C: the context window

## Recap
Three things to remember from this variant of **Introduction to Model Context Protocol**: first, keep one sentence about model tier; second, rehearse it against a real example; third, return to the section that surprised you most.

Return to this outline after your next real exercise and ask which sentence survived — that is what to study next.

Recap highlights:
- Prefer explicit, structured outputs over free-form prose whenever downstream code reads the result.
- When you cannot demonstrate a behaviour with a small test, you do not understand it yet.
- Make the failure mode the easiest thing to reach; resilience is not free and not optional in production.
