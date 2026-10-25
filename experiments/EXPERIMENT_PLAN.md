# Evidence auditing reconstruction, 23 October 2026

This file records the execution plan before new formal outcomes. The route is SCI empirical evaluation and measurement: the main question is whether a system correctly tracks condition evidence and required follow-up under controlled changes. It is not causal economics, administrative-outcome prediction, or a deployment benefit study. The experiment-design and paper-venue-router skills supply the applicable design checks; this single plan consolidates their records.

## Primary task and comparison

The primary target is evidence state z, separately for necessary conditions and for the conjunction. A curated condition checklist is supplied in the structured arm; neither automatic condition extraction nor complete legal interpretation is claimed. Both arms receive exactly the same complete controlled clause, target and numbered facts. The structured arm also receives a duplicate canonical condition list with IDs, whereas direct output is only a native three-state decision. Representation and requested output differ, so this is not an isolated aggregation effect. Both use the same local checkpoint, quantization, sampling and context budget; output token budgets differ because their outputs differ. No forced binary conversion is used.

The checklist arm returns condition IDs, supported/refuted/unknown, supporting fact IDs, an overall decision, and requested missing-condition IDs. We separately retain (a) the model's direct overall state, (b) deterministic three-valued conjunction over its condition states and (c) its requested conditions. A verified refutation dominates unrelated missing facts. Model-negative conclusions without verified evidence are not presumed trustworthy.

Protocol JSON constraints restrict format and vocabulary only. They do not fix state values, evidence choices, condition coverage or requests. Missing/duplicate IDs, absent evidence for determinate states, unsupported fact citations, truncation and invalid output are separately recorded. Necessary-condition omission in the substantive analysis means a required missing item is not identified/requested, not merely that a schema field is absent.

## Independent development and qualification

The four development cases and twenty-four qualification cases are constructed from ordinary objects with explicit attributes, not from the formal customs materials. Their immutable IDs, expectations and input hashes are in development_cases.jsonl, qualification_cases.jsonl and qualification_manifest.json. The 24-case qualification has 27 atomic conditions spanning direct attributes, strict bounds, intervals, explicit negation, object binding, measurement basis and conjunction. Qualification requires at least 23/24 correct case decisions, at least 95% condition accuracy in the checklist arm, no invalid/incomplete/truncated output, no unsupported affirmative decision, and correct refutation without follow-up when a decisive contradiction coexists with another missing condition. The direct arm is separately assessed.

The fixed model order is Qwen3-14B Q4_K_M, then Granite-3.3-8B Q4_K_M if needed. Passing does not establish legal competence; it excludes basic interface malfunction as the sole explanation for subsequent failures. All failing versions remain in the archive. Formal data are not used to choose prompt versions or checkpoints. The first implementation uses disabled thinking, native chat templates, local llama.cpp, temperature 0, seed 20261023, context 4096, and six CPU threads. All prompts, schemas, raw replies, cap indicators and timing are retained.

## Formal evidence construction

The source-audit agent supplies the 208-condition audit and source spans. For original and restored inputs, product attributes are separated from category interpretation, rule exposition, application reasoning and administrative outcomes. Restoring an admissible attribute can update its condition while leaving another interpretive condition unknown. H330938 is therefore not forced to whole-case support merely because connector absence is restored. Party assertions are distinguished from laboratory findings and agency-stated attributes.

Direct, interpretive, insufficient and disputed conditions are reported separately. The main defensible reference is transparent textual evidence under the stated policy; AI source coding is not expert legal gold. Complete public rulings are still retrospective documents, not original applicant submissions.

The old 208 condition entries are not assumed to be atomic. Deterministic conjunction is restricted to cases explicitly audited as a safe flat conjunction; embedded alternatives, exceptions, compound propositions or unresolved interpretation are not flattened to AND. The complete 73-case source audit and the narrower formal model subset may have different denominators. Attribute restoration may also be evaluated as an isolated condition diagnostic without asserting a whole-rule legal conclusion.

