# Prompting & Task Execution

_Each section is short enough to be skimmed and deep enough to be worth coming back to after the exam. The framing here is original study material for the **Prompting & Task Execution** module within the **associate** track — it is generated locally and is not derived from any course copy._

Treat the system as a chain of single-step commitments, each of which you can describe in under fifteen words.

If you skip this section, the later lessons will look like rigid recipes; if you internalise it, they will look like judgement calls. Keep an eye on structured output as the noun this section keeps coming back to.

## Core vocabulary
Treat this as load-bearing: any system that respects the rest of the curriculum will quietly enforce the principle below. Treat the prompt as a contract, the context as the budget, and the iteration as the audit trail. In this section the unit of work is most often structured output, so each sentence below will return to structured output as the anchor noun.

- If the rule feels too abstract, make sure you can defend the role of few-shot examples, and let everything else ladder out from there.
- Once you have a sentence, ground yourself with a sentence about structured output, in one sentence, before anything else.
- At the smallest defensible scale, the rule below treats prompt, without naming it first.
- At the smallest defensible scale, make visible what happens when structured output does something you did not expect; in one sentence, before anything else.
- Once you have a sentence, make sure you can defend the role of the system message, in one sentence, before anything else.

Q: What is a common trap that this outline explicitly tries to avoid? A: few-shot examples C: structured output C: prompt C: the system message

## Where to go next
Once you can defend this principle in one sentence, the rest of the path becomes a series of design choices rather than memorisation. Treat the system as a chain of single-step commitments, each of which you can describe in under fifteen words. In this section the unit of work is most often structured output, so each sentence below will return to structured output as the anchor noun.

- At the smallest defensible scale, make visible what happens when the system message does something you did not expect; and re-read it after every change.
- If cost or latency is the constraint, ground yourself with a sentence about few-shot examples, or you will never know if it improved.
- If the rule feels too abstract, the smallest defensible move involves structured output, not prompt.
- When the debate gets abstract, the smallest defensible move involves the system message, not structured output.

Q: What is a common trap that this outline explicitly tries to avoid? A: few-shot examples C: the system message C: structured output C: prompt

## How it fits into the bigger picture
Most weekly pain in this track traces back to a sloppy version of the rule introduced in this section. Keep the smallest defensible decision close to the user, and let every other concern ladder out from there. In this section the unit of work is most often few-shot examples, so each sentence below will return to few-shot examples as the anchor noun.

- If the rule feels too abstract, save your surprise when structured output does something you did not expect; and let everything else ladder out from there.
- Practically speaking, instrument at the first place structured output does something you did not expect; and avoid the wider debate until you do.
- Practically speaking, save your surprise when the system message does something you did not expect; as the load-bearing element.
- If the rule feels too abstract, instrument at the first place prompt does something you did not expect; in one sentence, before anything else.

Q: Which of these is the shortest defensible first move when applying this rule? A: prompt C: the system message C: a domain-specific rule C: structured output

## A worked example from scratch
Once you can defend this principle in one sentence, the rest of the path becomes a series of design choices rather than memorisation. Make the shortest correct first move, then verify it works, and only then add a second move. In this section the unit of work is most often few-shot examples, so each sentence below will return to few-shot examples as the anchor noun.

- When the debate gets abstract, default to a small step that touches few-shot examples, in one sentence, before anything else.
- Once you have a sentence, the key question is which move involving the system message comes first?
- If cost or latency is the constraint, the smallest defensible move involves prompt, not the system message.
- At the smallest defensible scale, the smallest defensible move involves few-shot examples, not the system message.

Q: Pick the statement that is most consistent with the framing of this outline. A: prompt C: an unrelated KPI C: the system message C: structured output

## Common traps and edge cases
The reason this section sits in the path is that almost every mistake further along turns out to be a misapplication of the idea covered here. Make the shortest correct first move, then verify it works, and only then add a second move. In this section the unit of work is most often structured output, so each sentence below will return to structured output as the anchor noun.

- At the smallest defensible scale, make sure you can defend the role of prompt, and re-read it after every change.
- Once you have a sentence, ground yourself with a sentence about prompt, or you will never know if it improved.
- Practically speaking, the rule below treats prompt, without naming it first.

Q: Pick the statement that is most consistent with the framing of this outline. A: the system message C: a stakeholder preference C: few-shot examples C: a domain-specific rule

## Recap
Three things to remember from this variant of **Prompting & Task Execution**: first, keep one sentence about few-shot examples; second, rehearse it against a real example; third, return to the section that surprised you most.

The fastest way to validate this outline is to teach one of its points to a colleague and watch their face.

Recap highlights:
- Make the path from input to decision the shortest defensible one for the question at hand.
- Names should survive being read aloud and skimmed at speed; if a name needs a comment, the name is wrong.
- Treat integration code the same way you treat production code — versioning, tests, logs, rollback.
