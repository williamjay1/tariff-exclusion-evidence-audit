# Source and condition-reference audit

This is an AI-assisted audit of 73 historical case–scope pairs and their 208 existing condition units, linked to 67 official CBP ruling snapshots. It is not human or expert gold. The auditor has previously seen administrative outcomes; this work cannot be called a fresh blind annotation. Administrative outcomes were not used as acceptance criteria, and no requirement to match those outcomes was imposed. The candidate scope is the quotation used in each ruling, not a replacement taken from the 2024 exclusion inventory.

## What was checked

Every historical condition, its complete frozen factual input, its cited evidence and its object/property assignment was read. All 47 historically unknown cases received additional review of relevant facts and analysis throughout the full official public ruling. For the remaining cases the audit checks complete frozen facts and source spans, with targeted context for numeric/refuted cases. A program verifies literal spans and assembles the table; it does not infer the object labels or decide the condition tiers. Direct means an explicit source-text attribute relation with ordinary arithmetic or lexical equivalence. It does not mean that the public statement has been empirically corroborated or legally validated.

The final tiers are **132 direct units (130 scoreable and 2 nonbinding), 45 interpretive, 19 insufficient and 12 disputed**. The strict excerpt states are **125 support, 5 refute, 76 unknown and 2 not applicable**. Adding the admitted independent full-source attributes gives **129 support, 5 refute, 72 unknown and 2 not applicable**. The two nonbinding units are an illustrative “including” list and a “whether or not” permission; they are not mandatory positive conditions.

The 208 units are inherited review units, not a claim that every exclusion has been fully or atomically formalized. Local disjunctions, negative exclusions, component quantifiers and illustrative examples remain marked. **58 cases** permit the restricted outer conjunction over the signed condition units; **15 cases** remain outside that flat interface. This strict diagnostic produces **10 supported, 3 refuted, 45 unknown and 15 logic-unresolved cases** for both excerpt and directly restored views. It must not be substituted for, or merged with, the historical AI-coded 21/5/47 reference. The unchanged case totals coexist with meaningful changes to individual conditions.

## What full-source recovery changes

| Case and condition | Independent source attribute | Boundary |
|---|---|---|
| H330938 c4 | Submitted documentation describes imported cables without connectors. | Repairs the earlier claim that no connector-specific fact appears anywhere in the ruling. It does not settle monopolar or conductor-material scope. |
| H322923 c2 | Wagons are fitted with four wheels. | Class-of-use interpretation remains separate. |
| H340899 c3 | Vacuums have self-contained electric motors. | The historical c3 was already inferred as support; the strict layer had withheld that inference. |
| H340899 c4 | Motor power does not exceed 1500 W. | Backpack versus commercial upright-vacuum category remains unresolved. |

These are four directly restored condition relations in three cases. Only three were historically unknown conditions: H330938 c4, H322923 c2 and H340899 c4. Other recoverable passages are retained separately: H341677 explicitly denies wireless-network transmission but needs a communications definition of “wireless”; H314080 supplies party-attributed width and areal-mass claims; H333673 supplies component-specific functionality. No legal applicability or holding sentence is appended as an observed product property.

## Provenance of the 47 historical unknown cases

These cases contain 137 historical units, of which 59 were historically unknown and 67 are unknown under the stricter relation-only policy. The following sets overlap and their case counts must not be added to 47. A case can contain both an omitted attribute and an unresolved definition.

| Source of unresolved evidence | Cases / 47 | Strict-unknown condition units |
|---|---:|---:|
| excerpt omission | 5 | 7 |
| no sufficient attribute in public source | 10 | 12 |
| definition category or use | 36 | 38 |
| object component or measurement scope | 11 | 12 |
| source or interpretation conflict | 5 | 5 |

The machine-readable summary includes the actual case and condition membership of every set. The “public source absent” designation means no sufficient independent assertion was located in this public ruling, not that the underlying technical document or real-world fact cannot exist. No negative attribute is inferred merely from silence.

## Exact locations and excerpt construction

All 208 rule-unit quotations locate in the raw official text, allowing only recorded whitespace or typographic normalization. Every frozen condition evidence quotation now has one or more verified continuous source spans. N314745_self and N314745_pedal deliberately concatenate nonadjacent product paragraphs: the audit preserves their frozen concatenated span and supplies separate original spans for each selected product. No artificial continuous source span is claimed. N316485 has a truncated individual-import context in the excerpt; the full procedural sentence is retained as context, not as proof that plywood is unfinished.

Raw JSON byte hashes and decoded-text hashes are separately recorded. Offsets address Python Unicode character positions in the unmodified decoded text; hashes identify the byte-level snapshot. Exact quote matching proves location, not legal validity. The full public source itself occasionally has apparent wording inconsistencies (for example the Kent product name in the N308085 reasoning); these are not silently used to supply object-specific facts.

## Five auditable chains

### H330938_1

The omitted connector fact is explicit in the analysis and changes c4 from unknown to support. Monopolar topology and copper-shield scope remain interpretation-dependent. Therefore source restoration alone does not create a strict supported case.

### H318593_1

The stated 61 x 30.2 x 15.2 cm excludes the handle, while the candidate ceiling does not. The full source does not establish the complete dimensions. The separate 550 kg rule in H318593_2 is decisively refuted by the stated 6000 lb load capacity (2721.55422 kg). Neither observation establishes overall legal eligibility.

### N311039_33

The rule is (60,250] V with contacts >=10 A. Bind 12/277, 110/277, 48/277, 48/277 V to four products as coil/contact alternatives, not a pooled interval. Products 1, 3 and 4 fail either rating-role interpretation; product 2 alone is unresolved. Under all-listed-products quantification the voltage condition is refuted. Contact ratings 30/40/40/40 A satisfy their independent threshold.

### H333371_1

The party supplies 48 percent textile, whereas a reported CBP laboratory result is about 76 percent. Both passages are visible. No text-recovery operation resolves the conflict; laboratory priority and party priority deliberately produce different optional states.

### H333673_1

The full source identifies only the front-light sensor as using passive infrared for light switching. The assembly also contains other sensors. Whether using passive infrared applies existentially to a component or universally to an apparatus is not encoded as a mandatory all-components rule. Preserve unresolved logic.

## Reuse and limits

`condition_audit_long.jsonl` contains object scope, property, signed logical role, local formula, numeric/unit scope, both historical states, strict excerpt/full-source states, exact evidence locations and optional interpretation policies. `case_audit.jsonl` exposes the flat-interface boundary. `recovered_attribute_spans.jsonl` is the restoration interface; only entries marked direct_attribute enter `facts_direct_restored`. `case_chains.json` provides all conditions and locators for the five examples.

`evaluate_interpretation_policy.py` applies only explicitly named policies supplied in a JSON configuration. It never selects a policy to agree with the administrative result. Changing interpretation can yield a contrary determinate state; such results are retained. The evaluator refuses to flatten marked unresolved logic and does not read administrative outcome y. These sensitivity states are declared assumptions, not a single replacement silver label.

No new experts, external measurements, or unseen-case validation are claimed. No historical input, reference, prediction or raw snapshot was overwritten. The remaining direct-property resource supports a bounded evidence-interface experiment; it does not evaluate general legal eligibility.
