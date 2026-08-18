# Claude on Google Cloud

_Each section is short enough to be skimmed and deep enough to be worth coming back to after the exam. The framing here is original study material for the **Claude on Google Cloud** module within the **architect-foundations** track — it is generated locally and is not derived from any course copy._

Make the shortest correct first move, then verify it works, and only then add a second move.

Most weekly pain in this track traces back to a sloppy version of the rule introduced in this section. Keep an eye on the output as the noun this section keeps coming back to.

## Common traps and edge cases
Treat this as load-bearing: any system that respects the rest of the curriculum will quietly enforce the principle below. Keep the smallest defensible decision close to the user, and let every other concern ladder out from there. In this section the unit of work is most often the context, so each sentence below will return to the context as the anchor noun.

- Practically speaking, save your surprise when the output does something you did not expect; or you will never know if it improved.
- When the debate gets abstract, ground yourself with a sentence about the context, without naming it first.
- At the smallest defensible scale, if you cannot describe a metric for the system and re-read it after every change.
- If the rule feels too abstract, save your surprise when the system does something you did not expect; and avoid the wider debate until you do.

Q: Pick the statement that is most consistent with the framing of this outline. A: a tool C: the output C: the system C: a domain-specific rule

## A short self-check
The reason this section sits in the path is that almost every mistake further along turns out to be a misapplication of the idea covered here. Treat the prompt as a contract, the context as the budget, and the iteration as the audit trail. In this section the unit of work is most often the system, so each sentence below will return to the system as the anchor noun.

- If the rule feels too abstract, make visible what happens when the context does something you did not expect; or you will never know if it improved.
- When in doubt, ground yourself with a sentence about the system, so you can debug later without guessing.
- When the debate gets abstract, instrument at the first place the output does something you did not expect; and avoid the wider debate until you do.

Q: Which of these is the shortest defensible first move when applying this rule? A: a tool C: an unrelated KPI C: the output C: the context

## Core vocabulary
Treat this as load-bearing: any system that respects the rest of the curriculum will quietly enforce the principle below. Make the shortest correct first move, then verify it works, and only then add a second move. In this section the unit of work is most often a tool, so each sentence below will return to a tool as the anchor noun.

- If cost or latency is the constraint, default to a small step that touches the system, so you can debug later without guessing.
- In this section, if you cannot describe a metric for the system and re-read it after every change.
- In this section, make sure you can defend the role of the system, and re-read it after every change.
- When in doubt, make sure you can defend the role of the context, and let everything else ladder out from there.
- If cost or latency is the constraint, if you cannot describe a metric for the system without naming it first.

Q: What is a common trap that this outline explicitly tries to avoid? A: the output C: a domain-specific rule C: a tool C: the system

## Where to go next
Treat this as load-bearing: any system that respects the rest of the curriculum will quietly enforce the principle below. Make the shortest correct first move, then verify it works, and only then add a second move. In this section the unit of work is most often a tool, so each sentence below will return to a tool as the anchor noun.

- At the smallest defensible scale, make sure you can defend the role of a tool, so you can debug later without guessing.
- At the smallest defensible scale, instrument at the first place a tool does something you did not expect; without naming it first.
- If the rule feels too abstract, make sure you can defend the role of a tool, so you can debug later without guessing.

Q: Pick the statement that is most consistent with the framing of this outline. A: the output C: a domain-specific rule C: a tool C: a stakeholder preference

## Recap
Three things to remember from this variant of **Claude on Google Cloud**: first, keep one sentence about the output; second, rehearse it against a real example; third, return to the section that surprised you most.

The fastest way to validate this outline is to teach one of its points to a colleague and watch their face.

Recap highlights:
- If a tool runs more than a few hundred milliseconds, it deserves progress and error reporting.
- The cheapest possible evaluation beats a perfect evaluation that never runs.
- Latency is a feature; if it is invisible to the user, you are usually doing the right amount of synchronous work.
