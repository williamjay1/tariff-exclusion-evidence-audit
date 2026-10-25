## S2 Source audit and annotation lineage

The source audit covers 73 historical product–exclusion pairs, 208 retained condition units and 67 official CBP rulings. Its purpose is to make the relationship between a public source, an admitted factual input and a condition state inspectable. It neither reconstructs the original importer dossier nor supplies independently validated legal answers. The candidate description remains the exclusion quoted in each ruling; it is not replaced by a superficially similar description in the January 2024 USTR index. Historical inputs and coding remain available alongside the audited records.

### S2.1 Records, statement roles and source locations

Every retained condition, its complete frozen factual input, cited evidence and product–attribute assignment was reread. All 47 historically unknown pairs received additional examination of relevant factual and analytical passages throughout their complete public rulings. The remaining pairs received complete excerpt review and source-span checks, with targeted context examination for numerical and refuted conditions. The assembly program checks locations and coverage; the product descriptions, attribute assignments and interpretive distinctions were assigned through AI-assisted reading rather than inferred by that program.

Table S2 lists the principal fields in `source_audit/condition_audit_long.jsonl`. These records preserve the original and later operational coding, rather than overwriting either with the strict audit state. A condition identifier denotes an inherited review unit. It does not certify that the unit is atomic or that the decomposition exhausts the legal description.

Table S2 Principal fields and their evidentiary functions

| Record group | Retained information | Function |
|---|---|---|
| Identity and rule | Case, ruling and condition identifiers; literal candidate quote and location | Links the unit to its actual historical scope |
| Governed relation | Product or component, attribute, quantifier and measurement scope | Distinguishes the target from other products, parts or ratings |
| Logic | Signed requirement, logical role, local alternatives, exception or illustrative status | Prevents negative wording and local alternatives from becoming mandatory positive conjuncts |
| Evidence | Frozen quote, excerpt span, continuous source span or span array, paragraph identifier and attribution | Separates admitted evidence from its public-source location |
| Lineage and state | Original coding, historical operational coding, strict excerpt and restored states | Preserves changes in policy and information availability |
| Interpretation | Reference tier, unresolved cause, reasoning and named optional mappings | Makes assumptions replaceable without replacing the source |

The source-location checks validate 455 continuous span instances and two noncontiguous quotation records: 208 rule locations, 231 continuous source locations corresponding to 228 frozen evidence quotations, and 16 restoration or contextual records. Repeated quotations can contribute more than one checked instance; 455 is not a count of independent observations. The two composite records, N314745_self and N314745_pedal, concatenate selected product paragraphs from the same ruling. Their members have separate continuous locations, rather than an invented continuous source span.

Character offsets refer to the unmodified decoded official text. Recorded whitespace or typographic normalization permits matching a retained quotation while preserving the original characters at its source location. Source attribution distinguishes party descriptions, laboratory findings, agency-stated attributes, definitions, application reasoning and outcomes. A descriptive clause in the analysis can be admitted without admitting the applicability conclusion surrounding it. Conversely, a party's proposed legal characterization does not become an established physical attribute merely because it appears under a factual heading. Successful location checks establish provenance, not legal or empirical validity.

### S2.2 Reference tiers and state lineage

The audit assigns 132 units to the direct tier, 45 to the interpretive tier, 19 to insufficient evidence and 12 to disputed evidence. Of the direct units, 130 are scoreable requirements and two are nonbinding: an illustrative “including” list and a “whether or not” permission. Direct relations allow explicit textual attributes, ordinary lexical equivalence, simple comparisons, unit conversion and discrete membership checks. They do not imply independent measurement of the reported attribute. Interpretive relations require an additional definition, category, functional equivalence or scope mapping. Insufficient records lack an admitted attribute in the relevant input. Disputed records retain conflicting assertions or unresolved interpretation, object or quantifier choices.

Tier and state are distinct. Tier assignment describes the evidentiary relation in the frozen input and remains recorded after restoration. The strict excerpt has 125 supported, five refuted, 76 unknown and two non-applicable units. Admitting the directly recoverable attributes yields 129 supported, five refuted, 72 unknown and two non-applicable units. These states must not be merged with the historical case reference of 21 supported, five refuted and 47 unknown pairs: they use different admission and aggregation policies.

### S2.3 Why historically unknown cases remain unresolved

The 47 historically unknown pairs contain 137 condition units. Fifty-nine conditions were historically unknown; 67 are unknown under the stricter direct-relation policy, which also withholds several previously accepted interpretations. Table S3 describes overlapping cause sets within those 47 pairs. Its condition column counts strict-unknown units belonging to each set. Neither column forms a mutually exclusive partition.

Table S3 Overlapping provenance of uncertainty in the 47 historically unknown pairs

| Cause set | Pairs, denominator 47 | Strict-unknown units, denominator 67 |
|---|---:|---:|
| Relevant assertion omitted from the excerpt | 5 | 7 |
| No sufficient attribute located in the public source | 10 | 12 |
| Definition, category or use interpretation | 36 | 38 |
| Object, component or measurement scope | 11 | 12 |
| Source or interpretation conflict | 5 | 5 |

