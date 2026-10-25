# Limited audit of the revision manuscript

Scope: read-only audit of the evidence, selection, inventory and numerical claims in `task_methods.md`, `results_core.md` and `discussion_conclusion.md`. The exact snapshots and observed record schemas are saved in `manuscript_claim_check_snapshot.json`. New neural-model results owned by other agents are outside this check. Results placeholders are work in progress and are not counted as errors. No manuscript file was edited.

## Required corrections

1. **Methods 3.1, paragraph beginning “Our evidence records contain”.** The present wording lists “a condition type, governed object” as stored fields. The 208 first-pass condition records actually have `condition_id`, `rule_quote`, `rule_span`, `evidence_state`, `fact_evidence`, `rationale` and `coding_status`. Alternatives and other scope structure appear in the separate `logical_structure` object. A governed object may be explicit in a quotation or rationale, but is not a uniformly encoded field. Replace the first sentence with:

   “Our evidence records contain literal rule spans, literal factual spans where available, a condition state and a coding rationale, with logical operators preserved separately.”

   The later proposal for a richer governed-object representation in Discussion 6.3 can remain; it is correctly framed as a useful representation rather than a complete existing ontology.

2. **Methods 3.3, paragraph beginning “The 73 compatible-code inputs”.** “Both preserve explanations and source spans” overstates the second pass. That file contains 73 records with `case_id`, `state` and `reason`; it is a separate case-level judgment, not another condition-span annotation. Replace the relevant sentences with:

   “The first pass preserves 208 condition-level records with source spans and coding rationales. The second pass records a case-level state and reason for each of the 73 inputs. Exact-span checks apply to the stored quotations, and the two passes are compared at case level.”

   Keep the existing same-lineage, prior-exposure and nonexpert limitations. The 66/73 agreement and kappa 0.814 concern initial case-level states only.

3. **Methods 3.1, evidence-policy paragraph.** State the quantifier for inputs describing multiple products. It determines the revised relay case and cannot remain implicit in the general definition of a product–candidate pair. Add:

   “Where an input describes multiple products, support requires every listed product to satisfy the candidate conditions; one definite counterexample suffices for refutation. Alternative ratings are evaluated discretely within each product rather than pooled into a continuous range across products.”

   Methods 4.5 already correctly identifies the reference-only relay adapter and all-products requirement, but the policy should be defined before its diagnostic implementation.

## Verified current statements

- The retrieval corpus has 2,482 rulings, not 2,482 documented individual relevance decisions. The 102 curated records come from 92 rulings; 16 record exclusions leave 86 pairs from 77 rulings. The current draft does not fabricate the missing retrieval-to-curation screening log.
- Inventory: 397 descriptions, 429 aliases and 337 distinct code strings; 41 standalone statistical codes plus two dated code-only replacements leave 354 remaining descriptions, or 89.2%. The 162/198/163/89 values are surface markers. The 38 disagreement audit partitions into 13 magnitude/count conditions, 24 nonmeasurement identifiers or dates and one named-component minimum. It is not an estimate of global semantic precision or recall.
- Quotation provenance: 86/86 rule and administrative reference excerpts are contiguous after normalization, whereas complete factual excerpts are contiguous for 82/86. The four remaining fact inputs concatenate source spans, with all nonwhitespace characters located in source order. The N316485 incomplete conditional fragment and operational unknown label are disclosed correctly.
- Methods 3.3 correctly separates the initial comparison from the later relay source correction and notes the handle-excluded measurement. Initial agreement remains 66/73, with first states 23/5/45 and second states 25/4/44. Final operational states are 21 support, 5 refute and 47 unknown. Do not attribute the final five refuted cases solely to agreement between the two initial passes.
- Administrative-by-evidence counts are eligible: 21 support and 26 unknown; ineligible: 5 refute and 21 unknown. No original disposition is changed.
- Forty-three numerical conditions occur in 33 pairs. Final numerical states are 23 pass, 3 fail and 7 unknown. Four-layer match counts in the requested order are 33/33, 30/33, 17/33 and 17/33. Emitted pass/fail/unknown counts are 23/3/7, 21/2/10, 10/1/22 and 10/1/22. The first result is internal execution consistency of the encoded representation, as the current Methods 4.5 and Figure 3 caption correctly say.
- The frozen fully automatic engine recovers none of the three definite numeric violations. Only five numerical-pass cases also have every qualitative condition supported; another 18 numerical-pass cases remain evidence-unknown. Test-only violation certificates could correct 1/3/1 native affirmative outputs for NLI/0.6B/4B, respectively. These are opportunities, not achieved frozen-engine corrections.
- The constructed revision suite has 96 rows, 48 pairs, 12 purposive mechanisms and 88 unique exact inputs. Seven duplicate clusters account for eight extra rows. There are 20 equivalence pairs, 26 decisive-change pairs and two same-state controls. The disclosed eight-input grammar correction after the first engine replay is accurate.
- Frozen-engine constructed agreement is 54/96, or 47/88 on unique inputs. The separate post hoc v2 obtains 73/96, or 66/88 on unique inputs, and 24/33 on real numerical cases versus frozen 17/33. Its development on inspected diagnostic examples, including the approximation-field repair after the first v2 run, is correctly disclosed in Methods 4.5. These are development diagnostics, not held-out generalization.
- Methods 4.5 appropriately distinguishes the reference-only relay binding adapter from the frozen automatic matcher; no general field-binding capability is silently attributed to the frozen extractor.
- Discussion 6.2–6.4 retains the central claim boundaries: AI coding does not create expert validity, ordinary accuracy can reward excessive unknown, local arithmetic performance does not certify full applicability, and prospective workload or duty savings were not observed.

## Insertion guardrails

The remaining evidence/numeric placeholders should use `final_data_summary.json` and `evidence_numeric_report.md`, not earlier reference versions. Reference history and initial decisions are preserved. Unknown-reason counts mix explicitly labeled condition occurrences and case flags and may overlap; their columns must not be summed to 33 cases. Native three-state evidence results must not be replaced by binary outputs or numerically guarded outputs without being renamed.

The independent reference audit is AI-assisted. Its agreement with the specified arithmetic and quote spans supports reproducibility, not independent human or domain validity. No additional expert-confirmation claim is warranted by the same-lineage second pass or by v2 performance on development examples.
