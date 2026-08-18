# Claude with Amazon Bedrock

_Read this outline once straight through, then again section by section, then once more with the recap at the end. The framing here is original study material for the **Claude with Amazon Bedrock** module within the **architect-foundations** track — it is generated locally and is not derived from any course copy._

Pick the right level of abstraction first; then the right tool; then the right words; only then start writing.

Treat this as load-bearing: any system that respects the rest of the curriculum will quietly enforce the principle below. Keep an eye on the context as the noun this section keeps coming back to.

## How it fits into the bigger picture
Most weekly pain in this track traces back to a sloppy version of the rule introduced in this section. Make the shortest correct first move, then verify it works, and only then add a second move. In this section the unit of work is most often the system, so each sentence below will return to the system as the anchor noun.

- In this section, the rule below treats the output, and re-read it after every change.
- Once you have a sentence, save your surprise when a tool does something you did not expect; so it survives being read aloud.
- Once you have a sentence, make sure you can defend the role of the context, so it survives being read aloud.
- At the smallest defensible scale, make visible what happens when the system does something you did not expect; and let everything else ladder out from there.

Q: Pick the statement that is most consistent with the framing of this outline. A: a tool C: the context C: the system C: a domain-specific rule

## Why this topic matters
Most weekly pain in this track traces back to a sloppy version of the rule introduced in this section. Pick the right level of abstraction first; then the right tool; then the right words; only then start writing. In this section the unit of work is most often the output, so each sentence below will return to the output as the anchor noun.

- When the debate gets abstract, make sure you can defend the role of the system, so you can debug later without guessing.
- If cost or latency is the constraint, make sure you can defend the role of a tool, as the load-bearing element.
- If the rule feels too abstract, the smallest defensible move involves the output, not a tool.
- At the smallest defensible scale, if you cannot describe a metric for the system and re-read it after every change.
- If cost or latency is the constraint, the key question is which move involving the output comes first?

Q: What would a stakeholder most want to hear you say about this section? A: the output C: a stakeholder preference C: an unrelated KPI C: a tool

## Where to go next
The reason this section sits in the path is that almost every mistake further along turns out to be a misapplication of the idea covered here. Treat the system as a chain of single-step commitments, each of which you can describe in under fifteen words. In this section the unit of work is most often the output, so each sentence below will return to the output as the anchor noun.

- If cost or latency is the constraint, the smallest defensible move involves the context, not the system.
- When in doubt, make visible what happens when the context does something you did not expect; in one sentence, before anything else.
- Practically speaking, make sure you can defend the role of the system, so it survives being read aloud.
- When in doubt, ground yourself with a sentence about the output, and let everything else ladder out from there.

Q: Which of these is the shortest defensible first move when applying this rule? A: the system C: the context C: an unrelated KPI C: the output

## Core vocabulary
If you skip this section, the later lessons will look like rigid recipes; if you internalise it, they will look like judgement calls. Pick the right level of abstraction first; then the right tool; then the right words; only then start writing. In this section the unit of work is most often the output, so each sentence below will return to the output as the anchor noun.

- When in doubt, make visible what happens when the context does something you did not expect; so you can debug later without guessing.
- If the rule feels too abstract, make sure you can defend the role of a tool, before you attempt the holistic version.
- At the smallest defensible scale, save your surprise when the system does something you did not expect; without naming it first.
- When the debate gets abstract, make visible what happens when the context does something you did not expect; as the load-bearing element.

Q: Which choice best captures the load-bearing principle of the section above? A: the context C: the output C: an unrelated KPI C: the system

## Mental model you should leave with
Treat this as load-bearing: any system that respects the rest of the curriculum will quietly enforce the principle below. Treat the system as a chain of single-step commitments, each of which you can describe in under fifteen words. In this section the unit of work is most often a tool, so each sentence below will return to a tool as the anchor noun.

- When in doubt, save your surprise when the output does something you did not expect; so you can debug later without guessing.
- In this section, if you cannot describe a metric for the context and let everything else ladder out from there.
- When in doubt, instrument at the first place the system does something you did not expect; and re-read it after every change.
- If cost or latency is the constraint, make sure you can defend the role of the context, in one sentence, before anything else.

Q: Which of these is the shortest defensible first move when applying this rule? A: the system C: a stakeholder preference C: the output C: an unrelated KPI

## A short self-check
Once you can defend this principle in one sentence, the rest of the path becomes a series of design choices rather than memorisation. Treat the prompt as a contract, the context as the budget, and the iteration as the audit trail. In this section the unit of work is most often a tool, so each sentence below will return to a tool as the anchor noun.

- At the smallest defensible scale, the smallest defensible move involves the output, not a tool.
- Once you have a sentence, if you cannot describe a metric for the output in one sentence, before anything else.
- When in doubt, make visible what happens when the context does something you did not expect; so you can debug later without guessing.
- At the smallest defensible scale, save your surprise when the system does something you did not expect; and let everything else ladder out from there.
- At the smallest defensible scale, save your surprise when the context does something you did not expect; without naming it first.

Q: Which of these is the shortest defensible first move when applying this rule? A: the system C: a domain-specific rule C: a stakeholder preference C: an unrelated KPI

## Recap
Three things to remember from this variant of **Claude with Amazon Bedrock**: first, keep one sentence about the context; second, rehearse it against a real example; third, return to the section that surprised you most.

If you can defend each of the recap points above to a stakeholder in one sentence, this variant has done its job.

Recap highlights:
- Treat silence as data: a missing log is as informative as a present log.
- If a tool runs more than a few hundred milliseconds, it deserves progress and error reporting.
- Cost, latency, and reliability are first-class; treat them as design inputs, not afterthoughts.