The deliberately short model interface uses an empty evidence list for unknown and therefore does not represent partial evidence or competing source claims for an unresolved condition. Contradictory sources are excluded from the ordinary constructed task and belong to a separately marked boundary, not claimed solved. Richer unknown causes come from the audited source table. Direct-decision output has no localization, citation or request fields, so those endpoint values are not applicable for that arm.

## Controlled intervention matrix

Each intervention changes one evidence feature and retains its source family identifier. Source-restored cases and synthetic modifications are explicitly distinguished.

| Intervention | Fixed elements | Expected behavior |
|---|---|---|
| Delete a unique supporting fact | Rule, target, other facts | Corresponding condition becomes unknown; identify its gap; avoid whole-case support |
| Restore the admissible original fact | Original rule and all other facts | Update that condition; do not manufacture support for unrelated conditions |
| Add an irrelevant statement | All relevant facts | Preserve correct decision and request set |
| Replace a decisive attribute | Other requirements explicitly controlled | Change the affected condition and overall conclusion as required |
| Keep a verified contradiction but omit another property | Contradictory fact and target | Preserve refutation; no pointless requests |
| Swap component/product ownership or measurement basis | Numeric magnitudes and rule | Follow the correct object and scope, not a bag of numbers |
| Paraphrase or equivalent unit conversion | Semantic content | Remain correct at both endpoints |

All constructed counterfactuals are diagnostic tests, not new observed customs cases. The design includes both invariance and required change so an always-unknown model cannot receive credit merely for stability. Formal families and expectations are frozen before their inference. No unseen-material generalization is claimed from replayed public rulings or constructed modifications.

The approved design has 108 unique inputs from twelve source families and 96 linked relationships, including restoration reusing the deletion endpoints. Before formal predictions were inspected, the parent reviewer identified two implicit interpretation differences between arms. A three-request pilot was stopped and retained uninspected; the formal input now includes identical complete requirement sentences for both arms. The every-granule quantifier and frame-species scope are supplied controlled interpretations, not verified legal interpretations. All two-condition fragments are explicitly narrower than the full exclusion. This correction and all old pilot files are recorded in controlled_freeze.json; the formal file is controlled_cases.jsonl.

The source-restoration diagnostic is separate: four isolated conditions, eight endpoints and three rulings. It retains the full frozen excerpt and adds only the admitted source-attribute sentence. The two vacuum conditions share one restored sentence. The motor condition was historically supported under implicit inference and is unknown only under the present explicit-attribute policy; this diagnostic therefore measures increased explicit evidence availability, not correction of four old errors.

## Endpoints

Primary endpoints are condition-state agreement in directly checkable conditions; missing-condition localization precision/recall; required gaps not identified/requested; unsupported affirmative conditions and case conclusions; unnecessary follow-up requests after support or a decisive refutation; correct evidence-object binding; and correctly updated paired endpoints. Equivalent-pair success requires both correct endpoints and preservation; decisive-pair success requires both correct endpoints and the expected change. Model overall decisions and deterministic aggregation are reported side by side. Interface invalidity is separate from unknown.

Counts use cases and linked source/rule families as denominators, with paired family resampling where meaningful. These intervals describe the purposive diagnostic collection, not population prevalence. Differences at similar determinate coverage are secondary and cannot establish real reviewer time savings.

## Resources and execution

On inspection D had approximately 203 GB free, F approximately 2.90 TB free, and available RAM approximately 9.6 GiB. Existing officially hash-checked GGUF copies and the existing llama.cpp runtime are read from D. No new model/raw download or paid API is needed. All new outputs, temporary files and logs are under this experiments directory on D. The 14B model uses mmap with no mlock, with a 6 GiB available-RAM preflight; Granite uses 4 GiB. Only the server started by this script is terminated. Direct development requests initially took about 5.5 seconds and checklist requests about 18–20 seconds; formal cost depends on the actual number of source cases and conditions and will be recorded, not inferred from parameter count.

The old guard's 3-to-1 refutation loss is reproduced in old_guard_diagnostic.json/.md. It stems from a numeric-unknown referral policy overriding two model-negative cases; H318593_2 and N307161 have independently checkable numerical contradictions. This audit does not silently replace the old guard or retrofit its reported results.
