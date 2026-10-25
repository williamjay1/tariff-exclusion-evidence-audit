# Auditing evidence construction in legal AI evaluation: a source to input protocol for tariff exclusion decisions

Junjie Zhang (a,b)

a Shanghai Academy of Global Governance & Area Studies, Shanghai International Studies University, Shanghai 201620, China

b School of Economics and Finance, Shanghai International Studies University, Shanghai 201620, China

Corresponding author: Junjie Zhang, junjiezhang2024@shisu.edu.cn

ORCID: 0009-0004-8821-4018


## Abstract

Legal AI systems are evaluated on documents written for administrative decisions, and the way such a document becomes a model input decides what can count as evidence. We present a source to input audit protocol that records, for every condition of a rule, the governed product, the signed requirement, the source span, the statement class, the admission policy and the interpretation option, so that an evidence state can be recomputed from a named input version. Applied to 67 US customs rulings and 208 inherited condition units, the protocol attributes each unresolved state to a cause: among 67 unresolved conditions inside 47 historically unresolved cases, restoring an omitted public sentence settles 4, a declared interpretation option settles 17, and 47 persist under every operation recorded here. Declared interpretation packages support 10, 17 and 19 of 58 conjunctive cases. A qualified local model on 108 constructed inputs shows that two output contracts produce different failure profiles, which whole case accuracy conceals. The protocol turns evidence labels into inspectable and recalculable objects, a precondition for comparing legal AI systems.

Keywords: legal AI evaluation; evidence construction; source provenance; customs rulings; tariff exclusions; evaluation validity

## 1 Introduction

Legal AI evaluation usually begins with a text and a label. The text is shorter than the document it came from, and the label records a conclusion that the document reached. The arrangement is convenient, and it hides a decision about which statements of the original document were admitted as evidence. In an administrative decision that decision is consequential. The same document carries product descriptions, submissions by interested parties, technical definitions, findings, application reasoning and a disposition. A benchmark builder who removes the holding to prevent answer leakage can remove a descriptive fact in the same operation. The resulting task then tests an inference from a shortened input against a conclusion drawn from the complete one.

Tariff exclusion applicability is a bounded instance of the problem. The scope of an exclusion is governed by its published tariff code and product description, and a qualifying product can benefit even when it was not the original requester [1]. A product may therefore have a known classification and still require assessment against a published description. The distinctions that matter are relational: whether a cable has connectors, whether a capacity refers to lifting or to collection, whether a material restriction governs a conducting core or a shield, whether two ratings belong to two products or to two operating roles. The institutional scale is large, with about 53,000 exclusion requests reported for 2018 to 2020 [2], and that figure concerns the creation of exclusions rather than the later assessment of transactions against a published description.

The computational ingredients are established. ContractNLI asks for entailment, contradiction or unmentioned information together with evidence spans [3]. Holzenberger and Van Durme connect statutory information extraction to symbolic reasoning, comparing predicted, partially supplied and empty knowledge bases [4]. Medvedeva and McBride explain why facts selected in a completed judgment need not represent the information available before a decision [5]. Evaluations of tax assistance [6] and of legal discrepancies [7] show the value of verifiable questions and controlled perturbations, and behavioral testing supplies the design principle for invariance and directed change [8]. This work uses those ingredients and adds a layer they leave implicit: the provenance and the admission policy of the statements that become the input.

That layer matters because one label can stand for several different situations. A condition can end as unknown in three ways. The input can omit a statement that the source contains. The source can lack the attribute altogether. A declared interpretation can be withheld, leaving a mapping undecided. The first is an artifact of input construction, the second is a limit of the public record, and the third is a policy choice. Each calls for a different action: restore the statement, request the fact, or adopt and defend a mapping. A single unknown label does not separate them, so a system that reports the label cannot be corrected at the right point.

The retained collection contains a direct instance. In ruling H330938 the candidate exclusion requires cables without connectors. The frozen input described the conductors and the voltage rating and left the connector condition unresolved. The complete ruling states, in its analysis, that the submitted documentation “describes the subject cables as imported on reels at very long lengths without connectors”. Restoring that sentence moved the condition from unknown to supported without any change to the legal question. The reference state of a product depends on which sentences were admitted, and the label never says which. Across the retained cases, source restoration settles 4 of the 67 unresolved conditions inside the 47 historically unresolved cases, a declared interpretation option settles 17, and 47 remain unresolved under every operation recorded here.

The contribution has three parts. A record schema and protocol link every condition to its rule span, object, attribute, statement class, admitted input version and interpretation option, so that a state can be recomputed rather than asserted. An attribution assigns each unresolved state to omission, evidentiary silence, interpretation or binding, with counts for the retained collection. A functional diagnostic shows that condition state, citation and request can be scored separately, and that a high whole case score can coexist with wrong condition states and missing requests.

The functional evaluation uses a qualified local interface as a demonstration that the audit categories are operationally separable, and it is not an assessment of model capability. The audit makes no claim about legal correctness, about administrative outcomes or about professional utility; those belong to expert adjudication and field observation that this study does not perform.

## 2 The task and the evaluations it can be compared with

### 2.1 Product scope after classification

The module takes a target product description, a supplied base classification and a candidate exclusion description, and asks which product requirements the admitted text establishes, contradicts or leaves open. Candidate retrieval, temporal validity and classification are upstream inputs. The output is a condition audit and, where a defensible logical representation exists, a conclusion supported by the admitted input with a specific information request attached. It is not a recommendation to file an entry or claim a refund. A classification error or an expired exclusion cannot be repaired by satisfying product description conditions.

This boundary matters when relating the work to customs AI. Explainable product classification [9] and recent hierarchical or graph based benchmarks [10, 11] examine the assignment of codes and the rules used in that assignment. In this study the candidate code is supplied, and a compatible code does not settle a narrower description inside it. The diagnostics reported below therefore cannot be read as evidence that upstream classification has been solved. An interface between the modules has to retain the exact tariff level and the historical version used in a ruling.

Institutional scale does not supply the missing task level evidence. The reported exclusion requests concern the creation of exclusions, not the number of later transactions assessed against an already published description. No transaction distribution and no importer workflow is observed in these materials, so the figure describes the setting and is not used to estimate the frequency, exposure or labour cost of the module studied here.

### 2.2 What neighbouring evaluations establish

ContractNLI is a close antecedent because its task combines inference over three states with evidence identification. Its 607 nondisclosure agreements and 17 hypotheses also show that evidence can be discontinuous and that exceptions complicate entailment at document level [3]. The distinction here is not the addition of an unknown class. It is the audit of how a public decision becomes an input, including the provenance and statement role of information outside a section selected as factual.

Holzenberger and Van Durme provide the closest extraction and reasoning comparison. Their statutory tax task represents entities, events and attributes in a knowledge base consumed by a Prolog reasoner, and the predicted, partially supplied and empty knowledge base conditions locate representation losses [4]. They also discuss ambiguity and revisions to selected cases. Their work rules out any claim that separating extraction from execution, or binding values to entities, is itself new. The extension here concerns admission and attribution in an administrative source: whether an attribute was supplied, clipped, definition dependent or disputed before a reasoner receives it.

