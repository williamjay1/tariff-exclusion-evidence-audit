# Evidence audit experiment results

This report concerns agreement with explicit, AI-assisted diagnostic references. The controlled cases are purpose-built synthetic examples anchored to selected source clauses. The source-restoration cases evaluate isolated attributes, not full legal eligibility. No new adjudications, expert gold, or population prevalence are claimed.

The same local Qwen3-14B Q4_K_M configuration passed the frozen independent qualification gate in both interfaces. Both obtained 24/24 case states; the checklist obtained 27/27 condition states. All outputs were valid, and there were no unsupported affirmative decisions. One unknown item omitted its required information request (7/8 necessary requests), showing that qualification did not imply perfect downstream behavior.

For the formal controlled comparison, both interfaces receive the same complete clause and numbered facts. The checklist additionally duplicates the clause as numbered conditions and requests condition states, fact citations and follow-up IDs. This joint representation/output change does not isolate an aggregation effect. The every-granule quantifier and frame-species scope are supplied interpretations within a two-condition diagnostic, not verified interpretations of complete legal provisions.

## controlled_cases

The direct interface matched 98/108 reference states. The checklist overall decision matched 104/108, and deterministic aggregation of its condition states matched 104/108. Condition-state agreement was 211/216. Unsupported affirmative case conclusions were 10 in direct and 3 in checklist. As an additional descriptive check, unsupported case refutations were 0 in direct and 1 in checklist; the checklist had 1 unsupported refuted conditions. Complete reference-by-prediction matrices are retained in the JSON summary.

Gap localization had 31 true positives, 1 false positives and 4 missed gaps. Required follow-up had 20 correctly requested conditions, 4 missing necessary requests and 0 unnecessary requests. Exact request sets matched in 104/108 inputs. These metrics are not applicable to the decision-only direct interface.

Acceptable citation-ID sets matched 213/216 conditions, including 180/181 determinate conditions. This is fact-ID retrieval agreement, not expert-validated legal entailment.

| Controlled relationship | Direct: both endpoints correct | Checklist: both endpoints correct |
|---|---:|---:|
| decisive_attribute | 12/12 | 12/12 |
| deletion | 10/12 | 10/12 |
| irrelevant_addition | 12/12 | 12/12 |
| object_binding_swap | 12/12 | 12/12 |
| refutation_preservation | 12/12 | 12/12 |
| restoration | 10/12 | 10/12 |
| semantic_equivalence | 12/12 | 12/12 |
| wrong_object_only | 4/12 | 10/12 |

Pair success requires both endpoint states to be correct and the required invariance/change. Shared endpoints are retained as dependent diagnostics; no population confidence interval is attached to this selected domain.

Recorded request time was 1190.401 s for direct and 3724.611 s for checklist. These are actual request times on the available CPU host; model loading and other runs are recorded separately in session files.

All 15 arm-by-input functional failure records are retained in experiment_final_summary.json, including cases whose whole-input decision is correct.

Before any formal outcomes were read, a separate AI-assisted source audit found that oak/teak implies a wooden frame. The frozen input and predictions remain unchanged. A timestamped erratum changes one CF10 condition from unknown to supported and admits equivalent target-frame citations in seven inputs; all whole-input states and linked case relationships remain unchanged.

The original frozen reference gives checklist condition agreement 212/216; the erratum gives 211/216. Excluding the entire frame family leaves 99 inputs, 198 conditions and 88 linked relationships: condition agreement 196/198. Strict refutation-with-another-unknown now has eleven cases; 11/11 retain refutation without a request.

## source_recovery_cases

The direct interface matched 7/8 reference states. The checklist overall decision matched 6/8, and deterministic aggregation of its condition states matched 6/8. Condition-state agreement was 6/8. Unsupported affirmative case conclusions were 0 in direct and 0 in checklist. As an additional descriptive check, unsupported case refutations were 0 in direct and 2 in checklist; the checklist had 2 unsupported refuted conditions. Complete reference-by-prediction matrices are retained in the JSON summary.

Gap localization had 3 true positives, 0 false positives and 1 missed gaps. Required follow-up had 3 correctly requested conditions, 1 missing necessary requests and 0 unnecessary requests. Exact request sets matched in 7/8 inputs. These metrics are not applicable to the decision-only direct interface.

Acceptable citation-ID sets matched 6/8 conditions, including 3/4 determinate conditions. This is fact-ID retrieval agreement, not expert-validated legal entailment.

| Controlled relationship | Direct: both endpoints correct | Checklist: both endpoints correct |
|---|---:|---:|
| source_attribute_restoration | 3/4 | 3/4 |

Pair success requires both endpoint states to be correct and the required invariance/change. Shared endpoints are retained as dependent diagnostics; no population confidence interval is attached to this selected domain.

Recorded request time was 118.048 s for direct and 220.358 s for checklist. These are actual request times on the available CPU host; model loading and other runs are recorded separately in session files.

All 3 arm-by-input functional failure records are retained in experiment_final_summary.json, including cases whose whole-input decision is correct.

| Isolated condition | Direct before → after | Checklist before → after | Reference |
|---|---|---|---|
| H330938_1:c4 | unknown → supported | unknown → supported | unknown → supported |
| H322923_1:c2 | unknown → supported | unknown → supported | unknown → supported |
| H340899_1:c3 | unknown → unknown | refuted → refuted | unknown → supported |
| H340899_1:c4 | unknown → supported | unknown → supported | unknown → supported |

All four transitions are shown, including the motor condition whose before-reference depends on the strict explicit-attribute policy. The motor condition remained unknown in direct output and refuted in checklist output after its explicit supporting source sentence was added. The historical before-state policy does not explain away this after-restoration failure; the responses do not establish its internal cause.

## Scope and historical diagnostic

Source recovery tests explicit evidence availability. The motor condition was supported in the historical annotation through an implicit component inference; its before-state is unknown only under the present stricter evidence policy. The two vacuum conditions share one restored sentence. The four pairs must not be described as four corrected historical labels or four independent rulings.

The old refuted-three-to-one loss is reproduced separately: an unknown numeric status triggered referral even when the neural model was negative. The two lost cases include a 6000-pound lifting capacity against a 550-kg maximum and enclosure dimensions inconsistent with the stipulated exact dimensions. The old policy is preserved as an archival comparator, not silently repaired.

A three-request pilot with semantically unequal clause wording was stopped before predictions were inspected and is preserved under the superseded constructed_cases filenames. Formal controlled_cases outputs use the corrected common clause; no formal outcome selected the wording or model.