A pair can contain both an omitted attribute and an unresolved definition. The membership lists in `source_audit/source_audit_summary.json` permit these overlaps to be inspected. “No sufficient attribute located” concerns the public ruling examined, not every document that may exist outside it. Silence is not converted into a negative attribute. Context restoration also need not resolve a property: N316485's complete individual-import sentence clarifies the procedural scope, but supplies no independent assertion that the plywood is unfinished.

### S2.4 Direct restoration and its limits

Four condition relations in three rulings change from strict unknown to support. H330938 c4 receives the statement that submitted documentation describes cables imported without connectors. H322923 c2 receives the explicit four-wheel description. H340899 c3 and c4 receive an assertion of self-contained electric motors with power not exceeding 1,500 W. These relations use three distinct added source sentences. Their original locations and statement attribution are retained in `source_audit/recovered_attribute_spans.jsonl`.

Only three of the four conditions were historically unknown. H340899 c3 had already been inferred as supported in the historical reference; its before-state is unknown under the stricter direct-text policy. Accordingly, the experiment measures changed availability of explicit attribute evidence, not correction of four historical unknown labels. Whole-case uncertainty can persist after restoration. Other passages are retained separately when their use requires additional decisions: H341677's denial of network communication requires a communications reading of “wireless,” while H314080's width and areal-mass intervals repeat the protesting party's proposed exclusion description. The strict policy retains these as attributed claims with an explicit acceptance option. Party attribution and absence of laboratory retesting are not general exclusion criteria.

### S2.5 Aggregation and declared interpretation sensitivity

Fifty-eight pairs permit the restricted outer conjunction over their signed condition units. Fifteen are withheld because alternatives, exceptions, examples or composite-object scope have not been resolved for that interface. Withholding these cases does not imply that their individual conditions are uninformative. The strict excerpt and directly restored versions both produce ten supported, three refuted and 45 unknown aggregate states among the 58 pairs; the other 15 retain an unresolved-logic status.

The sensitivity analysis enumerates only named interpretive or disputed options already recorded in the audit. Direct full-source relations remain fixed, insufficient conditions without admitted resolution remain unknown, and interpretive conditions without an available mapping remain unknown. Each optional mapping may also be withheld. Table S4 gives actual joint results from three fully specified packages, whose case-level choices are recorded in `source_audit/policy_sensitivity.json`.

Table S4 Joint results under explicitly declared interpretation packages, 58 pairs

| Package | Supported | Refuted | Unknown |
|---|---:|---:|---:|
| Withhold optional interpretations | 10 | 3 | 45 |
| Declared technical scope, laboratory priority and peak power | 17 | 8 | 33 |
| Alternative material/use scope, party priority and nominal power | 19 | 5 | 34 |

The second package accepts specified technical and use mappings, conducting-core material scope, laboratory priority for glove composition and peak motor output. The third changes selected material and use mappings, glove-source priority and rating basis. These are diagnostic packages, not authoritative legal doctrines. Across locally enumerated options, the marginal count envelopes are 10–20 supported, 3–9 refuted and 33–45 unknown pairs. They do not constitute one jointly attainable result, probabilities, or the range of all reasonable legal interpretations. Shared legal terms cannot be presumed independently redefinable by case.

### S2.6 Five traceable evidence chains

The complete chains in `source_audit/case_chains.json` include every condition, admitted quote and locator for the following five rulings.

**H330938.** The analytical paragraph beginning “Lastly, the submitted documentation” explicitly supplies connector absence. This corrects the earlier claim that the complete ruling lacked connector-specific evidence. Monopolar topology and the aluminum-core/copper-shield distinction remain separate interpretive switches; resolving c4 does not resolve them.

**H318593.** The product-description paragraph gives dimensions of 61 × 30.2 × 15.2 cm “exclusive of handle.” It cannot establish the unqualified complete-article ceiling in H318593_1. The same paragraph gives a 6,000 lb lifting capacity, approximately 2,721.55 kg, which directly contradicts the separate 550 kg ceiling in H318593_2. Article dimensions, article mass and supported load are distinct attributes.

**N311039.** Separate product paragraphs locate coil/contact voltage alternatives of 12/277, 110/277, 48/277 and 48/277 V. The coil ratings are AC for the first product and DC for the other three; contact ratings are AC. Products one, three and four fail the interval (60, 250] V under either rating-role interpretation. Under the declared all-listed-products quantifier, the condition is refuted without pooling values into an uncertainty interval. Contact ratings of 30, 40, 40 and 40 A independently satisfy the current threshold.

**H333371.** The party-composition and laboratory-report passages respectively give 48% and approximately 76% textile content. Both are visible. Source restoration cannot resolve their conflict; the competing priority policies remain explicit.

**H333673.** Component descriptions and the analytical sentence beginning “Out of the four ancillary sensors” identify passive infrared light-switching functionality in the front-light sensor. They do not settle whether the exclusion requires one qualifying component or a universal apparatus-level property. The audit therefore preserves the unresolved quantifier instead of silently requiring every component to qualify.

### S2.7 Validation boundary

The annotations and this audit are AI assisted, without independent human or domain-expert validation. The auditors had prior exposure to administrative outcomes and earlier project materials; this is not a new blind annotation. Outcomes were not criteria for selecting evidence states or interpretation packages. Shared model lineage permits shared semantic errors despite successful mechanical checks. The contribution of these records is inspectability and recalculation: readers can contest a quoted relation, change a declared mapping or withhold an assertion while preserving its source and annotation history.
