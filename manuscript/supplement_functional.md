# S4. Qualified interfaces and controlled evidence auditing

## S4.1. Scope and independent protocol qualification

This revision evaluates evidence state z rather than administrative disposition y. A condition is supported when the supplied facts establish it, refuted when they contradict it, and unknown when neither relation is established. Unknown is therefore an input-evidence state, not a negative legal ruling. The task supplies the relevant condition representation and tests evidence tracking, justified follow-up and three-valued aggregation. It does not evaluate discovery of every legal prerequisite or complete autonomous interpretation of an exclusion.

The configuration was developed and qualified on ordinary-object examples separate from the customs materials. Four development inputs tested a green bead with positive, contradictory and missing color evidence, and an opaque tube whose weight was unstated. These inputs contained five conditions. The frozen qualification set contained 24 inputs and 27 conditions: direct material and shape attributes, strict and interval bounds, connector negation, frame-versus-screw object binding, net-versus-gross measurement basis, and conjunctions with decisive contradiction or missing evidence. Qualification had eight supported, eight refuted and eight unknown whole-input states.

The model order was fixed as Qwen3-14B Q4_K_M followed, only if necessary, by Granite-3.3-8B Q4_K_M. A configuration had to achieve at least 23/24 correct whole-input decisions, no invalid, incomplete or truncated output, no unsupported affirmative decision, and correct decisive refutation in the presence of another unknown condition. The checklist additionally had to achieve at least 95% condition-state agreement and request nothing after that decisive refutation. Direct output has no condition or request fields, so corresponding checklist-only thresholds were not imputed to it. Qwen3-14B satisfied the fixed gate; the fallback was not needed. No formal customs or controlled diagnostic outcome selected the checkpoint or prompt.

Both direct and checklist interfaces obtained 4/4 development decisions; the checklist obtained 5/5 condition states. Both obtained 24/24 qualification decisions, and the checklist obtained 27/27 condition states. All qualification outputs were structurally valid and complete, with no truncation or unsupported affirmative case decision. Qualification nevertheless revealed a follow-up failure. In Q_negation_3, the lead was required to have no connectors, while the only fact gave its length as 4 m. The checklist correctly marked connector absence and the whole input unknown but returned an empty request list. It therefore retrieved seven of eight necessary qualification requests, with no unnecessary request, and matched 23/24 exact request sets. General request recall was not a frozen acceptance threshold; this failure was retained rather than used to revise the prompt after qualification. Passing these limited checks does not establish legal competence.

## S4.2. Local configuration and inference controls

Inference used the publisher-provided Qwen3-14B-GGUF checkpoint, file Qwen3-14B-Q4_K_M.gguf, with its pinned repository revision and verified official weight digest retained in the external manifest. The local llama.cpp server reported version 0.6.0-dev, build 11516, built with Clang 20.1.8 for Windows x86_64. The runner used Python 3.12.10 on an AMD Ryzen 9 8945HS host with eight physical cores, sixteen logical processors and approximately 32 GB installed memory. No GPU layers were offloaded. Six threads were used for both prefill and inference, with one parallel sequence, context length 4096, logical batch 512 and physical microbatch 128. Memory mapping remained enabled without memory locking; a 6 GiB available-memory preflight was applied before loading. These resource choices were made before formal inference.

The native chat template was rendered through the server with thinking disabled. Requests used temperature 0, seed 20261023, repetition penalty 1.0 and prompt caching disabled. Native-template prompts, request parameters and full responses are retained. Direct generation was capped at 48 tokens; checklist generation was capped at min(1024, 192 + 64m), where m is the supplied condition count. The runner rejected a request before inference if its input-token count plus output allowance exceeded 4096. It did not silently shorten inputs. Differences in output allowance reflect the different requested record sizes and are not presented as matched generation costs.

All reported seconds are wall-clock elapsed times for CPU-only execution with six inference threads, not summed CPU-core time. The shared host load was uncontrolled; external CPU competition occurred during formal checklist inference, and the frozen inference settings were retained. These measurements document the actual run and cannot support a fair efficiency ranking against earlier models or an isolated speed comparison.

