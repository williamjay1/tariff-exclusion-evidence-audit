### 5.4 Controlled state, evidence and request diagnostics

Both interfaces passed qualification with 24/24 decisions; the checklist also matched 27/27 condition states. Qualification nevertheless contained a request failure: in one unknown case, it omitted the needed request despite assigning the correct state. Its request recall was 7/8 and its exact request sets 23/24. This error remained in the record because request recall was not a qualification threshold.

The formal run completed all 108 inputs in each arm without invalid, incomplete or truncated responses. Direct decisions matched 98/108 references and supplied-checklist decisions 104/108 (Table 4). Seven inputs were correct only with the checklist and one only with the direct interface. All ten direct errors and all four checklist errors occurred on reference-unknown inputs. The direct arm made ten unsupported affirmative decisions. The checklist reduced that count to three but also made one unsupported refutation. These are exact contrasts within the selected diagnostic inputs, rather than estimates of legal accuracy or an isolated effect of aggregation.

Table 4 Functional diagnostics under the corrected reference

| Endpoint | Direct decision | Supplied checklist |
|---|---|---|
| Valid, complete responses | 108/108 | 108/108 |
| Correct whole-input states | 98/108 | 104/108 |
| Unsupported supported decisions | 10/108 | 3/108 |
| Unsupported refuted decisions | 0/108 | 1/108 |
| Correct condition states | Not applicable | 211/216 |
| Acceptable fact-ID sets | Not applicable | 213/216 |
| Acceptable IDs on determinate conditions | Not applicable | 180/181 |
| Correct state and fact IDs jointly | Not applicable | 211/216 |
| Unknown conditions located | Not applicable | 31/35; one false gap |
| Necessary requests made | Not applicable | 20/24; no unnecessary requests |
| Exact request sets | Not applicable | 104/108 |
| Overall answer matches own condition aggregation | Not applicable | 108/108 |
| Correct linked relations | 84/96 | 90/96 |
| Refutation retained with another condition unknown | 11/11 | 11/11, with no request |

Counts use the actual endpoint denominator. The 216 condition records include 35 unknown states whose acceptable citation set is empty; ID-set matching alone therefore does not establish a correct evidence chain. The determinate-only and joint endpoints distinguish this issue. Necessary requests exclude unknown companion conditions after a decisive mandatory refutation. Direct outputs do not contain condition, citation or request records, so those endpoints are not scored. The 96 linked relations share endpoints. All whole-input state changes are carried by the first condition in this construction; whole-input agreement does not establish general integration of necessary conditions.

The checklist matched 211/216 condition states and the same number of joint state-and-ID references. It identified 31 of 35 unknown conditions, introduced one false gap and made 20 of 24 necessary requests. It made no unnecessary requests, but missing four necessary requests remains a substantive failure. Its final answer agreed with deterministic aggregation over its own predicted states on all 108 inputs. Internal consistency thus coexisted with four wrong whole-input answers and five wrong condition states.

The errors distinguish different failure modes. When only Product B was described as having no connectors, the checklist refuted Product A's connector requirement with an empty evidence set, instead of leaving it unknown. In a deletion input containing only a wooden-frame assertion, it used that assertion to support the non-teak condition, although wood does not identify the timber species. In the frame-species refutation-with-missing input, it correctly refuted teak eligibility but incorrectly left the wooden-frame condition unknown despite the remaining teak-frame statement. A correct overall answer therefore concealed a condition error. These failures respectively expose unsupported negation, an invalid attribute inference and missed semantic support; they are not malformed output failures.

Figure 3 separates whole-input agreement, inspectable checklist endpoints and linked behavior. Both arms succeeded on 12/12 relations for irrelevant additions, decisive changes, object-ownership swaps, equivalent expressions and preservation of a refutation. Deletion and its reverse restoration each succeeded in 10/12 families in both arms. The largest contrast concerned evidence available only for another object: 4/12 successful relations with direct decisions and 10/12 with the checklist. This narrower object-binding result accounts for the net six-answer difference. It does not imply that the checklist solves entity binding generally, as the connector error shows.

![Figure 3](../artwork/figures/figure3_controlled_diagnostics.png)

Figure 3 Controlled functional diagnostics. Panel a shows correct whole-input states for 108 constructed inputs per arm. Panel b reports condition, acceptable fact-ID, joint state-and-ID and exact-request agreement for the supplied-checklist interface under the corrected reference. ID agreement includes empty sets for unknown conditions and must be read alongside the joint endpoint. Panel c shows successful linked relations, each requiring both correct endpoints and the stated change or invariance; circles denote direct decisions and squares the supplied checklist. Every row contains 12 linked relations, and endpoints are shared across rows. The refutation-preservation row includes the frame family whose companion condition is supported after correction; the stricter refutation-with-another-unknown endpoint has 11 families, all successful in both arms. These selected templates support descriptive diagnostic counts, without population confidence intervals or a claim about complete legal reasoning.

The semantic erratum reduced condition agreement from 212/216 under the frozen reference to 211/216 under the corrected reference, and acceptable-ID agreement from 214/216 to 213/216. Overall decisions and linked-relation results did not change. Excluding all nine frame-family inputs yielded 91/99 direct decisions, 97/99 checklist decisions, 196/198 condition states and 198/198 acceptable-ID sets. The correction was retained even though it lowered the model's score. The sensitivity shows exactly where the semantic construction affects evaluation, rather than establishing one unquestionable annotation policy.

### 5.5 Behavior after restoring actual source attributes

The separate source-restoration diagnostic completed eight isolated-condition endpoints per arm. Direct decisions matched 7/8 references and checklist decisions 6/8; each arm produced the required unknown-to-supported change in 3/4 linked restorations. Both handled the cable-connector condition in H330938, the four-wheel condition in H322923 and the motor-power bound in H340899. The remaining self-contained-motor condition failed in both interfaces. These counts refer to four condition relations supported by three source sentences from three rulings, without an estimate of performance across complete customs cases.

For the failed motor relation, the frozen product description did not explicitly establish the strict reference condition. The appended source sentence then explicitly described self-contained electric motors. The direct arm remained unknown at both endpoints. The checklist returned refuted at both, citing the initial description before restoration and both facts afterwards. Its two unsupported refutations are retained as failures to track the admitted assertion, without inferring an unobserved reasoning process from the answer. The checklist matched 6/8 state-and-ID references, made three of four necessary requests and made no unnecessary requests. Its exact request sets were 7/8, because the wrong refuted answer after restoration still had the same empty request set as the supported reference.

Source repair therefore supplies an input whose effect can be tested; it does not guarantee an appropriate model update. This diagnostic also shows why the formal checklist contrast cannot be generalized to every source input: the checklist had one fewer correct endpoint here, despite its higher controlled-input count. The motor condition had already been inferred as supported in the historical coding, whereas this before–after task uses the declared stricter direct-text policy. The four restorations must consequently remain distinct from a claim to have corrected four historical unknowns.