Medvedeva and McBride distinguish retrospective judgment classification from a genuine future outcome task, since removing the holding does not reverse the writer's selection of facts [5]. Source restoration addresses a narrower problem inside retrospective materials. It can repair a lost descriptive assertion and cannot reconstruct the original dossier or remove the writer's knowledge of the outcome.

The VITA study uses 130 tax questions and 260 variants that preserve the answer, with expert construction of answer references, to evaluate assistance with returns [6]. Its expert answer process is stronger than the legal validation available here, and it is the comparison that keeps the present validation claim modest. Evaluations of legal discrepancy examine omission, terminology and structural changes to legal text [7]. TriBench organizes judicial risks across tasks and includes attorney review of materials derived from sources, and it remains a preprint in the version examined [12]. Legal omission testing and risk oriented evaluation therefore predate this work. The contribution is a record of source roles and alternative admitted input versions through which an apparent information deficit can be attributed and contested.

Behavioral testing supplies the design principle for the functional demonstration [8]. The design specifies transformations that should preserve a correct answer together with transformations that should change it. Because the structured interface receives conditions, it does not test automatic recovery of a complete legal rule. Its additional outputs make particular failures observable: an answer can be correct while its request is missing, and a cited fact can belong to another product. Those failures stay visible when overall accuracy is high.

## 3 Sources and the evidence audit

### 3.1 Collection and units of analysis

The historical discovery process retained 2,482 retrieved documents, produced 102 candidate records, constructed 86 product and exclusion pairs and kept 73 pairs for a compatible code analysis. This was iterative, purposive discovery assisted by AI search. The retained artifacts do not contain a complete contemporaneous screening log for every retrieved item, and the earlier reduction to the candidate collection cannot be reconstructed as an exhaustive eligibility screen. The 2,482 documents are not 2,482 confirmed applicability decisions. Retrieval and selection records are preserved, and no claim is made about recall or inclusion probabilities.

The 73 pairs come from 67 rulings and 41 linked rule groups, using public snapshots retrieved on 7 October 2026 [13]. Twenty seven pairs are headquarters rulings and 46 are New York rulings. Several pairs can share a ruling or an exclusion family, and those dependencies differ from the 208 historical condition units, the 397 index entries and the constructed diagnostic endpoints. Table 1 states the units and their permitted uses. Repeated products, shared clauses and reverse intervention pairs are not counted as additional independent observations.

Table 1 Sources and analytical units

| Material | Retained unit and count | Analytical use |
|---|---|---|
| Historical discovery | 2,482 retrieved documents; 102 candidates | Provenance of purposive discovery, with incomplete contemporaneous screening |
| Curated collection | 86 product and exclusion pairs | Historical case construction and inventory matching |
| Compatible code audit | 73 pairs, 67 rulings, 41 linked groups | Source audit and restricted input interpretation |
| Historical decomposition | 208 condition units | Uniform source, object, attribute and interpretation records |
| USTR index of 17 January 2024 | 397 entries | Version specific structural context and coverage audit |
| Independent qualification | 24 cases, 27 conditions | Basic interface suitability before formal diagnostics |
| Constructed diagnostics | 108 unique inputs, 12 source families | Controlled state tracking under supplied semantics |
| Source restoration diagnostics | Four conditions in three rulings, eight endpoints | Before and after behavior for directly recoverable attributes |

A stricter subset that requires exact string agreement contains 60 pairs. The 13 removed pairs all come from headquarters rulings, with two eligible and eleven ineligible administrative outcomes, and all 46 New York pairs remain. Each removed pair has an eight digit product code against a ten digit candidate statistical code. Historical ten digit classification certainty is not inferred from those strings. The stricter filter changes source, class and rule group composition together and serves only as a documented sensitivity.

For every pair the applicable rule text is the candidate exclusion quoted in that ruling, and it is not replaced with the wording of the 2024 index. The index contains 41 single code entries, two date dependent code transitions and 354 product descriptions [14]. A semantic reading produced with AI assistance selects 1,096 coarse requirement groups inside the descriptions, preserving local alternatives, exceptions and component lists inside their groups. That is a declared representation granularity rather than a count of legally atomic conditions. Normalized exact description matching links 21 of the 86 pairs to 16 index entries, and 16 of those pairs belong to the 73 pair audit. Matching establishes a conservative textual intersection and neither temporal equivalence nor complete historical coverage. Unconfirmed similar clauses remain candidates.

### 3.2 Statement roles and source admission

![Figure 1](../artwork/figures/figure1_source_protocol.png)

Figure 1 Source to input evidence audit. Descriptive assertions retain statement class and provenance, while interpretations, application reasoning and outcomes are recorded separately. The protocol represents the condition, object and attribute relation before computing a state or an information request. Whole case conjunction is used only where the audit represents the conditions as jointly necessary under the stated interpretation policy; unresolved alternatives and exceptions require their own representation.

Figure 1 presents the protocol. The complete retained official text is the source, and the model input is a versioned selection from it. The audit distinguishes descriptive attributes attributed to a party, laboratory findings, agency stated product attributes, definitions or category explanations, application reasoning and the final outcome. A section heading is not an admission rule. A sentence in an analytical section can contain a separable description of a connector, a motor or a wheel count, and a sentence in a factual section can merely repeat a party's proposed legal characterization.

The frozen excerpt is preserved unchanged. A restored version appends only descriptive attributes admitted under the stated direct text policy. Exact character offsets and paragraph identifiers locate the original assertion. Where a retained quotation joins nonadjacent product descriptions, separate continuous spans locate its members and the joined excerpt is not presented as a continuous source quotation. Attribution to a submitted document is retained even when the agency reports it in its reasoning. Such provenance establishes that the public text contains the assertion, and it does not establish that the physical property was independently measured.

An attributed assertion that is contested, or that restates the requested exclusion, is not promoted to a verified attribute. The record keeps its source and the policy needed to use it. Definitions and conclusions can be consulted to identify an interpretation problem, and they are not inserted into an attribute only input as evidence that the product satisfies the rule. This avoids two equally problematic alternatives: discarding every analytical sentence, or importing the full legal answer.

### 3.3 Condition records, reference layers and aggregation

Each of the 208 records contains the literal rule quote, product or component, signed predicate, attribute, logical role, quantifier and scope, unit or measurement basis where relevant, factual quote and locator, historical coding, direct text excerpt and restored states, inference basis, unknown cause and explicit interpretation options. Historical units are not asserted to be atomic or complete. A unit can contain local alternatives, an illustrative list or a nested exception, which is recorded rather than flattened into positive requirements.

Supported, refuted and unknown describe textual evidence under a stated admission and interpretation policy. A negative requirement is a signed predicate: explicit connector absence supports the condition that the product is not fitted with connectors, explicit connector presence refutes it, and silence leaves it unknown. Invalid output is an interface status and never a fourth form of legal uncertainty. A nonbinding example or permission is marked not applicable for mandatory condition scoring.

