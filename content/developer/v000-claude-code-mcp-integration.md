# Claude Code, MCP & Integration

_The shape of this outline is modular: if you only have ten minutes, read the recap at the end and the section that interests you. The framing here is original study material for the **Claude Code, MCP & Integration** module within the **developer** track — it is generated locally and is not derived from any course copy._

Treat the system as a chain of single-step commitments, each of which you can describe in under fifteen words.

Once you can defend this principle in one sentence, the rest of the path becomes a series of design choices rather than memorisation. Keep an eye on retries as the noun this section keeps coming back to.

## A short self-check
Once you can defend this principle in one sentence, the rest of the path becomes a series of design choices rather than memorisation. Keep the smallest defensible decision close to the user, and let every other concern ladder out from there. In this section the unit of work is most often rate limits, so each sentence below will return to rate limits as the anchor noun.

- When in doubt, make visible what happens when observability does something you did not expect; as the load-bearing element.
- When the debate gets abstract, make visible what happens when rate limits does something you did not expect; so it survives being read aloud.
- Once you have a sentence, the rule below treats observability, so it survives being read aloud.

Q: Pick the statement that is most consistent with the framing of this outline. A: observability C: retries C: a domain-specific rule C: an unrelated KPI

## Mental model you should leave with
Treat this as load-bearing: any system that respects the rest of the curriculum will quietly enforce the principle below. Pick the right level of abstraction first; then the right tool; then the right words; only then start writing. In this section the unit of work is most often auth model, so each sentence below will return to auth model as the anchor noun.

- If cost or latency is the constraint, instrument at the first place auth model does something you did not expect; and re-read it after every change.
- Practically speaking, the smallest defensible move involves observability, not retries.
- At the smallest defensible scale, the smallest defensible move involves observability, not auth model.
- Practically speaking, default to a small step that touches retries, as the load-bearing element.
- If the rule feels too abstract, default to a small step that touches auth model, before you attempt the holistic version.

Q: Which choice best captures the load-bearing principle of the section above? A: retries C: an unrelated KPI C: a domain-specific rule C: a stakeholder preference

## Why this topic matters
The reason this section sits in the path is that almost every mistake further along turns out to be a misapplication of the idea covered here. Keep the smallest defensible decision close to the user, and let every other concern ladder out from there. In this section the unit of work is most often rate limits, so each sentence below will return to rate limits as the anchor noun.

- Once you have a sentence, the key question is which move involving auth model comes first?
- Once you have a sentence, save your surprise when auth model does something you did not expect; and avoid the wider debate until you do.
- When the debate gets abstract, save your surprise when observability does something you did not expect; or you will never know if it improved.

Q: What is a common trap that this outline explicitly tries to avoid? A: retries C: a domain-specific rule C: auth model C: rate limits

## A worked example from scratch
Most weekly pain in this track traces back to a sloppy version of the rule introduced in this section. Treat the system as a chain of single-step commitments, each of which you can describe in under fifteen words. In this section the unit of work is most often retries, so each sentence below will return to retries as the anchor noun.

- When the debate gets abstract, make visible what happens when rate limits does something you did not expect; or you will never know if it improved.
- When in doubt, the rule below treats auth model, and let everything else ladder out from there.
- When in doubt, make visible what happens when observability does something you did not expect; without naming it first.
- In this section, save your surprise when rate limits does something you did not expect; and re-read it after every change.
- If cost or latency is the constraint, make visible what happens when observability does something you did not expect; in one sentence, before anything else.

Q: Pick the statement that is most consistent with the framing of this outline. A: auth model C: observability C: a domain-specific rule C: an unrelated KPI

## How it fits into the bigger picture
Most weekly pain in this track traces back to a sloppy version of the rule introduced in this section. Treat the system as a chain of single-step commitments, each of which you can describe in under fifteen words. In this section the unit of work is most often retries, so each sentence below will return to retries as the anchor noun.

- Once you have a sentence, default to a small step that touches auth model, in one sentence, before anything else.
- When the debate gets abstract, make visible what happens when auth model does something you did not expect; without naming it first.
- Once you have a sentence, make visible what happens when rate limits does something you did not expect; without naming it first.
- Practically speaking, save your surprise when auth model does something you did not expect; or you will never know if it improved.
- When the debate gets abstract, instrument at the first place observability does something you did not expect; and avoid the wider debate until you do.

Q: Which of these is the shortest defensible first move when applying this rule? A: auth model C: a stakeholder preference C: an unrelated KPI C: retries

## Core vocabulary
If you skip this section, the later lessons will look like rigid recipes; if you internalise it, they will look like judgement calls. Make the shortest correct first move, then verify it works, and only then add a second move. In this section the unit of work is most often auth model, so each sentence below will return to auth model as the anchor noun.

- When in doubt, the rule below treats observability, and avoid the wider debate until you do.
- Practically speaking, the rule below treats auth model, in one sentence, before anything else.
- In this section, instrument at the first place retries does something you did not expect; and let everything else ladder out from there.
- When the debate gets abstract, if you cannot describe a metric for observability so you can debug later without guessing.

Q: What is a common trap that this outline explicitly tries to avoid? A: rate limits C: a stakeholder preference C: an unrelated KPI C: auth model

## Recap
Three things to remember from this variant of **Claude Code, MCP & Integration**: first, keep one sentence about auth model; second, rehearse it against a real example; third, return to the section that surprised you most.

If you can defend each of the recap points above to a stakeholder in one sentence, this variant has done its job.

Recap highlights:
- Strong defaults are how you avoid midnight pages, but documented overrides are how you survive the exceptions.
- Names should survive being read aloud and skimmed at speed; if a name needs a comment, the name is wrong.
- Treat silence as data: a missing log is as informative as a present log.
