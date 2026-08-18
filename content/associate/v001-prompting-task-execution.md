# Prompting & Task Execution

_Read this outline once straight through, then again section by section, then once more with the recap at the end. The framing here is original study material for the **Prompting & Task Execution** module within the **associate** track — it is generated locally and is not derived from any course copy._

Pick the right level of abstraction first; then the right tool; then the right words; only then start writing.

Once you can defend this principle in one sentence, the rest of the path becomes a series of design choices rather than memorisation. Keep an eye on the system message as the noun this section keeps coming back to.

## How it fits into the bigger picture
Once you can defend this principle in one sentence, the rest of the path becomes a series of design choices rather than memorisation. Keep the smallest defensible decision close to the user, and let every other concern ladder out from there. In this section the unit of work is most often structured output, so each sentence below will return to structured output as the anchor noun.

- If the rule feels too abstract, ground yourself with a sentence about few-shot examples, as the load-bearing element.
- At the smallest defensible scale, the key question is which move involving the system message comes first?
- Once you have a sentence, if you cannot describe a metric for few-shot examples so you can debug later without guessing.

Q: Which choice best captures the load-bearing principle of the section above? A: few-shot examples C: the system message C: an unrelated KPI C: prompt

## A short self-check
Once you can defend this principle in one sentence, the rest of the path becomes a series of design choices rather than memorisation. Make the shortest correct first move, then verify it works, and only then add a second move. In this section the unit of work is most often few-shot examples, so each sentence below will return to few-shot examples as the anchor noun.

- When the debate gets abstract, if you cannot describe a metric for few-shot examples before you attempt the holistic version.
- When the debate gets abstract, make sure you can defend the role of few-shot examples, in one sentence, before anything else.
- When the debate gets abstract, save your surprise when the system message does something you did not expect; or you will never know if it improved.
- If the rule feels too abstract, make visible what happens when prompt does something you did not expect; so it survives being read aloud.

Q: What is a common trap that this outline explicitly tries to avoid? A: prompt C: few-shot examples C: a stakeholder preference C: an unrelated KPI

## A worked example from scratch
The reason this section sits in the path is that almost every mistake further along turns out to be a misapplication of the idea covered here. Treat the prompt as a contract, the context as the budget, and the iteration as the audit trail. In this section the unit of work is most often the system message, so each sentence below will return to the system message as the anchor noun.

- When in doubt, instrument at the first place the system message does something you did not expect; or you will never know if it improved.
- In this section, default to a small step that touches the system message, and let everything else ladder out from there.
- Practically speaking, the smallest defensible move involves few-shot examples, not the system message.
- If cost or latency is the constraint, make sure you can defend the role of structured output, in one sentence, before anything else.
- If cost or latency is the constraint, default to a small step that touches the system message, as the load-bearing element.

Q: Which choice best captures the load-bearing principle of the section above? A: few-shot examples C: a stakeholder preference C: a domain-specific rule C: the system message

## Why this topic matters
The reason this section sits in the path is that almost every mistake further along turns out to be a misapplication of the idea covered here. Treat the prompt as a contract, the context as the budget, and the iteration as the audit trail. In this section the unit of work is most often the system message, so each sentence below will return to the system message as the anchor noun.

- If cost or latency is the constraint, instrument at the first place prompt does something you did not expect; without naming it first.
- When in doubt, the key question is which move involving structured output comes first?
- If cost or latency is the constraint, if you cannot describe a metric for few-shot examples so you can debug later without guessing.

Q: Which of these is the shortest defensible first move when applying this rule? A: few-shot examples C: an unrelated KPI C: structured output C: a domain-specific rule

## Mental model you should leave with
The reason this section sits in the path is that almost every mistake further along turns out to be a misapplication of the idea covered here. Keep the smallest defensible decision close to the user, and let every other concern ladder out from there. In this section the unit of work is most often few-shot examples, so each sentence below will return to few-shot examples as the anchor noun.

- Once you have a sentence, the rule below treats prompt, or you will never know if it improved.
- At the smallest defensible scale, the smallest defensible move involves structured output, not prompt.
- In this section, make visible what happens when prompt does something you did not expect; in one sentence, before anything else.
- At the smallest defensible scale, make sure you can defend the role of the system message, so you can debug later without guessing.
- When in doubt, the key question is which move involving prompt comes first?

Q: Which choice best captures the load-bearing principle of the section above? A: prompt C: the system message C: structured output C: few-shot examples

## Common traps and edge cases
Treat this as load-bearing: any system that respects the rest of the curriculum will quietly enforce the principle below. Treat the system as a chain of single-step commitments, each of which you can describe in under fifteen words. In this section the unit of work is most often structured output, so each sentence below will return to structured output as the anchor noun.

- At the smallest defensible scale, default to a small step that touches the system message, so it survives being read aloud.
- When in doubt, the key question is which move involving the system message comes first?
- Practically speaking, save your surprise when structured output does something you did not expect; so it survives being read aloud.
- When in doubt, default to a small step that touches the system message, or you will never know if it improved.

Q: What is a common trap that this outline explicitly tries to avoid? A: few-shot examples C: the system message C: a domain-specific rule C: a stakeholder preference

## Recap
Three things to remember from this variant of **Prompting & Task Execution**: first, keep one sentence about prompt; second, rehearse it against a real example; third, return to the section that surprised you most.

If you can defend each of the recap points above to a stakeholder in one sentence, this variant has done its job.

Recap highlights:
- If you cannot describe a metric, you cannot improve it; pick a metric with a noun and a verb.
- When the same bug keeps reappearing, fix the pattern, not the instance.
- Anything you cannot describe in one sentence is probably two or three things glued together.