The audit has four reference layers. Direct records concern an explicitly stated attribute with a simple comparison, unit conversion or discrete membership check. Interpretive records require a technical definition, product category, functional equivalence or scope mapping beyond that comparison. Insufficient records lack an admitted attribute in the relevant input, and the source search determines whether the gap can be repaired. Disputed records retain conflicting assertions or unresolved object, quantifier or definition choices. Layer assignment concerns the frozen input and is preserved even when a newly admitted direct assertion changes a restored condition state.

Unknown is accompanied by a cause. Missing product attributes, omitted source statements, unavailable incorporated definitions, unresolved categories, object or measurement scope mismatches, conflicting sources and disputed annotations call for different actions. A missing wheel count can motivate a factual request. A dispute about whether a backpack vacuum belongs to the legal class of upright cleaners cannot be resolved by requesting a number. Causes may overlap inside a case, and their counts do not partition the 47 historically unknown pairs.

For safe mandatory conjunctions a verified refutation determines refutation, all supported conditions determine support, and the remaining combinations are unknown. The rule concerns the evidence states of genuine necessary conjuncts. It does not justify accepting an unverified negative model answer and it does not convert a local disjunction into a conjunction. Fifteen pairs stay outside this aggregator because their historical units contain alternatives, exceptions, illustrative lists or unresolved composite object scope. Condition records remain available for those pairs.

### 3.4 What the audit establishes, and what it leaves open

The protocol supports three kinds of claim, and each is checked in a different way.

Mechanical claims are the first kind. A rule quotation occupies a locator in the official snapshot, a frozen fact occupies a continuous character range, a hash identifies the version, and an aggregation over stated condition states can be recomputed. Verification covered all 208 rule spans, 228 frozen fact spans expanding to 231 continuous source ranges, 455 continuous spans in total, 16 recovered attribute spans and the snapshot hashes of 67 rulings. A failure at this level is detectable without judgment.

Interpretive claims are the second kind. The decomposition of a description into conditions, the assignment of a reference layer and the list of interpretation options are judgments produced with AI assistance. Their warrant is inspectability: a reader can examine the quotation, the object and attribute, the option and its consequence, then replace a mapping and recompute. A challenge is answered by rerunning the record, not by appealing to the annotator. The frame species correction reported in Section 4.3 is an instance in which this procedure caught an error that span matching alone had passed.

Claims about legal correctness, outcome prediction and professional utility are outside the study. Those require expert adjudication and field observation, and their absence limits what the retained counts can mean. The value of the interpretive layer is that it makes such questions askable at a specific location, with a specific quotation and a specific policy attached.

The coding was performed with AI assistants in October 2026, using the GPT-6 family through Codex without an exposed immutable snapshot identifier. The assistants performed source coding, parallel semantic review, and separate provenance and arithmetic checks. The auditors had access to earlier project materials and to administrative outcomes, so this is an outcome exposed audit. The administrative disposition was excluded as a criterion for accepting a textual evidence state. No customs or trade law expert independently validated the records, and agreement among AI coders measures the repeatability of a procedure rather than its legal validity. Shared model lineage allows shared mistakes, and the relay example in Section 6.3 is one.

## 4 Functional evaluation

### 4.1 Qualification and frozen interface

Four development cases check the implementation. Twenty four separate qualification cases contain 27 conditions across ordinary attributes, bounds, intervals, explicit negation, object binding, measurement basis and conjunction, and they do not use the formal customs materials. The decision gate was fixed before qualification at 23 of 24 correct decisions or better, no invalid or truncated responses, no unsupported affirmative decisions, and correct handling of a decisive refutation alongside another missing requirement. The checklist arm additionally required 95 percent condition accuracy or better. Request recall was measured and did not serve as a qualification threshold.

The fixed model order was Qwen3-14B [15], followed by Granite-3.3-8B if necessary. Qwen3-14B passed in the first qualified configuration, so the fallback was not selected. Passing these checks establishes basic interface function on the qualification cases and leaves behaviour specific to customs untested on the formal inputs. Every development and qualification attempt is retained, including request errors. The qualification inputs, prompts, schemas and thresholds are versioned separately from the formal collection.

Inference uses a Q4_K_M GGUF checkpoint whose official hash was verified, a local llama.cpp server [16], native chat templates, disabled thinking, temperature zero, seed 20261023, a 4,096 token context and six CPU threads. No API judge supplies reference answers. The output grammar constrains JSON structure and allowed identifiers, and it leaves the factual states, the cited evidence, the condition coverage and the requests to the model. The parser and evaluator record missing or duplicate identifiers, incomplete coverage, absent evidence for a determinate state, unsupported citations and generation limits. The supplement provides software and checkpoint manifests, prompts, raw responses and elapsed compute times.

### 4.2 Common semantic input and controlled changes

The direct arm receives the target, the complete controlled clause and numbered facts, and returns a decision in the three states. The checklist arm receives the same semantic content plus a structured duplicate of the two requirements and their identifiers, and returns per condition states, cited fact identifiers, an overall decision and requested unknown condition identifiers. This is a supplied checklist diagnostic. Neither arm is credited with discovering a complete exclusion rule, and the contrast includes representation and output demands rather than isolating one causal prompt ingredient.

Twelve source clauses, each from a different historical rule group, anchor the formal construction. They cover connectors, lifting capacity, motor power, single use, precious metal plating, textile fraction, granule diameter, instrument mass, electrical power, frame species, propulsion power and fireplace mass. Each contributes two selected requirements and nine synthetic inputs, and the complete original clause with selected quote spans remains in provenance. The controlled clause states the supplied interpretation explicitly, so every granule quantification and the teak scope specific to the frame family are assumptions of the diagnostic rather than validated readings of a full exclusion.

The nine variants comprise a complete base, deletion of the unique supporting fact, an irrelevant addition, a decisive contrary attribute, retention of that contradiction while another fact is removed, an object binding original, its ownership swap, a semantic or unit equivalent, and evidence about another product only. That yields 108 unique inputs with 48 supported, 36 refuted and 24 unknown expected decisions. Eight linked relations per family yield 96 relations. Restoration reverses deletion using an already evaluated base endpoint and is not an additional independent input. Source families share a construction template, so twelve families do not imply twelve independent legal populations.

The first condition carries the whole case state changes in this construction, and the second tests companion state tracking and the suppression of requests after a decisive refutation. Whole case accuracy therefore cannot establish general integration of every necessary condition. The formal claim rests on the condition, evidence, request and paired change endpoints actually exercised.

An input audit before outcomes were examined found that short literal fragments left two interpretations more explicit in the checklist arm, so the complete canonical clause was supplied to both arms. Three responses from the superseded input pilot were preserved, excluded from the formal analysis and not used to choose the model or the prompt. The semantically aligned 108 inputs and the protocol were hashed and frozen before the formal run. That is a documented input semantic correction rather than a claim of preregistration, and it is not a claim that the collection was unseen by the researchers.

