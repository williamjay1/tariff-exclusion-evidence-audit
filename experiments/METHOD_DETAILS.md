# Fixed local evidence-audit configuration

This document describes the experiment, not an improvement to the historical frozen models. The implementation is a post hoc revision following the supplied methodological critique. All formal inputs, references and corrections are retained with their timing.

| Element | Direct state interface | Condition audit interface |
|---|---|---|
| Checkpoint | Qwen3-14B, Q4_K_M GGUF | Same |
| Execution | Local llama.cpp CPU; six inference and prefill threads | Same |
| Native template | Applied through the server, thinking disabled | Same |
| Sampling | Temperature 0, seed 20261023, repetition penalty 1 | Same |
| Context limit | 4096 tokens; input exceeding the limit rejected before inference | Same |
| Formal clause meaning | Full, explicitly controlled two-condition clause | Identical clause, also duplicated as condition IDs and requirements |
| Facts and target | Identical numbered facts and target | Same |
| Requested output | One supported/refuted/unknown decision | Condition states, fact IDs, model decision and requested unknown-condition IDs |
| JSON constraints | Valid keys and state vocabulary | Valid keys, ID vocabulary and bounded array lengths; no reference states supplied |
| Maximum generated tokens | 48 | min(1024, 192 + 64 × number of supplied conditions) |
| Derived output | None | Fixed conjunction: any refuted dominates unknown; otherwise all supported gives supported; all other complete records give unknown |

The fixed conjunction does not rescue a false condition state or establish that an uncited refutation is trustworthy. Condition evidence and model-generated requests are scored separately. A supplied checklist is an explicit task restriction; automatic discovery of every legal prerequisite is not evaluated. The two interfaces jointly differ in instruction, structured representation and requested output, so any difference cannot be attributed to aggregation alone.

The server's JSON schema restricts syntax and candidate vocabulary. It does not enforce a particular state, factual entailment, complete coverage of all condition IDs, uniqueness of IDs, appropriate requests, or the evidence policy. The parser separately checks duplicate IDs, unknown IDs, output keys and field types. Incomplete condition coverage is retained as a separate interface failure. Formal summaries distinguish invalid, incomplete and token-capped records from the semantic state unknown.

The qualification set contains 24 ordinary-object problems and 27 conditions separate from customs materials. Its acceptance thresholds were frozen before execution: at least 23 correct decisions, at least 95% condition accuracy where applicable, no invalid/incomplete/truncated output, no unsupported affirmative decision, and correct decisive refutation with no request when an unrelated condition is missing. The direct arm has no condition/request endpoint except the decision part of that decisive-refutation test. Both arms passed. One other unknown qualification item omitted its request, and that failure remains explicit.

The original source-anchored construction had a raw-quote semantic asymmetry for two families. A three-request pilot was stopped before its predictions were inspected. Both formal arms now receive the same complete requirement sentences. The original pilot remains available and is never pooled with formal results. The subsequent wood-frame annotation erratum was identified by independent AI source review and fixed by the parent before formal outcomes were read; no input or prediction was changed.

The formal constructed diagnostic contains 108 unique inputs from twelve families. Ninety-six linked relationships share endpoints, including a restoration that reverses deletion. Its role is to test specified functions, not estimate unseen legal performance. Whole-input paired success requires both correct endpoint states and the required invariance or change. Merely retaining an incorrect or always-unknown state earns no credit. The wood-frame correction changes one condition state and permits equivalent target-frame evidence in seven records, without changing any whole-input reference or pair relation. A sensitivity analysis excludes that entire family.

The separate restoration diagnostic contains four isolated conditions in three rulings and eight before/after endpoints. Each retains the entire frozen excerpt and appends one exact admissible attribute sentence from the complete source. The two vacuum conditions share a sentence. These are post hoc source-availability probes; they do not reproduce the original applicant file or establish a whole-rule legal conclusion. Strict explicit-evidence coding of the motor condition differs from its earlier implicit interpretation and is identified separately.

All raw model replies, rendered prompts, JSON schemas, token counts, response times and source hashes are retained. Expected states, reference citations, source group IDs and administrative outcomes are not passed to the model. The final report reconstructs every submitted user prompt from whitelisted input fields and checks exact identity. All computations, logs and working copies remain on D; existing official raw documents are read from F without modification.