JSON-constrained decoding restricted keys, state vocabulary, candidate condition IDs, candidate fact IDs and maximum array lengths. The grammar did not choose the correct state, factual entailment, complete condition coverage, appropriate request or evidence justification. Duplicate condition IDs and request IDs, unexpected keys, unknown IDs and wrong field types were checked separately; missing condition coverage was retained as an incomplete record. Invalid or incomplete records were not reclassified as semantically unknown. Unknown states were instructed to have an empty evidence list, so this deliberately concise interface does not represent competing claims or partially supporting evidence within an unresolved condition. Such source ambiguity is documented in the source audit rather than claimed solved here.

All model inputs were constructed from a whitelist of target, rule text, numbered facts and, for the checklist, numbered requirements. Expected states, requested reference IDs, source-family identifiers and administrative outcomes were withheld. Final integrity checks reconstruct each submitted user prompt and require exact agreement with the stored prompt. The archive includes the complete dynamic JSON schemas, rendered templates, raw responses, token counts and cap indicators; the lengthy schemas need not be reproduced in full here.

## S4.3. Exact natural-language instructions

The decision-only interface used the following instruction, followed by an INPUT object containing target, rule_text and facts. Its response schema had one required decision key with values supported, refuted or unknown.

> Use only the stated facts to audit the supplied rule for the named target. All rule conditions are mandatory unless an explicit alternative is given. Return supported only if the facts establish all mandatory requirements; refuted if a stated fact contradicts a mandatory requirement; otherwise unknown. One decisive contradiction remains refuted even when other facts are missing. Silence is not negation. Keep each value or attribute attached to its product, component and measurement basis. Do not infer facts from product names. Return only {"decision":"supported"}, {"decision":"refuted"}, or {"decision":"unknown"}.

The checklist interface used the following complete instruction, followed by an INPUT object containing target, rule_text, conditions and facts. A JSON FORMAT object listed each supplied condition ID with a supported|refuted|unknown placeholder and an empty evidence array, followed by a decision placeholder and an empty requests array. These placeholders specified the output schema and did not contain reference states.

> Audit whether the numbered facts establish the numbered requirements for the specified target. Use only these facts, not likely properties or background expectations. A requirement can be negative: for "no connectors", explicit absence supports it, explicit presence refutes it, and silence leaves it unknown.
> For each requirement return supported if the facts establish it, refuted if the facts explicitly contradict it, and unknown if neither. Keep attributes attached to the named product, component, operating state, and measurement basis. Facts about a different object do not establish or contradict the target requirement. Do not convert a model identifier into a physical value. Evidence must be a list of supplied fact IDs; unknown has an empty list.
> The decision is refuted when ANY mandatory requirement is refuted, even if another requirement is unknown. Otherwise it is supported only when ALL requirements are supported, and unknown otherwise. Request the IDs of unknown requirements only when the decision is unknown. Request nothing after a decisive refutation, and do not request an already established property. The supplied checklist is conjunctive; it is a provided task input, not a hidden answer.
> Return only the JSON object specified below. There is no need to explain the answer outside that object.

The deterministic comparison applies only to the returned condition states: any mandatory refutation yields refuted; otherwise all supported conditions yield supported; otherwise the state is unknown. This operation does not certify the model’s evidence. Model whole-input state, deterministic aggregate, condition states, citations and requests are scored separately. A missing unknown prerequisite and an omitted schema field are different errors: the former is a substantive evidence/request failure, while the latter is an interface-completeness failure.

## S4.4. Formal controlled inputs and paired functions