A separate semantic audit during inference identified an annotation defect in the frame species family. In the variant that retains a refutation while a companion fact is missing, a teak frame statement also supplies evidence that the frame is wooden, so removing a separate wooden frame sentence did not remove every support for that condition. Frozen inputs and predictions are preserved. An outcome independent erratum changes that one condition state and permits either valid supporting fact, or both, for the seven affected citation endpoints. Corrected and frozen reference scores are both retained, with a sensitivity that excludes all nine inputs of that family. Reference decisions are unchanged. The decisive refutation with another unknown diagnostic has eleven valid families after correction. The incident also shows why span matching alone cannot establish semantic label validity.

### 4.3 Endpoints, reference policy and the source probe

Decision agreement is accompanied by condition state agreement, complete condition coverage, correct evidence identifier binding, missing condition localization, request precision and recall, unsupported affirmative or refuting conditions and case conclusions, and unnecessary requests. A required gap omitted from the requested set counts as a substantive request failure even when every schema field is present. No request is necessary once a credible mandatory contradiction settles the conjunction. Unnecessary requests include asking for an established property and continuing after such a refutation.

Pair success requires both endpoints to be correct and to exhibit the specified relation. For an invariant addition or an equivalent unit, two equally wrong answers fail. For deletion, restoration, decisive change or object swap, two identical unknown answers fail. The overall decision is retained separately from deterministic aggregation over the model's own predicted conditions, which exposes a disagreement between condition reasoning and the final answer.

The short interface requires empty evidence for unknown, so it cannot encode partial support, competing factual claims or the richness of the audit cause fields. Contradictory source reports mark the boundary of the ordinary constructed task rather than a solved capability. The functional experiment concerns explicit controlled statements and supplied conjunctive requirements.

Counts are reported with their actual denominators, and family level patterns are examined. Population confidence guarantees are not attached to the purpose built templates, and the 96 linked relations are not treated as independent trials. Historical resampling results describe variation inside the selected corpus and do not correct unknown inclusion probabilities. Previously inspected numeric repairs remain development demonstrations, and neither bootstrap resampling nor new random seeds can convert those materials into independent validation.

## 5 Results

### 5.1 The audit reconstructs condition evidence

The 208 historical units divide into 132 direct, 45 interpretive, 19 insufficient and 12 disputed records. Two direct units are nonbinding: an illustrative list and a permission expressed with the phrase whether or not. That leaves 130 scorable direct units. The stratification changes what literal attributes and simple relations can evaluate, and it prevents a dispute about the meaning of a legal category from being scored as an incorrectly compared number.

Figure 2 separates the layer assignment from the state under each admitted input version. The strict excerpt policy yields 125 supported, 5 refuted and 76 unknown conditions with 2 not applicable, and direct source restoration yields 129 supported, 5 refuted and 72 unknown. The four changes occur in three cases: connector absence in H330938, four wheels in H322923, and a motor supplied as a single unit together with a 1,500 W ceiling in H340899. The motor relation had been inferred as supported in the historical coding, and the other three had been historically unknown. The restoration count therefore depends on the reference policy against which it is compared.

All four restored relations are local corrections, and none alone resolves its whole case. Restricting aggregation to the 58 safe outer conjunctions gives 10 supported, 3 refuted and 45 unknown cases, unchanged by direct restoration. The remaining 15 pairs are logic unresolved and stay outside these state totals. Against the historical coding of 21 supported, 5 refuted and 47 unknown, five supported cases become strict unknown and six require a richer logic representation, while two historical refutations fall outside the simple aggregator. These movements follow a stricter representation and admission policy, and they are not evidence that the administrative outcomes were wrong.

Independent verification located all retained rule quotations, checked the raw snapshot hashes of 67 rulings and validated 455 continuous evidence spans. Two joined product excerpts receive separate original spans in place of a fictional continuous locator. The checks establish the provenance needed to inspect the audit and leave the semantic mapping open to criticism.

![Figure 2](../artwork/figures/figure2_source_audit.png)

Figure 2 Condition layers and the effect of direct source restoration. Panel a classifies the 208 inherited condition units by the evidence demands of the frozen input. Panel b shows their states under the strict direct text policy before and after admitted attributes are restored. Coding layers stay fixed while restored states can change. The counts describe the retained units rather than a population prevalence or an expert validated accuracy estimate.

### 5.2 Unresolved states have three different repair paths

Table 2 attributes the 67 strict unknown conditions to the cause recorded for each unit and adds what could settle it. The table answers a question the aggregate state cannot: whether the evidence fails because the input was clipped, because the public record is silent, or because a mapping was withheld.

Table 2 Causes of unresolved evidence and the operations that can settle them

| Cause recorded for the condition | Cases containing the cause (of 47) | Strict unknown units | Settled by source restoration | Settled by a declared option | Settled by neither |
|---|---:|---:|---:|---:|---:|
| Descriptive information omitted from the excerpt | 5 | 7 | 4 | 1 | 3 |
| No sufficient independent attribute in the public source | 10 | 12 | 0 | 0 | 12 |
| Definition, category or use mapping | 36 | 38 | 0 | 12 | 26 |
| Object, component or measurement scope | 11 | 12 | 0 | 3 | 9 |
| Source conflict or competing interpretation | 5 | 5 | 0 | 3 | 2 |

The first feature is that the causes are not interchangeable. Omission is repairable from the source itself, and 4 of the 7 units in that group acquired a determinate state when the descriptive sentence was restored. No unit in the absent attribute group did, because the public ruling holds no sentence to restore. Definition, category and use problems are partly manageable by declaring an option (12 of 38 units) and otherwise depend on a rule source or an adjudicated meaning. The second feature is that the operations differ in reach across the 67 units: restoration settles 4, a declared option settles 17, one unit is settled by either, and 47 are settled by neither. The category counts overlap, so the rows sum to more than 67 and the column entries are not a partition.

The reach of the operations differs by more than a factor of ten. Input construction is the smallest category in this collection and the interpretation category is the largest, which is an argument about where an evaluation should spend its validation effort and the opposite of what a single unknown count suggests.

The case level shows the same structure. Of the 40 safe conjunctions inside the 47 historical unknowns, the declared technical package moves 7 cases out of unknown, 2 to support and 5 to refute, and the alternative package moves 6, 4 to support and 2 to refute. Between 33 and 34 of the 40 stay unresolved under whichever package is declared. A reference that reports unknown therefore marks a mixed set: a small repairable part, a policy dependent part, and a large residual part that depends on evidence or authority outside the record.

For an evaluation the practical consequence is that an unknown answer is neither an error nor a correct abstention until the audit says which operation produced the reference state. The connector ruling in Section 6.1 is the minimal case, where the same product and the same rule yield a supported reference once one sentence is restored. A benchmark that had drawn its reference from the complete ruling while supplying the clipped text would have recorded a failure of legal reasoning at a point where the input could not support any other answer. That mechanism follows from the selection of sections in general, whatever its frequency in this collection.

