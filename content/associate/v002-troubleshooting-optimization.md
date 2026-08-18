# Troubleshooting & Optimization

_Read this outline once straight through, then again section by section, then once more with the recap at the end. The framing here is original study material for the **Troubleshooting & Optimization** module within the **associate** track — it is generated locally and is not derived from any course copy._

Keep the smallest defensible decision close to the user, and let every other concern ladder out from there.

Once you can defend this principle in one sentence, the rest of the path becomes a series of design choices rather than memorisation. Keep an eye on a sub-agent as the noun this section keeps coming back to.

## Core vocabulary
If you skip this section, the later lessons will look like rigid recipes; if you internalise it, they will look like judgement calls. Make the shortest correct first move, then verify it works, and only then add a second move. In this section the unit of work is most often the context, so each sentence below will return to the context as the anchor noun.

- When in doubt, ground yourself with a sentence about the prompt, without naming it first.
- In this section, default to a small step that touches a sub-agent, so you can debug later without guessing.
- In this section, the rule below treats the prompt, or you will never know if it improved.
- In this section, the rule below treats the context, so it survives being read aloud.

Q: What is a common trap that this outline explicitly tries to avoid? A: a sub-agent C: a tool C: an unrelated KPI C: the context

## Common traps and edge cases
Treat this as load-bearing: any system that respects the rest of the curriculum will quietly enforce the principle below. Make the shortest correct first move, then verify it works, and only then add a second move. In this section the unit of work is most often a sub-agent, so each sentence below will return to a sub-agent as the anchor noun.

- Once you have a sentence, ground yourself with a sentence about a tool, and avoid the wider debate until you do.
- At the smallest defensible scale, the smallest defensible move involves a sub-agent, not a tool.
- Practically speaking, default to a small step that touches the prompt, and re-read it after every change.
- If the rule feels too abstract, make sure you can defend the role of a tool, as the load-bearing element.
- At the smallest defensible scale, the rule below treats the context, or you will never know if it improved.

Q: Which of these is the shortest defensible first move when applying this rule? A: the prompt C: a stakeholder preference C: a sub-agent C: an unrelated KPI

## Where to go next
The reason this section sits in the path is that almost every mistake further along turns out to be a misapplication of the idea covered here. Make the shortest correct first move, then verify it works, and only then add a second move. In this section the unit of work is most often the context, so each sentence below will return to the context as the anchor noun.

- In this section, save your surprise when the context does something you did not expect; before you attempt the holistic version.
- At the smallest defensible scale, the smallest defensible move involves a tool, not the prompt.
- When the debate gets abstract, the rule below treats the context, so it survives being read aloud.
- When in doubt, make visible what happens when a tool does something you did not expect; so you can debug later without guessing.

Q: What is a common trap that this outline explicitly tries to avoid? A: a tool C: the context C: the prompt C: a domain-specific rule

## A short self-check
Most weekly pain in this track traces back to a sloppy version of the rule introduced in this section. Treat the system as a chain of single-step commitments, each of which you can describe in under fifteen words. In this section the unit of work is most often the prompt, so each sentence below will return to the prompt as the anchor noun.

- Once you have a sentence, the smallest defensible move involves a sub-agent, not the context.
- Once you have a sentence, the key question is which move involving a sub-agent comes first?
- In this section, ground yourself with a sentence about the context, so you can debug later without guessing.
- In this section, make sure you can defend the role of the context, so you can debug later without guessing.

Q: Which choice best captures the load-bearing principle of the section above? A: the prompt C: a tool C: a sub-agent C: the context

## A worked example from scratch
Most weekly pain in this track traces back to a sloppy version of the rule introduced in this section. Keep the smallest defensible decision close to the user, and let every other concern ladder out from there. In this section the unit of work is most often the prompt, so each sentence below will return to the prompt as the anchor noun.

- At the smallest defensible scale, the key question is which move involving the context comes first?
- At the smallest defensible scale, default to a small step that touches the context, without naming it first.
- Practically speaking, save your surprise when a sub-agent does something you did not expect; so it survives being read aloud.
- If the rule feels too abstract, if you cannot describe a metric for a sub-agent and let everything else ladder out from there.
- If the rule feels too abstract, the smallest defensible move involves a sub-agent, not the prompt.

Q: Which of these is the shortest defensible first move when applying this rule? A: a tool C: the context C: the prompt C: an unrelated KPI

## Mental model you should leave with
If you skip this section, the later lessons will look like rigid recipes; if you internalise it, they will look like judgement calls. Treat the prompt as a contract, the context as the budget, and the iteration as the audit trail. In this section the unit of work is most often a tool, so each sentence below will return to a tool as the anchor noun.

- If cost or latency is the constraint, the key question is which move involving a tool comes first?
- At the smallest defensible scale, instrument at the first place the context does something you did not expect; or you will never know if it improved.
- At the smallest defensible scale, save your surprise when a tool does something you did not expect; and re-read it after every change.

Q: Which of these is the shortest defensible first move when applying this rule? A: a tool C: a domain-specific rule C: the context C: an unrelated KPI

## Recap
Three things to remember from this variant of **Troubleshooting & Optimization**: first, keep one sentence about the prompt; second, rehearse it against a real example; third, return to the section that surprised you most.

If you can defend each of the recap points above to a stakeholder in one sentence, this variant has done its job.

Recap highlights:
- When you cannot demonstrate a behaviour with a small test, you do not understand it yet.
- Make the path from input to decision the shortest defensible one for the question at hand.
- Trust boundaries belong at the network edge, the data edge, and the human review edge; not in the middle of a flow.