The controlled diagnostic contains 108 distinct inputs, 216 supplied conditions and twelve source families. Each family uses two explicitly supplied conditions derived from selected exclusion-clause fragments. These are artificial clauses, not the complete legal exclusions. Both interfaces receive the same complete clause meaning and identical target and facts. The checklist duplicates that meaning as condition IDs and requirements and requests a richer output. The comparison therefore changes representation, instruction and requested output jointly; it does not isolate the effect of deterministic aggregation. In particular, every-granule quantification and the wooden-frame species scope are supplied controlled interpretations, not validated legal interpretations.

| Source family | Principal controlled attribute | Source ruling/product pair |
|---|---|---|
| Connectors | Explicit connector absence | H330938_1 |
| Lifting capacity | At most 550 kg | H318593_2 |
| Motor power | At most 1500 W | H340899_1 |
| Single use | Intended for one use | N310745 |
| Precious-metal plating | No plated article in a set | H330005_1 |
| Textile fraction | Less than 50% by weight | H333371_1 |
| Granule diameter | Every granule within the supplied interval | H332948_1 |
| Load-instrument mass | More than 4 kg and less than 8 kg | H316154_1 |
| Electrical power | Not electrically powered | N303860 |
| Frame species | Target frame not made of teak | N309167 |
| Propulsion power | At most 1000 W | N306552 |
| Fireplace mass | At most 21 kg | H311957_1 |

Each family contains nine unique endpoints: supported base, deletion of the primary fact, irrelevant addition, decisive attribute change, retained contradiction with the companion fact omitted, original object binding, swapped object binding, equivalent expression, and evidence about another object only. Eight linked relationships per family give 96 relationships. Restoration reverses the deletion using the same base endpoint, so it adds no duplicate input. The paired observations are dependent and are not treated as 96 independent cases. Binding swaps preserve the complete value and token frequency while changing ownership. Irrelevant additions leave all relevant facts unchanged. Equivalent expressions use paraphrases or genuine unit conversions, whereas decisive changes alter the relevant attribute.

The first condition carries every whole-input state change in this particular construction. The second condition serves as a companion-state and request-suppression check; the formal whole-input reference always equals the first-condition reference. Whole-input accuracy therefore cannot establish general integration of every necessary condition. The qualification set separately includes a supported first condition and an unknown second condition, but that small check does not remove the formal design restriction. The principal functional evidence consequently comes from condition states, gap/request behavior, object binding and preservation of a verified contradiction.

Paired success requires both endpoint states to match the reference and the expected invariance or change. Always retaining an unknown answer cannot earn credit merely for stability. The report additionally records condition-state agreement; unknown-gap localization; missed necessary requests; unnecessary requests; unsupported affirmative conditions and decisions; acceptable evidence-ID sets; and preservation of a supported refutation when another condition is unknown. Direct output has no condition, citation or request fields, so those metrics are not applicable rather than assigned zero. Whole-input and paired counts are descriptive of this selected diagnostic domain, not estimates of deployment prevalence.

The refutation-with-another-unknown endpoint checks whether the whole-input answer remains refuted and the request list is empty. It does not itself certify the returned condition explanation or citation; those are scored separately. Unknown-gap localization also includes unresolved conditions in already-refuted inputs, whereas necessary-request recall excludes those conditions because a decisive contradiction makes further requests unnecessary for the stated decision task.

An initial construction used literal short quotations in the direct clause but more explicit interpretations in the checklist. Before the pilot predictions were inspected, a separate AI review identified unequal semantics for the granule and frame families. That run was stopped after three direct responses; the responses were preserved as a superseded pilot and never pooled with formal outcomes. The formal clause was rewritten once to include the same complete requirement sentences in both interfaces, with facts, references and paired links unchanged. The input versions, their before/after digests and the review record remain in the external manifests. No prediction selected the revised wording.

## S4.5. Pre-result reference erratum and sensitivity versions

A separate AI-assisted source audit, conducted without reading the formal predictions, identified one semantic dependence in the wooden-frame family. A statement that the target frame is made of teak establishes that it is wooden. Consequently, CF10_refute_missing does not leave its second condition unknown even after the explicitly worded wooden-frame sentence is removed. The frozen input, original expected field, prompts and model responses were preserved. A separate timestamped annotation erratum changes only that condition state from unknown to supported. Every whole-input state and all 96 case-level paired reference relationships remain unchanged, as does the empty request set after the decisive teak refutation.

