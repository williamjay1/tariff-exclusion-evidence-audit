# Evidence-state review instrument

This instrument concerns what a restricted product description establishes about a supplied exclusion description. It does not ask the reviewer to predict or reconstruct CBP's administrative decision. The current study used AI-assisted source coding and a separate same-lineage AI reading. No human or customs expert annotations were obtained. The unlabelled packet is available for subsequent review; its availability is not evidence that such review has occurred.

Use `unlabelled_review_packet.jsonl`. The packet contains 73 shuffled inputs and blank responses; keep `review_packet_private_key.jsonl`, administrative dispositions, model predictions, legal analysis and the present reference files unavailable during a new coding pass. Record the coder identity, accessible model version or relevant expertise, date and whether the coder previously saw the project. The existing AI readers had prior project knowledge, so their review is outcome-masked for this pass rather than completely uninformed blinding.

For every mandatory condition, copy a literal rule span and any supporting or contradictory fact spans. Character offsets are zero-based and end-exclusive in the exact JSON strings. Preserve negation and alternatives: “A or B” is one disjunction; “whether or not A” permits either state; “other than X” requires that the exception be excluded; “including” can introduce examples rather than a further required conjunction. Retain an incorporated legal definition as unresolved if the supplied text does not establish it. Do not silently expand a heading reference using the administrative conclusion.

Use **support** when the visible facts establish the condition through an explicit statement or a documented ordinary-language equivalence. Use **refute** for an explicit contradiction. Use **unknown** for missing facts, conflicting evidence that changes the threshold conclusion, unresolved legal categories, unclear measurement scope or rating interpretation. Evidence not mentioning a prohibited component does not prove its absence. A list of known components need not be exhaustive.

The case-level claim is that all products included in that input satisfy the candidate scope. A definite violating product refutes that proposition. Keep products distinct when comparing their attributes. Alternative interpretations of a rating remain discrete alternatives, not a made-up continuous range: if every possible rating for one product violates the same criterion, that product is refuted; if interpretations disagree, it is unknown. For a conjunction, one refuted condition suffices for refutation; otherwise one unknown condition makes the result unknown. Numeric satisfaction never supplies missing qualitative conditions.

For numeric conditions record attribute, subject, unit, endpoint values and inclusivity, plus measurement scope. Keep own weight separate from load capacity. Do not read digits in a model number, CAS identifier, material grade, tariff code or date as a physical measurement. Unit conversion must be explicit. An approximate value without a tolerance cannot become an exact point. A reported partial-article dimension does not establish the dimension of the complete article without a further premise.

Complete `response.evidence_state`, the list of condition records, rationale and coder metadata. Compare two independently completed copies using:

```
python compute_coding_agreement.py coder_a.jsonl coder_b.jsonl
```

The script ignores blank forms and reports jointly completed counts, disagreement counts and Cohen's kappa. Preserve initial responses before adjudication; do not replace initial agreement with post-discussion agreement. Report discrepancies and alternative-policy sensitivity. Agreement between AI readers of the same model lineage cannot substitute for independent domain validation.

Current operational policy: the seven semantic disagreements between the two initial AI passes remain unknown. A separate source-based numeric audit then established an explicit counterexample for the relay case and clarified the handle-excluded jack dimensions. Original administrative labels and both initial coding passes remain unchanged.
