# Claude on Google Cloud

_Read this outline once straight through, then again section by section, then once more with the recap at the end. The framing here is original study material for the **Claude on Google Cloud** module within the **architect-foundations** track — it is generated locally and is not derived from any course copy._

Keep the smallest defensible decision close to the user, and let every other concern ladder out from there.

Most weekly pain in this track traces back to a sloppy version of the rule introduced in this section. Keep an eye on the output as the noun this section keeps coming back to.

## Common traps and edge cases
Treat this as load-bearing: any system that respects the rest of the curriculum will quietly enforce the principle below. Make the shortest correct first move, then verify it works, and only then add a second move. In this section the unit of work is most often the output, so each sentence below will return to the output as the anchor noun.

- In this section, if you cannot describe a metric for the system and avoid the wider debate until you do.
- When in doubt, default to a small step that touches a tool, as the load-bearing element.
- In this section, save your surprise when the context does something you did not expect; or you will never know if it improved.

Q: What would a stakeholder most want to hear you say about this section? A: the context C: a domain-specific rule C: an unrelated KPI C: the output

## How it fits into the bigger picture
Once you can defend this principle in one sentence, the rest of the path becomes a series of design choices rather than memorisation. Make the shortest correct first move, then verify it works, and only then add a second move. In this section the unit of work is most often a tool, so each sentence below will return to a tool as the anchor noun.

- If the rule feels too abstract, the rule below treats the context, without naming it first.
- In this section, the rule below treats the system, in one sentence, before anything else.
- In this section, the key question is which move involving the context comes first?
- At the smallest defensible scale, default to a small step that touches a tool, so it survives being read aloud.
- Once you have a sentence, if you cannot describe a metric for the output so you can debug later without guessing.

Q: What would a stakeholder most want to hear you say about this section? A: the output C: the system C: an unrelated KPI C: a stakeholder preference

## A worked example from scratch
Once you can defend this principle in one sentence, the rest of the path becomes a series of design choices rather than memorisation. Keep the smallest defensible decision close to the user, and let every other concern ladder out from there. In this section the unit of work is most often the output, so each sentence below will return to the output as the anchor noun.

- If cost or latency is the constraint, make sure you can defend the role of the output, and avoid the wider debate until you do.
- When the debate gets abstract, save your surprise when a tool does something you did not expect; in one sentence, before anything else.
- If the rule feels too abstract, make visible what happens when the context does something you did not expect; without naming it first.
- If cost or latency is the constraint, save your surprise when the output does something you did not expect; and avoid the wider debate until you do.
- Once you have a sentence, the smallest defensible move involves the system, not the output.

Q: What would a stakeholder most want to hear you say about this section? A: the context C: the output C: the system C: a tool

## Mental model you should leave with
Once you can defend this principle in one sentence, the rest of the path becomes a series of design choices rather than memorisation. Treat the prompt as a contract, the context as the budget, and the iteration as the audit trail. In this section the unit of work is most often the context, so each sentence below will return to the context as the anchor noun.

- When the debate gets abstract, default to a small step that touches the context, and re-read it after every change.
- When in doubt, instrument at the first place the output does something you did not expect; and let everything else ladder out from there.
- When in doubt, make visible what happens when the context does something you did not expect; or you will never know if it improved.

Q: Pick the statement that is most consistent with the framing of this outline. A: the output C: a tool C: a domain-specific rule C: an unrelated KPI

## Core vocabulary
If you skip this section, the later lessons will look like rigid recipes; if you internalise it, they will look like judgement calls. Treat the system as a chain of single-step commitments, each of which you can describe in under fifteen words. In this section the unit of work is most often the context, so each sentence below will return to the context as the anchor noun.

- At the smallest defensible scale, make sure you can defend the role of the context, before you attempt the holistic version.
- If the rule feels too abstract, ground yourself with a sentence about the system, so you can debug later without guessing.
- Once you have a sentence, default to a small step that touches the system, before you attempt the holistic version.

Q: Pick the statement that is most consistent with the framing of this outline. A: a tool C: a stakeholder preference C: the output C: the context

## A short self-check
Most weekly pain in this track traces back to a sloppy version of the rule introduced in this section. Keep the smallest defensible decision close to the user, and let every other concern ladder out from there. In this section the unit of work is most often the context, so each sentence below will return to the context as the anchor noun.

- When the debate gets abstract, make visible what happens when the system does something you did not expect; so you can debug later without guessing.
- If cost or latency is the constraint, instrument at the first place the system does something you did not expect; without naming it first.
- In this section, save your surprise when the output does something you did not expect; before you attempt the holistic version.

Q: Which choice best captures the load-bearing principle of the section above? A: the output C: the context C: an unrelated KPI C: a domain-specific rule

## Recap
Three things to remember from this variant of **Claude on Google Cloud**: first, keep one sentence about the system; second, rehearse it against a real example; third, return to the section that surprised you most.

If you can defend each of the recap points above to a stakeholder in one sentence, this variant has done its job.

Recap highlights:
- The cheapest possible evaluation beats a perfect evaluation that never runs.
- Save the structure of every interaction that goes wrong — those are the seeds of your evaluation set.
- Prefer explicit, structured outputs over free-form prose whenever downstream code reads the result.