The erratum also admits equivalent evidence in seven wooden-frame endpoints. For the companion wooden-frame condition, any nonempty subset of the target’s oak/teak statement and its explicitly worded wooden-frame statement is acceptable. The binding cases admit only the target Product A facts, never the neighboring Product B fact. The main condition analysis uses this corrected reference and acceptable citation sets; the original frozen-reference scores remain available. A separate sensitivity excludes the entire frame family, leaving 99 inputs, 198 conditions and 88 linked relationships. The strict test of a refutation coexisting with another unknown condition has eleven, rather than twelve, inputs after correction.

Acceptable citation-set agreement is agreement with a fact-ID reference, not expert-validated legal entailment. Missing or invalid condition records stay in the denominator. The separate AI-assisted audit found no analogous companion-condition entailment in the other eleven families. The correction is an explicit reference-validity repair, not an inference rerun or a model-selection step.

## S4.6. Source-attribute restoration

The separate restoration diagnostic contains four isolated conditions from three rulings and eight before/after endpoints. Before inputs retain the entire frozen product excerpt. After inputs append exactly one admitted product-attribute sentence from the complete public ruling; no holding or applicability conclusion is inserted. Both interfaces receive the same isolated requirement and product facts. The model is not asked to decide the full exclusion.

| Isolated source condition | Added explicit attribute | Reference transition |
|---|---|---|
| H330938_1:c4 | Cables imported without connectors | Unknown to supported |
| H322923_1:c2 | Wagons fitted with four wheels | Unknown to supported |
| H340899_1:c3 | Self-contained electric motors | Unknown to supported under the strict explicit-attribute policy |
| H340899_1:c4 | Motor power not exceeding 1500 W | Unknown to supported |

The two vacuum conditions share one restored sentence, giving three distinct additions rather than four independent sources. The historical motor-condition reference was supported through implicit component inference from a battery-powered vacuum. Its current before-state is unknown under a stricter explicit-attribute policy. This diagnostic therefore measures increased explicit evidence availability, not correction of four historical errors. Restoring connector absence also does not settle the cable ruling’s separate interpretive questions. These are post hoc probes of a retrospectively available public text, not unseen adjudications or contemporaneous applicant files.

## S4.7. Complete results and measured computation

Table S4.1. Complete controlled results under all reference versions. Numerators are matched whole-input or condition states; citation counts use the reference version indicated.

| Reference version | Inputs / conditions / relationships | Direct case states | Checklist case states | Checklist aggregate | Condition states | Citation sets |
|---|---:|---:|---:|---:|---:|---:|
| Original frozen reference | 108 / 216 / 96 | 98/108 | 104/108 | 104/108 | 212/216 | 214/216 |
| Pre-result corrected reference | 108 / 216 / 96 | 98/108 | 104/108 | 104/108 | 211/216 | 213/216 |
| Whole frame family excluded | 99 / 198 / 88 | 91/99 | 97/99 | 97/99 | 196/198 | 198/198 |

Under the corrected reference, gap-localization counts were 31 true positives, 1 false positives and 4 false negatives. Requests included 20 necessary conditions, omitted 4 necessary conditions and included 0 unnecessary conditions; exact request sets matched 104/108 inputs. Unsupported affirmative whole-input conclusions numbered 10 for direct and 3 for checklist, with 3 unsupported affirmative condition states. Strict refutation-with-another-unknown was correctly retained without a request in 11/11 inputs.

An additional descriptive check counted unsupported whole-input refutations against a supported or unknown reference: 0 for direct and 1 for checklist. The unsupported-refutation count at checklist condition level was 1. A model-generated negative state is therefore evaluated against condition evidence rather than presumed to be a verified contradiction. Reference-by-prediction cross-counts are retained in the complete analysis artifacts; these checks do not modify the predeclared primary endpoints.

