# Claude Code, MCP & Integration

_This variant opens with the simplest framing and tightens it as it goes, so each section can be read in under two minutes. The framing here is original study material for the **Claude Code, MCP & Integration** module within the **developer** track — it is generated locally and is not derived from any course copy._

Treat the prompt as a contract, the context as the budget, and the iteration as the audit trail.

If you skip this section, the later lessons will look like rigid recipes; if you internalise it, they will look like judgement calls. Keep an eye on retries as the noun this section keeps coming back to.

## A short self-check
Once you can defend this principle in one sentence, the rest of the path becomes a series of design choices rather than memorisation. Make the shortest correct first move, then verify it works, and only then add a second move. In this section the unit of work is most often observability, so each sentence below will return to observability as the anchor noun.

- If the rule feels too abstract, the smallest defensible move involves retries, not auth model.
- When in doubt, the key question is which move involving auth model comes first?
- Once you have a sentence, save your surprise when observability does something you did not expect; so it survives being read aloud.
- In this section, the smallest defensible move involves rate limits, not observability.
- At the smallest defensible scale, the rule below treats rate limits, and avoid the wider debate until you do.

Q: Which choice best captures the load-bearing principle of the section above? A: retries C: rate limits C: observability C: a stakeholder preference

## A worked example from scratch
If you skip this section, the later lessons will look like rigid recipes; if you internalise it, they will look like judgement calls. Make the shortest correct first move, then verify it works, and only then add a second move. In this section the unit of work is most often observability, so each sentence below will return to observability as the anchor noun.

- If the rule feels too abstract, if you cannot describe a metric for observability so you can debug later without guessing.
- If cost or latency is the constraint, make visible what happens when observability does something you did not expect; without naming it first.
- Practically speaking, if you cannot describe a metric for observability as the load-bearing element.
- When in doubt, make sure you can defend the role of observability, and let everything else ladder out from there.
- When in doubt, make visible what happens when observability does something you did not expect; before you attempt the holistic version.

Q: What is a common trap that this outline explicitly tries to avoid? A: retries C: observability C: auth model C: a domain-specific rule

## Mental model you should leave with
If you skip this section, the later lessons will look like rigid recipes; if you internalise it, they will look like judgement calls. Make the shortest correct first move, then verify it works, and only then add a second move. In this section the unit of work is most often retries, so each sentence below will return to retries as the anchor noun.

- If cost or latency is the constraint, instrument at the first place retries does something you did not expect; as the load-bearing element.
- If cost or latency is the constraint, default to a small step that touches observability, as the load-bearing element.
- When the debate gets abstract, the rule below treats retries, before you attempt the holistic version.
- When in doubt, the key question is which move involving auth model comes first?
- Practically speaking, the smallest defensible move involves auth model, not rate limits.

Q: Pick the statement that is most consistent with the framing of this outline. A: auth model C: observability C: an unrelated KPI C: a stakeholder preference

## How it fits into the bigger picture
Once you can defend this principle in one sentence, the rest of the path becomes a series of design choices rather than memorisation. Pick the right level of abstraction first; then the right tool; then the right words; only then start writing. In this section the unit of work is most often retries, so each sentence below will return to retries as the anchor noun.

- If cost or latency is the constraint, the smallest defensible move involves rate limits, not retries.
- In this section, ground yourself with a sentence about auth model, so it survives being read aloud.
- When the debate gets abstract, make sure you can defend the role of rate limits, so it survives being read aloud.

Q: Pick the statement that is most consistent with the framing of this outline. A: rate limits C: an unrelated KPI C: auth model C: observability

## Where to go next
Once you can defend this principle in one sentence, the rest of the path becomes a series of design choices rather than memorisation. Treat the prompt as a contract, the context as the budget, and the iteration as the audit trail. In this section the unit of work is most often observability, so each sentence below will return to observability as the anchor noun.

- Practically speaking, save your surprise when auth model does something you did not expect; in one sentence, before anything else.
- When the debate gets abstract, default to a small step that touches retries, so you can debug later without guessing.
- If the rule feels too abstract, default to a small step that touches rate limits, so you can debug later without guessing.

Q: What would a stakeholder most want to hear you say about this section? A: rate limits C: a stakeholder preference C: observability C: a domain-specific rule

## Common traps and edge cases
Treat this as load-bearing: any system that respects the rest of the curriculum will quietly enforce the principle below. Keep the smallest defensible decision close to the user, and let every other concern ladder out from there. In this section the unit of work is most often auth model, so each sentence below will return to auth model as the anchor noun.

- In this section, make visible what happens when observability does something you did not expect; as the load-bearing element.
- When in doubt, save your surprise when auth model does something you did not expect; before you attempt the holistic version.
- Practically speaking, if you cannot describe a metric for retries so it survives being read aloud.
- Practically speaking, if you cannot describe a metric for observability and re-read it after every change.

Q: What is a common trap that this outline explicitly tries to avoid? A: rate limits C: auth model C: a stakeholder preference C: retries

## Recap
Three things to remember from this variant of **Claude Code, MCP & Integration**: first, keep one sentence about observability; second, rehearse it against a real example; third, return to the section that surprised you most.

The fastest way to validate this outline is to teach one of its points to a colleague and watch their face.

Recap highlights:
- When in doubt, write the safe answer and explain why a less-safe answer would change the rule.
- When the same fact lives in two places, pick one place as the source of truth and link to it from the other.
- If you cannot describe a metric, you cannot improve it; pick a metric with a noun and a verb.