The omission group is broader than the repaired set, and the residual cases show why. The wireless condition in H341677 still needs a declared meaning of wireless enabled. In H314080 the width and areal mass intervals repeat the protesting party's proposed description, and they remain attributed claims with an explicit acceptance option. Attribution alone is not an exclusion rule, as the submitted document assertion admitted in H330938 also shows. Only four relations meet the stated direct restoration policy. Conversely, the absence of a sufficient attribute means that this public ruling supplies no independent assertion, and it does not mean the technical document or the physical fact cannot exist elsewhere.

The largest case set concerns definitions, categories or use, and its 36 cases show that generic requests for more specifications would often target the wrong problem here. An information request needs an action type. A missing mass can be requested from a product dossier, an incorporated definition has to be retrieved and interpreted, and a conflict between a laboratory report and a party submission needs a source priority decision. Reporting unknown without that distinction does not explain how review could proceed.

### 5.3 Interpretation policy changes the reference

The 58 safe conjunctions were recomputed under three fully specified interpretation packages. The strict package withholds unresolved mappings. A technical scope package admits the listed monopolar system and conducting core readings, selected use and material mappings, laboratory priority for glove composition and peak output for a motor. An alternative package changes material and use scope, upright orientation, party priority over the laboratory and nominal output over peak output. Unreported attributes and interpretations without a recorded option stay unresolved. No package is selected to maximize agreement with an administrative result.

Table 3 Joint interpretation policy sensitivity in the 58 safe conjunctions

| Declared package | Supported | Refuted | Unknown |
|---|---:|---:|---:|
| Withhold unresolved interpretations | 10 | 3 | 45 |
| Listed technical scope, laboratory priority and peak output | 17 | 8 | 33 |
| Listed alternative material and use scope, party priority and nominal output | 19 | 5 | 34 |

The three rows describe the same 58 cases and differ only in declared mapping. Two evaluations that report supported counts for this collection can therefore disagree by a factor of almost two while using identical source text and identical admitted facts. A reported count is conditional on the mapping, and a report that omits the mapping cannot be reproduced, which is a requirement of evaluation validity rather than a remark about sensitivity.

Separate enumeration by case gives marginal envelopes of 10 to 20 supported, 3 to 9 refuted and 33 to 45 unknown. These are not three jointly attainable ranges, probabilities or bounds over every reasonable interpretation. Their function is to identify which recorded mapping changes a result. H330938, for example, can be supported, refuted or unknown under different declared material and topology choices after its connector fact is restored.

The inventory analysis supplies structural context for those choices. All 397 entries were read under a common annotation scheme. The 354 product descriptions contain 1,096 source anchored coarse groups, and the 43 entries that consist only of a code add no physical product groups while retaining their classification and date gates. Component dimensions, alternative outputs, lists and conditional guards stay inside their declared groups. Thirteen entries are marked unresolved under this reading, and a source wording anomaly such as a shelf width printed as 183 m is preserved rather than silently corrected. The records support inspection of rule structure, and they establish neither a prevalence of difficult transactions nor a complete executable ontology. Only 16 of the 397 entries have normalized exact description matches in the case collection, which further limits coverage claims.

### 5.4 State, citation and request are separately observable

Both interfaces passed qualification with 24 of 24 decisions, and the checklist also matched 27 of 27 condition states. Qualification still contained a request failure: in one unknown case the needed request was omitted although the state was correct. Request recall was 7 of 8 and exact request sets were 23 of 24. The error remained in the record because request recall was not a qualification threshold.

The formal run completed all 108 inputs in each arm without invalid, incomplete or truncated responses. Direct decisions matched 98 of 108 references and supplied checklist decisions matched 104 of 108 (Table 4). Seven inputs were correct only with the checklist and one only with the direct interface. All ten direct errors and all four checklist errors occurred on reference unknown inputs. The direct arm made ten unsupported affirmative decisions, and the checklist reduced that count to three while adding one unsupported refutation. These are exact contrasts inside the selected diagnostic inputs, and they are not estimates of legal accuracy or an isolated effect of aggregation.

Table 4 Functional diagnostics under the corrected reference

| Endpoint | Direct decision | Supplied checklist |
|---|---|---|
| Valid, complete responses | 108/108 | 108/108 |
| Correct whole case states | 98/108 | 104/108 |
| Unsupported supported decisions | 10/108 | 3/108 |
| Unsupported refuted decisions | 0/108 | 1/108 |
| Correct condition states | Not applicable | 211/216 |
| Acceptable fact identifier sets | Not applicable | 213/216 |
| Acceptable identifiers on determinate conditions | Not applicable | 180/181 |
| Correct state and fact identifiers jointly | Not applicable | 211/216 |
| Unknown conditions located | Not applicable | 31/35, one false gap |
| Necessary requests made | Not applicable | 20/24, no unnecessary requests |
| Exact request sets | Not applicable | 104/108 |
| Answer matches own condition aggregation | Not applicable | 108/108 |
| Correct linked relations | 84/96 | 90/96 |
| Refutation retained with another condition unknown | 11/11 | 11/11, with no request |

Counts use the actual endpoint denominator. The 216 condition records include 35 unknown states whose acceptable citation set is empty, so identifier matching alone does not establish a correct evidence chain. The determinate only and joint endpoints separate that issue. Necessary requests exclude unknown companion conditions after a decisive mandatory refutation. Direct outputs contain no condition, citation or request records, and those endpoints are therefore not scored. The 96 linked relations share endpoints, and the whole case state changes are carried by the first condition, so whole case agreement does not establish general integration of necessary conditions.

![Figure 3](../artwork/figures/figure3_controlled_diagnostics.png)

Figure 3 Controlled functional diagnostics. Panel a shows correct whole case states for 108 constructed inputs per arm. Panel b reports condition, acceptable fact identifier, joint state and identifier, and exact request agreement for the supplied checklist interface under the corrected reference. Identifier agreement includes empty sets for unknown conditions and is read alongside the joint endpoint. Panel c shows successful linked relations, each requiring both correct endpoints and the stated change or invariance; circles denote direct decisions and squares the supplied checklist. Every row contains 12 linked relations, and endpoints are shared across rows. The refutation preservation row includes the frame family whose companion condition is supported after correction, while the stricter refutation with another unknown endpoint has 11 families that both arms completed. These selected templates support descriptive diagnostic counts without population confidence intervals.

The checklist matched 211 of 216 condition states and the same number of joint state and identifier references. It identified 31 of 35 unknown conditions, introduced one false gap and made 20 of 24 necessary requests. It made no unnecessary requests, and four missing necessary requests remain a substantive failure. Its final answer agreed with deterministic aggregation over its own predicted states on all 108 inputs. Internal consistency therefore coexisted with four wrong whole case answers and five wrong condition states.

The errors distinguish different failure modes. When only product B was described as having no connectors, the checklist refuted product A's connector requirement with an empty evidence set instead of leaving it unknown. In a deletion input containing only a wooden frame assertion, it used that assertion to support the condition that the frame is not made of teak although wood does not identify the timber species. In the variant that keeps a refutation while a companion fact is missing, it correctly refuted teak eligibility and then left the wooden frame condition unknown despite the remaining teak frame statement. A correct overall answer concealed a condition error. These are unsupported negation, invalid attribute inference and missed semantic support, and none of them is a malformed output.

