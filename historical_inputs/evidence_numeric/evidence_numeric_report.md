# Evidence and numerical diagnostics: verified revision results

The analysis distinguishes an administrative disposition from what the model-visible evidence establishes. Both targets are retained; neither is substituted for the other. All new references are AI-assisted diagnostic references, not expert gold. Original source files, benchmark inputs, dispositions and model predictions are unchanged.

## Sample formation and source provenance

Six saved official CROSS searches produced 4,530 query-hit occurrences and 2,482 unique rulings in the 7 October 2026 snapshot. The four initial queries were `301 AND exclusion` (177), `301 AND exclusions` (1,723), `301 AND exempt` (80) and `301 AND exclude` (54); the wider queries `exclusion` and `exclusions` returned 392 and 2,104. Pagination used 100 results per page, ascending date, and the search interval 1 January 2018–7 October 2026. Every query's saved page counts sum to its reported total. The first four queries cover 1,914 unique IDs; two explicit seed details raised initial detail requests to 1,916. The broader queries added 566 new detail requests. The union of all six query result sets contains every final ruling, including those seeds. Two failed detail requests were recovered successfully.

AI-assisted purposive curation produced 102 case records from 92 rulings. The transition from the retrieved corpus to these records lacks exhaustive individual screening decisions. It cannot be presented as 2,482 rulings independently read and systematically adjudicated. The 2,390 rulings with no curated record are marked as having no logged individual curation decision. The subsequent exclusion of 16 curated records is reproducible: six lacked binary reference dispositions, five were outside the product-description task, four lacked a full candidate rule, and one contained a documented source conflict. The retained corpus has 86 pairs from 77 rulings; 73 have compatible product and candidate codes.

All 86 frozen fact inputs and scope strings match their curated records. All 86 rule quotations and administrative reference quotations match whitespace-normalized official text, as do 82 complete fact excerpts. The remaining four fact inputs concatenate source spans rather than forming continuous excerpts: N309775_buttons joins the first and fourth product descriptions; N314745_self joins the first, second and fourth bicycle descriptions; N314745_pedal joins the third and fifth; N316485 joins component paragraphs, a dimension sentence and the final import-condition phrase. An ordered character-level check finds no unmatched nonwhitespace content in those four inputs. The last input contains an incomplete appended `if` phrase, and its operational evidence state remains unknown. These checks establish textual provenance, not completeness or expert validity of the selection.

## Outcome-masked evidence coding

The first AI pass coded 208 conditions in the 73 compatible-code inputs. Each condition includes a literal rule span, factual spans where available, a state and rationale; a separate logical representation retains alternatives, exceptions and incorporated definitions. The second pass supplies case-level states and reasons, rather than a second set of 208 condition annotations. Administrative outcomes, legal-analysis sections and model outputs were excluded from the coding view. Both AI readers had prior project involvement, so this is outcome-masked review rather than a claim of uninformed blinding or independent human expertise.

