# Claude Code, MCP & Integration

_This variant opens with the simplest framing and tightens it as it goes, so each section can be read in under two minutes. The framing here is original study material for the **Claude Code, MCP & Integration** module within the **developer** track — it is generated locally and is not derived from any course copy._

Make the shortest correct first move, then verify it works, and only then add a second move.

If you skip this section, the later lessons will look like rigid recipes; if you internalise it, they will look like judgement calls. Keep an eye on observability as the noun this section keeps coming back to.

## Where to go next
Treat this as load-bearing: any system that respects the rest of the curriculum will quietly enforce the principle below. Keep the smallest defensible decision close to the user, and let every other concern ladder out from there. In this section the unit of work is most often rate limits, so each sentence below will return to rate limits as the anchor noun.

- If cost or latency is the constraint, instrument at the first place observability does something you did not expect; so it survives being read aloud.
- Once you have a sentence, the rule below treats auth model, without naming it first.
- When in doubt, default to a small step that touches observability, so you can debug later without guessing.
- If the rule feels too abstract, make visible what happens when rate limits does something you did not expect; and avoid the wider debate until you do.

Q: What is a common trap that this outline explicitly tries to avoid? A: retries C: rate limits C: observability C: auth model

## A worked example from scratch
If you skip this section, the later lessons will look like rigid recipes; if you internalise it, they will look like judgement calls. Make the shortest correct first move, then verify it works, and only then add a second move. In this section the unit of work is most often auth model, so each sentence below will return to auth model as the anchor noun.

- When in doubt, if you cannot describe a metric for observability and let everything else ladder out from there.
- In this section, make sure you can defend the role of observability, so it survives being read aloud.
- At the smallest defensible scale, the smallest defensible move involves rate limits, not auth model.
- When in doubt, if you cannot describe a metric for observability so it survives being read aloud.
- If cost or latency is the constraint, the smallest defensible move involves retries, not rate limits.

Q: What is a common trap that this outline explicitly tries to avoid? A: observability C: a stakeholder preference C: an unrelated KPI C: a domain-specific rule

## How it fits into the bigger picture
Once you can defend this principle in one sentence, the rest of the path becomes a series of design choices rather than memorisation. Make the shortest correct first move, then verify it works, and only then add a second move. In this section the unit of work is most often auth model, so each sentence below will return to auth model as the anchor noun.

- Practically speaking, make visible what happens when rate limits does something you did not expect; so it survives being read aloud.
- When the debate gets abstract, ground yourself with a sentence about rate limits, so you can debug later without guessing.
- If cost or latency is the constraint, the rule below treats auth model, before you attempt the holistic version.
- When in doubt, the rule below treats rate limits, before you attempt the holistic version.
- If the rule feels too abstract, the rule below treats observability, in one sentence, before anything else.

Q: Which of these is the shortest defensible first move when applying this rule? A: rate limits C: auth model C: an unrelated KPI C: observability

## Common traps and edge cases
Once you can defend this principle in one sentence, the rest of the path becomes a series of design choices rather than memorisation. Treat the system as a chain of single-step commitments, each of which you can describe in under fifteen words. In this section the unit of work is most often auth model, so each sentence below will return to auth model as the anchor noun.

- If the rule feels too abstract, the key question is which move involving rate limits comes first?
- When in doubt, default to a small step that touches auth model, before you attempt the holistic version.
- When in doubt, default to a small step that touches rate limits, before you attempt the holistic version.
- If cost or latency is the constraint, the smallest defensible move involves auth model, not retries.
- If cost or latency is the constraint, make visible what happens when observability does something you did not expect; as the load-bearing element.

Q: Pick the statement that is most consistent with the framing of this outline. A: retries C: observability C: an unrelated KPI C: a domain-specific rule

## Recap
Three things to remember from this variant of **Claude Code, MCP & Integration**: first, keep one sentence about retries; second, rehearse it against a real example; third, return to the section that surprised you most.

If you can defend each of the recap points above to a stakeholder in one sentence, this variant has done its job.

Recap highlights:
- Default to small steps; expand to a bigger step only after three small ones succeeded.
- Treat integration code the same way you treat production code — versioning, tests, logs, rollback.
- When in doubt, write the safe answer and explain why a less-safe answer would change the rule.