Figure 3 separates whole case agreement, inspectable checklist endpoints and linked behaviour. Both arms succeeded on 12 of 12 relations for irrelevant additions, decisive changes, object ownership swaps, equivalent expressions and preservation of a refutation. Deletion and its reverse restoration each succeeded in 10 of 12 families in both arms. The largest contrast concerned evidence available only for another object, with 4 of 12 successful relations under direct decisions and 10 of 12 under the checklist. That object binding result accounts for the net six answer difference, and it does not imply that the checklist solves entity binding in general, as the connector error shows.

The semantic erratum reduced condition agreement from 212 of 216 under the frozen reference to 211 of 216 under the corrected reference, and acceptable identifier agreement from 214 of 216 to 213 of 216. Overall decisions and linked relation results were unchanged. Excluding all nine frame family inputs yielded 91 of 99 direct decisions, 97 of 99 checklist decisions, 196 of 198 condition states and 198 of 198 acceptable identifier sets. The correction was retained even though it lowered the model's score, which locates the semantic construction inside the evaluation instead of asserting one unquestionable annotation policy.

### 5.5 A restored attribute tests whether behaviour follows the input

The separate source restoration diagnostic completed eight isolated condition endpoints per arm. Direct decisions matched 7 of 8 references and checklist decisions 6 of 8, and each arm produced the required change from unknown to supported in 3 of 4 linked restorations. Both arms handled the cable connector condition in H330938, the condition on four wheels in H322923 and the motor power bound in H340899. The remaining motor condition failed in both interfaces. The counts refer to four condition relations supported by three source sentences from three rulings, and they carry no estimate of performance across complete customs cases.

For the failed motor relation the frozen product description did not explicitly establish the strict reference condition, and the appended source sentence then described electric motors supplied as a single unit. The direct arm stayed unknown at both endpoints. The checklist returned refuted at both, citing the initial description before restoration and both facts afterwards. Its two unsupported refutations are retained as failures to follow the admitted assertion, without inferring a reasoning process from the answer. The checklist matched 6 of 8 state and identifier references, made three of four necessary requests and made no unnecessary requests. Its exact request sets were 7 of 8 because the wrong refuted answer after restoration carried the same empty request set as the supported reference.

Source repair supplies an input whose effect can be tested, and it does not guarantee an appropriate model update. The diagnostic also shows why the formal checklist contrast cannot be generalized to every source input, since the checklist had one fewer correct endpoint here despite its higher controlled input count. The motor condition had been inferred as supported in the historical coding, while the before and after task uses the declared stricter direct text policy. The four restorations therefore stay distinct from a claim to have corrected four historical unknowns.

### 5.6 Earlier experiments in brief

The historical numerical study remains informative when its representation boundary is explicit. In 33 selected pairs from 16 groups, source coded rules and fields reproduce all 33 encoded local states. Automatic rule parsing with reference fields matches 30, and automatic fields with either rule representation match 17. Removing the largest family, which supplies 15 pairs, leaves 18, 15, 9 and 9 matches respectively, so the representation loss persists after that exclusion while its magnitude stays specific to the chosen cases. The later repair of 24 of 33 is a development replay on inspected material and supplies no estimate on data held out from development.

The local executor's 466 of 480 correct constructed scenario slots show arithmetic and relation execution with standardized fields and other requirements satisfied by construction, and they establish no complete applicability. Of 23 local numeric passes on real cases, five have historically supported evidence for the whole description and eighteen stay unknown because other conditions are unresolved. The old automatic guard corrected no binary administrative disagreement error. For the five historically refuted cases it reduced the correct native refutations from three to one by converting two to unknown, because an unparsed numeric rule was allowed to override a negative answer even when the audit could establish a mandatory contradiction. Preserving verified refutations is a logical requirement, while accepting every unverified model negative is not.

Administrative comparisons stay in the supplement rather than entering the main evidence task ranking. A source only majority diagnostic obtains 69.1 percent balanced accuracy and Granite 71.7 percent, and their paired difference of 2.6 percentage points has a wide group resampling interval from minus 18.4 to 19.4. That shows an available source signal without establishing that Granite used the shortcut internally. Granite's full input gains over facts only and rules only are 16.3 and 22.8 points, with intervals of 1.4 to 31.6 and 10.2 to 37.2, so both input types matter to that fixed implementation. Aggregate input dependence still does not verify condition reasoning. The historical tasks, reference policies, intervals and interface failures are preserved as conditional diagnostics and are not pooled with the new controlled endpoints.

## 6 Five source to condition chains

### 6.1 Connector absence: a gap created by input selection