The initial passes assigned 23/5/45 and 25/4/44 supported/refuted/unknown cases, agreeing on 66 of 73 (90.4%; Cohen's kappa 0.814). Their seven differences concerned product categories, material composition, use, incorporated headings and multi-product descriptions. A conservative operational policy retains all seven as unresolved. A subsequent numerical source audit additionally found that jack dimensions explicitly excluding the handle do not establish the complete-article dimensions. It also corrected the relay case: several listed relays violate the voltage interval under both coil and contact interpretations, even though those alternatives had initially been collapsed into an uninformative continuous hull. This third-pass correction is recorded separately from initial agreement.

The final operational evidence policy yields 21 supported, 5 refuted and 47 unknown cases. Among the 47 administratively eligible pairs, 21 are supported by the restricted evidence and 26 remain unknown. Among the 26 administratively ineligible pairs, five are refuted and 21 remain unknown. Missing evidence is therefore not equivalent to an adverse administrative decision. These are policy-dependent AI readings of a restricted input, and their agreement does not establish independent legal validity.

Original native three-class predictions, without binary collapse or numerical override, give the following results. Macro recall averages the three class recalls, including unknown. The final two columns use each initial AI pass as an alternative reference policy.

| Model | Final correct | Final macro recall (%) | Final macro F1 (%) | Unknown recall (%) | First-pass macro recall (%) | Second-pass macro recall (%) |
|---|---:|---:|---:|---:|---:|---:|
| nli | 31/73 | 32.3 | 31.8 | 53.2 | 38.4 | 33.8 |
| qwen | 21/73 | 33.3 | 14.9 | 0.0 | 33.3 | 33.3 |
| qwen4 | 27/73 | 53.7 | 33.2 | 10.6 | 52.7 | 56.0 |
| always_unknown_diagnostic | 47/73 | 33.3 | 26.1 | 100.0 | 33.3 | 33.3 |

The always-unknown diagnostic has higher ordinary accuracy because unknown is frequent; it cannot recover supported or refuted cases. The 4B model recognizes 19 of 21 supported cases and three of five refuted cases, but only five of 47 unknown cases. Its remaining unknown-reference cases receive 21 affirmative and 21 negative outputs. Performance against administrative labels consequently answers a different question from evidence-sufficiency performance.

## Real numerical opportunities and layer interventions

Independent source coding identified 43 numerical conditions across 33 cases. After source-audit corrections, the case-level numerical states are 23 satisfied, three violated and seven unresolved. Only five cases combine numerical satisfaction with support for every qualitative condition. Eighteen numerically satisfied cases still contain unresolved qualitative requirements. The three numerical violations occur in H318593_2 (lifting capacity), N307161 (dimensions), and N311039_33 (per-product voltage alternatives).

The four interventions below actually execute the frozen Decimal comparator. Source-coded fields are test-only inputs, independently specified from literal source spans; they are not generated by the evaluated parser. For the relay case an explicit reference-only adapter preserves subjects and discrete alternative ratings, calls the same comparator for each alternative, and then evaluates the all-listed-products claim. This adapter is not attributed to the frozen automatic matcher. The source-coded/source-coded result checks consistency of the reference representation and execution; 33/33 is not an independently established accuracy estimate.

| Input layer | State agreement | Satisfied | Violated | Unknown |
|---|---:|---:|---:|---:|
| Source-coded rule + source-coded fields | 33/33 | 23 | 3 | 7 |
| Automatic rule + source-coded fields | 30/33 | 21 | 2 | 10 |
| Source-coded rule + automatic fields | 17/33 | 10 | 1 | 22 |
| Automatic rule + automatic fields | 17/33 | 10 | 1 | 22 |

The diagnostic trace further separates reasons for unresolved execution. The columns follow the intervention order above: RR denotes reference rule/reference fields, AR automatic rule/reference fields, RA reference rule/automatic fields, and AA fully automatic. Condition-level counts and case-level flags are explicitly distinguished. Categories can overlap and must not be summed into a number of cases.

| Reason | Counting unit | RR | AR | RA | AA |
|---|---|---:|---:|---:|---:|
| missing_or_binding_mismatch | condition occurrences | 8 | 4 | 21 | 11 |
| multiple_distinct_fields | condition occurrences | 0 | 0 | 8 | 9 |
| straddling_interval | condition occurrences | 2 | 2 | 0 | 0 |
| no_parsed_constraint | cases | 0 | 3 | 0 | 3 |
| unparsed_rule_quantity | cases | 0 | 5 | 0 | 5 |

The two automatic-field configurations retain the same incorrect numerical failure for the vacuum model identifier and fail to recover the three definite violation certificates. Missing fields, attribute binding, multiple distinct candidate values, unsupported expressions and genuinely insufficient evidence have separate traces. A test-only numerical violation certificate could correct one affirmative NLI output, three affirmative 0.6B outputs and one affirmative 4B output. Those counts describe available source evidence; they are not achieved corrections by the frozen extractor. Numerical satisfaction alone cannot justify affirmative legal-scope predictions.

Paired differences use the original linked groups restricted to these 33 cases: 16 groups, with 15 cases in the largest. Each of 2,000 resamples draws 16 groups with replacement, preserving all retained cases within each selected group and using the same draws across comparisons (seed 20261007). Agreement is pooled over cases in each resample. All 2,000 differences are defined for every contrast; no class-presence exclusion is needed for exact three-state agreement. The percentile intervals below condition on the saved predictions and source-coded references. They do not incorporate reference uncertainty, model refitting or independent v2 generalization.

| Paired comparison | Difference (percentage points) | 95% group-resampling interval |
|---|---:|---:|
| Reference fields minus automatic fields; reference rule fixed | 48.5 | 33.3 to 66.7 |
| Reference fields minus automatic fields; automatic rule fixed | 39.4 | 18.7 to 50.0 |
| Reference rule minus automatic rule; reference fields fixed | 9.1 | 0.0 to 33.3 |
| Reference rule minus automatic rule; automatic fields fixed | 0.0 | 0.0 to 0.0 |
| Post hoc v2 minus frozen fully automatic | 21.2 | 10.0 to 35.0 |

The reference-rule/reference-field endpoint remains an internal consistency control, so its difference from an automatic layer is a representation diagnostic, not a causal intervention on legal accuracy. The zero difference with automatic fields reflects identical case-level correctness indicators in this replay, not proof that rule parsing is generally irrelevant. The v2 contrast describes repair on inspected development cases.

## Constructed mechanism diagnostics and post hoc repair

The constructed suite contains 96 rows, 48 pairs and 12 purposively selected mechanisms, but only 88 distinct fact–rule inputs. Labels were specified using explicit interval, alternative and conditional semantics, and independently checked by another AI; the examples are not additional rulings or human annotations. Twenty pairs are equivalent reformulations, 26 deliberately change the expected state, and two retain the state while changing a value. The component-binding family's rule wording was standardized after an initial frozen-engine run to remove an unsupported-grammar confound, with facts and labels unchanged; the initial inputs and predictions remain available.

The frozen engine agrees with 54/96 constructed references. A separately saved v2 applies general repairs to identifier boundaries, supported units, comparison intervals, explicit mass/capacity and motor/lamp binding, and measurement uncertainty. It was developed after observing these diagnostics, including a further repair when the first v2 run showed that dropping an approximate report could falsely certify a competing exact report. The initial v2 summary is retained. Thus the v2 findings are transparent post hoc software diagnostics, not held-out generalization evidence.

Final v2 agreement is 73/96 on constructed rows and 24/33 on the real numerical cases, compared with 54/96 and 17/33 for the frozen engine. On the 88 unique constructed inputs, the corresponding counts are 47/88 and 66/88. v2 preserves predictions across all 20 equivalence pairs and gets both members right in 18; it gets both members right in 14/26 decisive-change pairs. Compound units and general logical composition remain substantial limitations. The lower nested-exception accuracy follows deliberate abstention on unsupported exceptions rather than an attempt to claim that a flattened conjunction is a sound legal interpretation.

| Mechanism | Frozen correct | v2 correct |
|---|---:|---:|
| comparative_facts | 4/8 | 8/8 |
| component_binding | 0/8 | 8/8 |
| compound_units | 0/8 | 0/8 |
| conflicting_reports | 6/8 | 6/8 |
| dimension_binding | 8/8 | 8/8 |
| disjunction | 2/8 | 2/8 |
| identifier | 4/8 | 8/8 |
| mass_capacity | 5/8 | 8/8 |
| measurement_uncertainty | 6/8 | 8/8 |
| nested_exception | 5/8 | 1/8 |
| two_sided_bounds | 8/8 | 8/8 |
| unit_equivalence | 6/8 | 8/8 |

## Inventory interpretation

The frozen statutory transcription contains 397 descriptions and 429 note aliases. Its original feature counts—162 quantitative markers, 198 numbers outside removed tariff codes, 163 negation markers and 89 purpose markers—are surface-feature counts. An AI source audit examined every one of the 38 disagreements between the two quantitative proxies. Thirteen contain genuine measurable or item-count requirements missed by the quantitative-marker expression; 24 contain nonmeasurement identifiers or references, including CAS identifiers, material grades, tariff headings, standards, regulatory classes and statutory dates. One contains a minimum inventory of named components rather than a scalar measurement. This purposive disagreement audit cannot estimate population precision, recall or corrected prevalence.

The original `whole_code` flag identifies 41 descriptions containing exactly one standalone statistical code. Two further descriptions contain dated replacements of statistical codes, not additional physical product criteria. Semantic reporting should therefore distinguish 41 standalone code descriptions, two temporal code-only descriptions, and 354 remaining descriptions. The transcription is a versioned representation of one official index, not a full historical legal ontology.

## Reproducible instruments and boundaries

Machine-readable deliverables include the complete retrieval-membership ledger; 86 retained-source checks; original, second-pass and operational evidence references; source-coded numerical fields and preserved earlier versions; four-layer execution traces; original and v2 diagnostic outputs; inventory semantic checks; and an unlabelled review packet with a coding guide and agreement calculator. No expert review is claimed to have taken place. The public administrative sources are authoritative about their published dispositions, but AI extraction, sample curation and restricted-input evidence judgments remain fallible. Prospective review with independently supplied product evidence is outside the present validation.