Table S4.2. Linked functional relationships. Success requires both correct endpoint states and the specified relation; the endpoints are shared.

| Relationship | Direct success | Checklist success |
|---|---:|---:|
| decisive attribute | 12/12 | 12/12 |
| deletion | 10/12 | 10/12 |
| irrelevant addition | 12/12 | 12/12 |
| object binding swap | 12/12 | 12/12 |
| refutation preservation | 12/12 | 12/12 |
| restoration | 10/12 | 10/12 |
| semantic equivalence | 12/12 | 12/12 |
| wrong object only | 4/12 | 10/12 |

The source-restoration diagnostic matched 7/8 direct and 6/8 checklist states. The checklist matched 6/8 condition states and 6/8 acceptable citation sets. Both endpoints of the four restoration pairs were correct in 3/4 direct and 3/4 checklist relationships. These four relationships comprise three sources, with the policy-sensitive motor condition reported above.

The four observed transitions are reported individually below; each reference transition is unknown to supported.

- H330938_1:c4: direct unknown to supported, checklist unknown to supported.
- H322923_1:c2: direct unknown to supported, checklist unknown to supported.
- H340899_1:c3: direct unknown to unknown, checklist refuted to refuted.
- H340899_1:c4: direct unknown to supported, checklist unknown to supported.

The motor condition remained unknown in direct output and refuted in checklist output after the explicit supporting sentence was restored. The checklist therefore had 2 unsupported refutations across the before and after inputs; direct had 0. Neither interface made an unsupported affirmative restoration decision. The strict policy governing the before-reference does not remove the after-restoration error, and these output records do not establish its internal cause.

Table S4.3. Recorded inference costs and interface integrity. Completion-request times are summed wall-clock elapsed seconds for CPU-only, six-thread execution. They include uncontrolled shared-host load variation and exclude separate template/tokenization calls and model startup; full session wall time is retained separately. These records do not establish a fair efficiency ranking across configurations.

| Dataset / interface | Requests | Request seconds | Generated tokens | Maximum input tokens | Invalid / incomplete / capped |
|---|---:|---:|---:|---:|---:|
| qualification cases / direct | 24 | 141.361 | 152 | 197 | 0 / 0 / 0 |
| qualification cases / checklist | 24 | 483.312 | 1294 | 439 | 0 / 0 / 0 |
| controlled cases / direct | 108 | 1190.401 | 684 | 267 | 0 / 0 / 0 |
| controlled cases / checklist | 108 | 3724.611 | 8456 | 522 | 0 / 0 / 0 |
| source recovery cases / direct | 8 | 118.048 | 48 | 551 | 0 / 0 / 0 |
| source recovery cases / checklist | 8 | 220.358 | 408 | 757 | 0 / 0 / 0 |

Development request times were 22.296 s for direct and 92.296 s for checklist. Session metadata retain actual startup and total wall time separately. Exact prompt reconstruction and duplicate-free input/output identity checks passed for every complete reported run. All functional failure records, including errors hidden by a correct whole-input decision, remain in the machine-readable summary.

## S4.8. Reproducibility artifacts and limits

The accompanying experimental folder contains the fixed protocol and runner; development and qualification inputs and thresholds; controlled and source-restoration inputs; pair maps; original source spans; the semantic-alignment review; the reference erratum; complete raw model responses; the original-reference, corrected-reference and family-exclusion analyses; and metric-logic fixtures. The latter are implementation tests rather than model observations. The external manifests contain the file digests and immutable checkpoint identifiers. The archived superseded pilot and earlier failed interfaces are preserved separately and are not pooled into the qualified comparison.

These diagnostics establish only the measured functions within their stated input policy. They do not estimate the frequency of evidence gaps in all applications, prove expert legal validity, automate rule extraction, resolve conflicting sources, or demonstrate reviewer-time or financial savings. AI-assisted source coding and synthetic construction are disclosed; no independent human expert annotation is claimed.