[H330938](https://rulings.cbp.gov/ruling/H330938) concerns two cable descriptions. The candidate requires monopolar conductors, voltage above 1,000 V, a material restriction expressed as other than of copper, and absence of connectors. The frozen input contains an aluminum conducting core and an explicit 2,000 V wiring rating, and it omits the decisive connector description. The complete ruling reports that the submitted documentation “describes the subject cables as imported on reels at very long lengths without connectors”, an independently identifiable descriptive assertion in the agency's analysis. Its location outside the retained excerpt explains the earlier unknown connector state, and the gap was introduced by input selection.

Restoring the assertion changes the connector condition from unknown to supported under the direct text policy. It does not settle the whole description. Whether the single pole system establishes the intended monopolar category stays a mapping question. The aluminum core and the copper shield also require a decision about which component the copper restriction governs, since restricting the predicate to the conducting core supports it and extending it to every part that contains copper refutes it. The audit keeps those policies separate instead of attributing both uncertainties to missing measurements. The chain identifies one repairable input omission and two remaining interpretation choices. A request for connector status becomes unnecessary once the public assertion is admitted, and a whole case affirmative answer is still not licensed by that repair alone.

### 6.2 Dimensions and lifting capacity are different predicates

[H318593](https://rulings.cbp.gov/ruling/H318593) describes a three ton floor jack. Against the first candidate description its stated dimensions of 61 by 30.2 by 15.2 cm lie comfortably below ceilings of 81 by 41 by 25 cm, and its mass of 26.4 kg is below 52 kg. The dimensional statement expressly excludes the handle, so establishing the dimensions of the complete jack requires matching the measurement scope before comparing values. The audit keeps the mass comparison as supported and the complete dimension condition as unknown. A stated composition of 68.50 percent steel with aluminum components adds a separate category question about what counts as of steel, and review needs complete dimensions together with an explicit mixed metal interpretation.

A second candidate in the same ruling limits lifting capacity to 550 kg. The stated capacity of 6,000 lb converts to 2,721.55422 kg and directly refutes that necessary condition. The value concerns the supported load rather than the jack's own mass, and it stays decisive even if another attribute is unreported. The pair therefore requires two distinct audit actions: seek or define the correct measurement scope for the first candidate, and preserve an established contradiction for the second. A guard that converts every unparsed numeric description into overall unknown can erase the latter finding, and the fault lies in the relation and the fusion policy rather than in conjunction.

### 6.3 Relay ratings require product and role binding

[N311039](https://rulings.cbp.gov/ruling/N311039) describes four power relays. The candidate voltage condition is greater than 60 V and no more than 250 V, and the contacts must also be rated at least 10 A. The four products have coil and contact voltage pairs of 12 and 277, 110 and 277, 48 and 277, and 48 and 277 V, with contact current ratings of 30, 40, 40 and 40 A. Each number keeps its product and its rating role. A pooled interval spanning all reported voltages would insert values the source never reports and discard which rating belongs to which relay.

The second product is role dependent, since its 110 V coil lies inside the range while its 277 V contacts do not. Products one, three and four fail the voltage limit under either listed rating role, because their coil voltages are too low and their contact voltages are too high. Under the declared all listed products task the voltage condition is refuted even without choosing a role for the second product, and the current threshold is independently supported. This corrects an earlier AI coding that treated the electrical information as unresolved. A determinate conclusion about the quantified set survives the remaining ambiguity because other members fail every represented alternative.

### 6.4 Glove composition: the value is present and its authority is contested

[H333371](https://rulings.cbp.gov/ruling/H333371) concerns polyurethane coated gloves. The material condition requires less than 50 percent by weight of textile fibers. The public record contains a party supplied composition of 48 percent polyester and a reported laboratory result of approximately 76 percent textile. The product description, the plastic coating and the enhanced grip purpose have direct support. The unresolved condition is the textile fraction and which assertion is admitted as controlling, so this is not an absent number problem.

Under laboratory priority the textile condition is refuted, under party priority it is supported, and a strict record that declines to resolve the conflicting assertions leaves it unknown. These are explicit alternative policies rather than equally authoritative recommendations. Laboratory evidence may carry compelling institutional priority, and that priority is an argument to state and evaluate instead of an invisible preprocessing decision. Appending another copy of either number cannot reconcile the conflict. A prospective interface would need to expose the competing reports with their attribution and a rule for resolving them, and the short condition output schema used in the controlled demonstration cannot express that conflict.

### 6.5 A passive infrared subsystem inside a multisensor apparatus

[H333673](https://rulings.cbp.gov/ruling/H333673) concerns a rain, light, solar and humidity sensor assembly. The public source distinguishes several sensing functions and describes the front light sensor as using passive infrared detection for light switching, while other sensors in the assembly operate on different principles. The candidate describes apparatus using passive infrared detection sensors and designed to turn lights on and off. The light control function has direct textual support. The infrared condition raises a scope question about whether use by the relevant light control subsystem suffices or a broader apparatus category must be established.

Neither the presence of other sensor types nor the word apparatus establishes a universal requirement that every component use passive infrared, and one passive infrared component does not settle the complete legal category. The disputed scope is preserved and the case stays outside a flat necessary conjunction conclusion. That treatment shows why the 15 logic unresolved pairs are not simply difficult unknown examples for the same aggregator, since their representation needs further work. The appropriate next action concerns a category or quantifier interpretation rather than a generic request for an infrared number.

## 7 Discussion

### 7.1 One label, three operations

The audit identifies three operations with different implications. Restoring a descriptive assertion repairs an omission in input construction. Declaring a material, category or measurement mapping resolves a policy choice conditionally. Correcting a product or component binding changes which relation is being tested. A single insufficient evidence class obscures both the origin of the uncertainty and the action that could address it, and the counts in Section 5.2 show that the three operations differ in reach by more than a factor of ten.

The distinction also changes how an apparent model error reads. A model that agrees with a complete administrative ruling can be unsupported by the shortened input it received. A model that requests a fact omitted by the benchmark can be responding correctly to that input while appearing unhelpful in an audit of the public source. An evaluation therefore has to name its reference object before scoring: agreement with an administrative disposition, support in an admitted text, or validity under an authoritative interpretation. Those are related endpoints and they are not interchangeable.

The records make the admitted text endpoint reproducible and expose the choices that legal interpretation involves. A reader can localize a disagreement to a quotation, a target object, a rating role, an admission policy or a logical scope, then recompute its consequence. The resource supports a substantive challenge to a label, including challenges that agreement between annotators would conceal.

### 7.2 What a legal AI evaluation should report

Four disclosures follow from the audit, and each is cheap relative to the cost of an uninterpretable score.

The first is the source version and the admission policy. A result should state which official text version was used, which statements were admitted as evidence and which were withheld, because the same ruling supports different reference states under different selections.

The second is the interpretation mapping. The 10, 17 and 19 supported cases in Table 3 come from one collection under three declared packages, so a single reported count without its mapping is not reproducible and cannot be compared across systems.

The third is the separation of state, citation and request. A whole case score can be high while condition states are wrong and necessary requests are missing, as the checklist results show, and each of those failures has a different remedy in review.

The fourth is the denominator structure. The 96 linked relations share endpoints, the 216 condition records contain 35 unknown states with an empty citation set, and the 58 conjunctive cases exclude 15 logic unresolved pairs. A count reported without that structure invites a comparison that the design does not support.

None of these disclosures requires new models or larger data. They require that the construction of the input be recorded as part of the evaluation, which is what the protocol supplies.

### 7.3 From interface diagnosis to legal reasoning evaluation

The functional results are interface level diagnostics, and naming that boundary makes the remaining work specific rather than open ended. Four capabilities are currently supplied by the construction and would have to be recovered for an evaluation of legal reasoning.

Rule extraction is supplied. The two conditions arrive as structured requirements, while a complete exclusion must be recovered from published text that contains code gates, incorporated standards, alternatives and exceptions. The inventory in Section 5.3 shows the shape of that material.

Fact finding is supplied. Facts arrive numbered and selected, while a real dossier requires deciding which product attributes are relevant and where they are documented. The audit's absent attribute category marks the cases in which the public record itself is silent.

Conflict representation is missing. The short interface requires empty evidence for unknown, which cannot express two competing reports about the same predicate, as the glove composition case shows. A richer output contract would represent competing claims, their sources and a priority rule.

Temporal and version tracking is missing. Exclusions and tariff codes change, and a condition can be valid in one period and not in another. The inventory's date dependent transitions make that requirement concrete.

An evaluation that addressed these four items could support claims about legal applicability reasoning. The present diagnostics support claims about whether the audit categories are observable and whether an interface can report them, which is the prior question.

### 7.4 Boundaries

The main validity limit is independent domain validation. Public source quotations are inspectable and machine checked, while the semantic assignments and interpretation packages remain judgments produced with AI assistance. The frame species erratum shows that deleting one explicit statement need not remove semantic support for its condition, since the remaining teak frame statement still establishes that the frame is wooden.

The materials are also retrospective, selectively published and purposively retrieved, and they cannot establish the distribution of incomplete importer dossiers. Shared rulings and rule groups limit independent information, and the twelve constructed families share a design template. One model in one configuration supplies the functional results, so the comparison describes two output contracts rather than a causal effect of any single prompt ingredient.

No participant, importer workflow or field intervention is observed, and no professional time or monetary consequence is estimated. Those constraints limit claims about legal accuracy, population rates and operational benefit, and they leave the narrower findings about the retained sources and the frozen interfaces intact.

## 8 Conclusion

An evidence benchmark built from a public legal decision should preserve the path from the complete source to the admitted input and to the condition that input is meant to establish. In this tariff exclusion audit, some apparent gaps come from clipped descriptive statements, others from attributes absent in the public record, and others from interpretation or binding. Those distinctions produce different reference states and different next actions. Source restoration repairs particular relations while category and scope choices stay visible.

The records, alternative input versions, interpretation packages and controlled diagnostics support inspection and recalculation of those choices, and the resulting resource makes an evidence label an object that can be contested at a named location. The next steps are expert adjudication of the interpretive layer, richer conflict representation, automatic rule construction and prospective dossiers built against this explicit baseline. An administrative disposition or agreement among AI coders cannot serve as the endpoint of that validation.

## Declarations

Funding: This research received no specific grant from any funding agency in the public, commercial or nonprofit sectors.

Competing interests: The author declares no competing interests.

Ethics approval and consent to participate: Not applicable. The study analyses public administrative rulings and involves no human participants, human tissue or animal subjects.

Consent for publication: Not applicable.

Data availability: The retained derived records, source locators, constructed inputs, reference erratum, prompts, raw model outputs and analysis code are archived at Zenodo: https://doi.org/10.5281/zenodo.23641463. Official public source snapshots are included in that archive and identified in its manifest. Model weights are not redistributed, and their official provenance and hashes are recorded.

Materials availability: Not applicable beyond the public documents identified in the package manifest.

Code availability: Audit scripts, aggregation code, figure scripts and analysis code are included in the same Zenodo archive. The verification command recomputes the reported counts from the retained records and saved model replies.

Author contributions: Junjie Zhang designed the study, curated the sources, performed the audit, ran the experiments, analysed the results and wrote the manuscript.

Use of artificial intelligence: OpenAI Codex (GPT-6 family, October 2026) was used for Python code assistance, English language polishing and assisted semantic coding of the condition records. Coding is described in Section 3.4, retrieval support in Section 3.1 and the control conditions in Section 4.2. All counts reported in Sections 5.1 to 5.5 were independently recomputed from retained artifacts, and every quotation was checked against the public ruling text. The author takes full responsibility for the manuscript. Qwen3-14B generated the diagnostic responses in Sections 5.4 and 5.5. All sources are public federal documents, and no personal, proprietary or human subject data were processed.

## References

1. U.S. Trade Representative. Notice of product exclusions: China's acts, policies, and practices related to technology transfer, intellectual property, and innovation. Office of the U.S. Trade Representative (2018). https://ustr.gov/sites/default/files/enforcement/301Investigations/12.21.18_Notice_of_Product_Exclusions.pdf

2. U.S. Government Accountability Office. U.S.-China trade: USTR should fully document internal procedures for making tariff exclusion and extension decisions. GAO-21-506 (2021). https://www.gao.gov/products/gao-21-506

3. Koreeda, Y., Manning, C.D. ContractNLI: a dataset for document-level natural language inference for contracts. In: Findings of the Association for Computational Linguistics: EMNLP 2021, pp. 1907–1919. Association for Computational Linguistics (2021). https://doi.org/10.18653/v1/2021.findings-emnlp.164

4. Holzenberger, N., Van Durme, B. Connecting symbolic statutory reasoning with legal information extraction. In: Proceedings of the Natural Legal Language Processing Workshop 2023, pp. 113–131. Association for Computational Linguistics (2023). https://doi.org/10.18653/v1/2023.nllp-1.12

5. Medvedeva, M., McBride, P. Legal judgment prediction: if you are going to do it, do it right. In: Proceedings of the Natural Legal Language Processing Workshop 2023, pp. 73–84. Association for Computational Linguistics (2023). https://doi.org/10.18653/v1/2023.nllp-1.9

6. Gogani-Khiabani, S., Trivedi, A., Chyi, S.P., Tizpaz-Niari, S. Performance of LLMs on VITA test: potential for AI-assisted tax returns for low income taxpayers. Artificial Intelligence and Law (2025). https://doi.org/10.1007/s10506-025-09465-7

7. Roy Choudhury, M., Chandramouli, A., Anand, M., Gupta, V. Better Call CLAUSE: a discrepancy benchmark for auditing LLMs legal reasoning capabilities. In: Findings of the Association for Computational Linguistics: EACL 2026, pp. 5776–5818. Association for Computational Linguistics (2026). https://doi.org/10.18653/v1/2026.findings-eacl.305

8. Ribeiro, M.T., Wu, T., Guestrin, C., Singh, S. Beyond accuracy: behavioral testing of NLP models with CheckList. In: Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics, pp. 4902–4912. Association for Computational Linguistics (2020). https://doi.org/10.18653/v1/2020.acl-main.442

9. Lee, E., Kim, S., Kim, S., Jung, S., Kim, H., Cha, M. Explainable product classification for customs. ACM Transactions on Intelligent Systems and Technology 15(2), Article 25, 1–24 (2024). https://doi.org/10.1145/3635158

10. Lan, T., Yang, Y., Jia, Q., Zhu, L., Jiang, H., Zhu, H., Luo, W., Wang, L. HSCodeComp: a realistic and expert-level agent benchmark for hierarchical rule application. In: Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics, Volume 1: Long Papers, pp. 20458–20489. Association for Computational Linguistics (2026). https://doi.org/10.18653/v1/2026.acl-long.937

11. Xia, Q., Zhang, Z., Wang, A., Wang, W., Wang, X., Li, J. HSGraphAgent: knowledge-graph-guided large language models for Harmonized System code classification. In: Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics, Volume 1: Long Papers, pp. 44761–44773. Association for Computational Linguistics (2026). https://doi.org/10.18653/v1/2026.acl-long.2072

12. Lee, H., Choi, G., Lee, E.-J., Lee, S.-M., Ko, Y., Lim, D., Jang, S.-K., Jo, Y. TriBench-Ko: evaluating LLM risks in judicial workflows. arXiv 2605.03792 (2026) [preprint]. https://doi.org/10.48550/arXiv.2605.03792

13. U.S. Customs and Border Protection. Customs Rulings Online Search System (CROSS), public database (n.d.). https://rulings.cbp.gov/

14. U.S. Trade Representative. Index of exclusions for possible extension, 17 January 2024 version (2024). https://ustr.gov/sites/default/files/Updated%20Index%20of%20Exclusions%20for%20Extension%201.17.24.pdf

15. Qwen Team. Qwen3-14B, model card and weights (2025). https://huggingface.co/Qwen/Qwen3-14B

16. ggml-org. llama.cpp, build b11516 (2026). https://github.com/ggml-org/llama.cpp/releases/tag/b11516
