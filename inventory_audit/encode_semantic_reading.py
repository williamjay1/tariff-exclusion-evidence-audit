"""AI source-reading register. Codes below were assigned after reading each scope.
This is not an automatic classifier or an executable legal ontology.
Columns: row | target | logic | stated magnitude types | external identifier types.
Empty magnitude field means no explicit magnitude judged in the scope, not no legal condition.
"""
from pathlib import Path
import json,hashlib
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
rules=[json.loads(x) for x in (ROOT/'datasets/statutory_rules.jsonl').read_text(encoding='utf-8').splitlines()]
REGISTER='''
0|C|ID||HTS
1|P|AND||HTS
2|P|ALT||
3|P|ATOM||
4|P|AND|value|
5|A|AND,EXCL|value|
6|A|AND|power,cooling_capacity|
7|S|AND||
8|P|ALT||
9|A|AND|value|
10|A|AND,ALT||
11|C|ID||HTS
12|A|AND||
13|P|AND,ALT,UNRESOLVED|length|
14|P|AND,ALT|length|
15|A|AND,ALT||
16|A|AND||
17|A|AND,ALT||
18|P|AND||
19|A|AND|mass|
20|P|AND,ALT||
21|P|AND||
22|C|ID||HTS
23|A|AND||
24|A|ATOM||
25|A|AND||
26|P|AND,ALT||
27|M|AND,ALT||
28|P|AND||
29|P|AND||
30|A|ATOM||
31|P|AND||
32|A|AND,EXCL||
33|C|ID||HTS
34|P|AND,ALT||
35|P|AND,ALT||
36|P|AND,ALT||
37|S|AND|dimensions,mass|
38|P|AND||
39|P|AND||
40|P|AND||
41|P|AND|count,dimensions,mass|
42|P|AND||
43|P|AND||
44|C|ID||HTS
45|P|AND||
46|P|ALT,OPEN_LIST||
47|A|AND|power|
48|A|AND,EXCL|power,diameter|
49|A|AND|power,value|
50|A|AND|phase_count,pole_count,power,value|
51|A|AND||
52|A|AND|power|
53|A|AND|power|
54|A|AND||
55|C|ID||HTS
56|A|AND|dimensions|
57|S|AND|layer_count,value|
58|P|AND||
59|P|AND|value|
60|A|AND|current,dimensions,terminal_count|
61|A|AND|pole_count,throw_count,current,dimensions|
62|A|AND|voltage|
63|A|AND,ALT||
64|P|AND|voltage,value|
65|P|AND|voltage,value|
66|A|AND|pressure,value|
67|P|AND|voltage|
68|P|AND|voltage,value|
69|P|AND,ALT||
70|A|AND,EXCL|value|
71|P|AND,ALT||
72|A|AND|value|
73|S|AND|range,value|
74|P|AND,UNRESOLVED||unspecified_dimensional_standard
75|P|AND||
76|A|AND||
77|A|AND,EXCL|power|
78|S|AND||
79|S|AND|panel_pair_count|
80|A|ATOM||
81|M|AND,ALT||
82|P|AND||
83|S|AND||
84|P|AND,ALT||
85|S|AND,COND|dimensions|
86|A|AND,ALT,EXCL||
87|A|AND,EXCL|voltage_discrete_exclusions|
88|A|ATOM,OPT||
89|A|AND||chemical_name
90|A|AND,ALT|displacement|
91|A|AND,ALT,OPT|mass|
92|A|AND|mass|
93|A|AND,ALT|power|
94|A|AND|power|
95|A|AND|voltage,power,dimensions|
96|A|AND|voltage,power,dimensions|
97|A|AND|voltage,power,dimensions|
98|A|AND|power|
99|A|AND|power,dimensions|
100|A|AND|dimensions|
101|A|AND|power,value|
102|A|ALT||
103|A|AND||
104|A|AND,ALT|value|
105|A|AND|value|
106|A|AND||
107|A|ATOM||
108|A|AND,EXCL|dimensions|
109|A|AND,EXCL|voltage|
110|P|AND||HTS
111|A|AND|width,value_per_area|
112|A|AND,OPEN_LIST|displacement,value|
113|A|AND|power|
114|A|ATOM||
115|A|AND|value|
116|A|AND||
117|A|AND||
118|A|AND,ALT,OPT|width,length|
119|A|AND|width,length|
120|A|AND,ALT,OPT|thickness|
121|A|AND,ALT||
122|A|AND,ALT|width,length|
123|C|ID||HTS
124|C|ID||HTS
125|A|AND|dimensions|
126|A|AND|dimensions,power,mass|
127|A|AND||
128|A|AND|dimensions,mass,door_count|
129|A|AND|weighing_capacity,dimensions|
130|A|AND,ALT|lift_arm_count,mass,load_capacity|
131|A|AND,EXCL|mass|
132|P|AND|value|
133|S|AND||
134|S|AND||
135|C|ID,COND,ALT||HTS,legal_date
136|S|AND||
137|P|AND,OPT,EXCL||HTS
138|S|AND|width,length|
139|S|AND||
140|A|AND,EXCL|power,dimensions,mass|
141|S|AND|power,dimensions|
142|A|AND|power,dimensions|
143|A|AND|power,voltage,mass,dimensions|
144|A|AND,EXCL,OPT|power,voltage,mass,dimensions|
145|A|AND,ALT|voltage,frequency,dimensions,mass|
146|C|ID||HTS
147|A|AND,ALT|value|
148|P|AND,ALT||
149|A|AND,OPT|power,volume_capacity|
150|A|AND|power,volume_capacity|
151|A|AND,ALT||
152|P|AND||
153|A|AND||
154|A|AND,OPT|power,mass|
155|M|AND,ALT,UNRESOLVED|BTU_rating|
156|A|AND|mass|
157|C|ID||HTS
158|A|AND||
159|P|AND||
160|S|AND,ALT|channel_count,camera_count|
161|A|AND|mass,dimensions,cable_length|
162|A|AND|resolution,mass,dimensions|
163|A|AND|resolution,mass,dimensions|
164|P|AND,EXCL|layer_count|
165|P|AND,EXCL|layer_count,dimensions|NEMA
166|P|AND,EXCL|layer_count|
167|A|AND,ALT|dimensions,mass,value|
168|C|ID||HTS
169|A|AND,ALT|channel_count,dimensions|
170|A|AND|voltage,value|
171|A|AND|voltage,length|NEMA
172|A|AND,ALT|voltage,length|NEMA
173|S|AND,EXCL,ALT|voltage,bundle_count|
174|S|AND|diode_count,cable_count,voltage|
175|P|AND||
176|P|AND,ALT||
177|P|AND,ALT||HTS
178|P|AND||SAE
179|C|ID||HTS
180|P|AND||SAE
181|P|AND||SAE
182|P|AND||material_grade
183|P|AND||SAE
184|P|AND,EXCL|host_bumper_dimensions|
185|A|AND,EXCL,ALT|wheel_diameter,tire_cross_section,speed_count|
186|A|AND,EXCL|wheel_diameter,mass_without_accessories,tire_cross_section|
187|A|AND,EXCL|wheel_diameter,speed_count|
188|P|AND|value|
189|A|AND,COND|mass,load_capacity|ASTM
190|C|ID||HTS
191|P|AND,COND|diameter_including_tires|
192|A|AND,EXCL|magnification,mass|
193|A|AND,EXCL|magnification,mass|
194|P|AND|mass|
195|S|AND|wind_cup_count,solar_panel_count|
196|S|AND,UNRESOLVED|wind_cup_count,mass|
197|P|AND,ALT||HTS
198|A|AND|mass|
199|A|AND|duration|
200|A|AND,EXCL|dimensions|
201|C|ID||HTS
202|A|AND||
203|A|AND,EXCL,ALT,UNRESOLVED|width|
204|A|AND,ALT,OPEN_LIST|minimum_user_capacity|
205|A|AND,EXCL,ALT,UNRESOLVED|width|
206|P|AND,OPEN_LIST||
207|P|AND|dimensions|
208|P|AND||
209|S|AND||
210|A|AND,EXCL||
211|S|AND,EXCL,ALT,UNRESOLVED|assembled_dimensions|
212|C|ID||HTS
213|A|AND,OPT|dimensions,lip_height|
214|A|AND,ALT|dimensions|
215|A|AND,EXCL||
216|S|AND,EXCL|piece_count,member_dimensions|
217|A|AND|diameter|
218|A|AND|reel_dimensions|
219|A|AND,ALT||
220|P|AND||
221|C|ID||HTS
222|C|ID||HTS
223|A|AND,ALT|case_net_mass|
224|A|AND|block_mass|
225|A|AND|container_net_mass|
226|A|AND|container_net_mass|
227|A|AND,EXCL|container_net_mass|
228|A|ATOM||CAS,IUPAC
229|A|ATOM||CAS
230|A|ATOM||CAS,IUPAC
231|A|AND||
232|A|AND,ALT||
233|C|ID||HTS
234|A|AND||
235|A|AND,UNRESOLVED|concentration|CAS
236|A|AND,ALT||
237|A|AND||
238|A|AND||
239|A|AND||
240|A|AND,ALT||
241|A|AND,ALT||
242|A|AND||
243|A|AND||
244|C|ID||HTS
245|A|AND||
246|A|AND||CAS
247|A|AND|mass_fractions|CAS
248|A|AND|mass_fractions|refrigerant_identifier
249|P|AND,ALT|mass|
250|P|AND,ALT|overall_length,mass|
251|P|AND,ALT|circumference,width,mass|
252|A|AND|dimensions,mass|
253|A|AND|dimensions,mass|
254|A|AND|dimensions|
255|C|ID||HTS
256|A|AND|mass|
257|A|AND|mass|
258|P|AND||
259|A|AND,ALT|mass|
260|A|AND,ALT|mass|
261|A|AND,ALT,EXCL|mass_fraction,width|
262|A|AND,ALT,EXCL|mass_fraction,width|
263|A|AND,ALT,EXCL||
264|A|AND|mass_fraction,width,areal_mass|
265|A|AND|mass_fraction,width,areal_mass|
266|C|ID||HTS
267|A|AND|mass_fraction,width,areal_mass|
268|A|AND|areal_mass,width|
269|A|AND,EXCL|areal_mass,width|
270|A|AND|areal_mass,width|
271|A|AND|mass_fractions,areal_mass,width|
272|A|AND|linear_density|
273|A|AND|linear_density|
274|A|AND|areal_mass,width|
275|A|AND|dimensions,areal_mass|
276|A|AND|area|
277|C|ID||HTS
278|A|AND|mass_fractions,areal_mass,width|
279|A|AND|value_per_area|
280|A|AND,ALT||
281|A|AND|side_count,edge_count,density|
282|A|AND|side_count,dimensions|
283|A|AND||
284|A|AND|side_count,mass,dimensions|
285|A|AND|area|
286|P|AND|dimensions,mass|
287|P|AND|dimensions,mass|
288|C|ID||HTS
289|A|AND,ALT|grid_dimensions|
290|S|AND,ALT,UNRESOLVED|assembled_dimensions,mass,load_capacity|
291|S|AND,ALT|minimum_component_inventory|
292|P|AND|dimensions,mass|
293|A|AND|mass,dimensions|
294|A|ATOM||CAS
295|S|AND||
296|A|AND,ALT,EXCL,OPEN_LIST||
297|S|AND,UNRESOLVED|shaft_measurement|
298|P|AND,ALT||
299|C|ID,COND,ALT||HTS,legal_date
300|P|AND||
301|P|AND||
302|A|AND|mass,dimensions|
303|P|AND,EXCL,ALT,UNRESOLVED||HTS
304|P|AND,EXCL,ALT|dimensions,mass|HTS
305|P|AND,EXCL,ALT|dimensions,mass|HTS
306|P|AND||
307|P|AND,ALT||HTS
308|A|AND|dimensions,volume|
309|A|AND,ALT|mass,pressure|
310|C|ID||HTS
311|M|AND,ALT||
312|A|AND||
313|A|AND||
314|S|AND|pad_count|
315|A|AND,ALT||
316|A|AND,ALT||
317|A|AND,EXCL,ALT,OPT||HTS
318|A|AND||
319|A|AND||
320|A|AND,EXCL||
321|C|ID||HTS
322|A|AND||
323|A|AND||
324|A|AND,EXCL||
325|A|AND,ALT,EXCL||
326|A|AND,EXCL||
327|A|AND,EXCL||
328|A|AND,EXCL|edge_length|
329|A|AND,EXCL|edge_length|
330|P|AND,ALT||
331|A|AND||
332|C|ID||HTS
333|P|AND,EXCL||
334|A|AND||
335|P|AND||
336|A|AND,ALT||
337|A|AND|mass|
338|A|AND,COND|side_length,diameter,thickness,mass|
339|A|AND||
340|P|AND,EXCL|display_diagonal|
341|S|AND||
342|A|UNRESOLVED||undefined_product_term
343|C|ID||HTS
344|A|AND,EXCL,ALT|magnification,aperture|
345|P|AND||
346|A|AND,ALT||
347|C|ID||HTS
348|C|ID||HTS
349|C|ID||HTS
350|C|ID||HTS
351|A|ATOM||CAS
352|P|AND,OPEN_LIST||
353|S|AND||DIN
354|A|AND||
355|M|AND,ALT||
356|A|AND,OPT|dimensions|
357|C|ID||HTS
358|C|ID||HTS
359|C|ID||HTS
360|C|ID||HTS
361|C|ID||HTS
362|C|ID||HTS
363|P|AND,ALT||
364|P|AND||
365|A|AND||FDA_class_and_product_code
366|A|AND,ALT||
367|C|ID||HTS
368|A|AND,OPT||
369|A|AND||CAS
370|C|ID||HTS
371|A|AND,ALT||
372|A|AND,ALT|width,length|
373|A|AND||CAS
374|A|AND,EXCL,ALT||HTS
375|A|AND,EXCL,ALT,UNRESOLVED||
376|S|AND,ALT||
377|P|AND||
378|P|AND,ALT||
379|A|AND||
380|A|AND||
381|A|AND||
382|S|AND||
383|A|ATOM||
384|A|ATOM||
385|S|AND||
386|P|AND,ALT||
387|A|AND,ALT||
388|S|AND||
389|A|AND||
390|P|AND||
391|A|AND,ALT||
392|P|AND,ALT||
393|C|ID||HTS
394|C|ID||HTS
395|A|AND|length,inner_diameter,outer_diameter,flange_diameter|
396|A|AND|width,length,areal_mass|
'''
NOTES={
 6:'Input/motor power and cooling capacity are distinct attributes even though both use W/kW.',
 7:'Glass tubes and stands with tanks form named component requirements; do not treat the list as alternative products.',
 13:'Width or length applies to processed sheets, not die dimensions; OR wording retained; no automatic both-dimensions interpretation.',
 14:'51 cm qualifies the host calendering machine width, not every cutting pad.',
 20:'Product alternatives housings/covers/couplings; steel and host liquid-filter function apply to every selected alternative.',
 27:'Mixed apparatus and parts language; do not require a part to be a complete forklift.',
 29:'Steel condition attaches to cords and cleats; rubber applies to track.',
 50:'Three phase and eight pole are count-type configuration attributes, not decimal magnitudes inferred from identifiers.',
 60:'Current is switch rating; terminal count belongs to each switch; D-shaped is categorical, not numeric diameter.',
 66:'Read direct acting and spring return as source-listed actuator types; whether jointly required for a single product is not resolved here.',
 73:'Value is per set; transmission range refers to communication system, not dimensions.',
 74:'Set dimensional and surface finish requirements are asserted but their values are absent; external specification unresolved.',
 79:'Three pairs of panels describes gantry cover components; not six independent products.',
 85:'Dimensions apply when assembled; required set components are plate, tray and lid.',
 87:'Excluded set {6,12,24} V, not a continuous interval from6 to24 V.',
 88:'Accessories/batteries explicitly optional; no negative requirement follows from not in whether or not.',
 91:'Manual/proximity battery pump alternatives are accepted configurations, not simultaneous requirements.',
 95:'Motor outer diameter, housing length and shaft length are separate measured objects.',
 97:'Shaft length differs from motor overall length.',
 109:'Copper exclusion may depend on conductor ontology (core versus neutral conductor); no universal material inference from cable composition. Connector absence is a separate condition.',
 118:'Adhesive is on one side; clear/transparent-color alternatives; printing is optional.',
 120:'Total film thickness includes layers; primer optional and coating material alternatives are not contradictions.',
 129:'16 kg is weighing capacity, not scale mass; handles mentioned without an explicit exclusion from dimensions in this index entry.',
 130:'Article mass and load limit are separate; two lift arms is component cardinality.',
 135:'Date selects historical statistical code branch; not a physical dimension or standalone validity determination.',
 137:'Fan hubs/LEDs are permitted optional content; other goods of referenced headings are excluded. Needs heading definitions to apply.',
 138:'Widths/length belong to textile straps; overall assembly contains hooks and adjustment mechanism.',
 141:'Dimensions explicitly apply to assembly including listed components, not unassembled motor alone.',
 142:'Shaft length bound cannot be substituted for motor height.',
 145:'Input120V/60Hz and output63V OR87V are distinct electrical positions; do not build one voltage interval.',
 149:'50 W belongs to self-contained motor;1 L belongs to receptacle; accessories optional.',
 150:'1500 W motor power and1 L receptacle capacity; model suffix resembling W is not evidence.',
 155:'Source says5000 BTUs, not BTU/hour. Do not silently convert this rating to power without specification.',
 160:'One DVR, channel count4/8/16, camera count2–16 and packaged components use different objects/cardinalities.',
 161:'Camera dimensions and presented cable length are different targets.',
 165:'FR-4 is a standard/grade identifier;10 is layer count; neither can be conflated.',
 171:'5-15P and5-15R are complementary endpoint types, not numeric thresholds.',
 172:'The two NEMA endpoint pairs are alternatives; mixing endpoints from different pairs is not licensed by OR.',
 173:'Bundle count3/5/6 and connectors at each end require distinct bundle/member/end bindings.',
 174:'Three diodes and two cables belong to assembly; voltage bound applies to assessed assembly context.',
 184:'102 mm applies to target vehicle bumper side, not receiver width.',
 185:'Both wheels must meet diameter; material alternatives apply to wheels, not frame/belt. Speed list is discrete.',
 186:'Mass explicitly excludes accessories; both-wheel quantifier and tire-use prohibition are separate.',
 187:'Both-wheel diameter; no more than3 speeds is separate count.',
 189:'ASTM F1975 condition is guarded by child-carrying designation; not unconditional for every trailer.',
 191:'Diameter includes tires where appropriate; the measurement boundary is conditional.',
 194:'Mass plausibly attaches to wind-vane unit; source span retained for interpretation.',
 195:'Exactly3 cups, bearings and fan, at least1 solar panel; minimum panel count cannot be applied to wind cups.',
 196:'35 g attachment is ambiguous between cups and whole assembly; mark binding unresolved, do not force one gold target.',
 203:'Width may attach to seats/backs shells rather than chair overall; binding unresolved from sentence alone.',
 205:'Same width attachment ambiguity as row203; non-upholstery is distinct from other household exclusion.',
 211:'Source transcription says183 m (not cm) for width upper bound; suspected source-unit anomaly requires original-source check; retain literal.',
 213:'Dimensions apply to rack; lip height applies to each slanted shelf. Casters and LED lighting optional.',
 216:'Two pieces have different dimension bounds; one/other binding must be retained.',
 218:'25 cm diameter and1.5 cm width refer to reel, not strip.',
 223:'More than4.5 kg is net case weight, not fish or block mass.',
 224:'Mass per block differs from container net-weight conditions in neighboring entries.',
 235:'Concentration basis not explicit as by-weight/by-volume in this scope; CAS digits are identity, not quantity.',
 247:'Three mass-fraction constraints are joint composition conditions, not independent arbitrary values that can exceed total100%.',
 248:'Composition ranges jointly constrained; identifier R-421B is not a magnitude.',
 250:'Overall stopper length is specified; do not measure only plug/stirrer.',
 261:'Silk/noil exclusion and by-weight fraction require material identity; not printed/not jacquard are categorical exclusions.',
 262:'Same as row261 with different width interval; no automatic merge.',
 268:'Wholly indicates composition completeness, not an explicit numeric percentage in source.',
 272:'ktex is linear density, not width or mass alone.',
 273:'ktex is linear density, not width or mass alone.',
 275:'g/m² is areal mass; do not compare to whole-sheet mass.',
 281:'One textured side, up-to-four chiseled edges and bulk density are distinct properties.',
 290:'Dimensions attach to assembled configurations; whether91kg is per assembly/component requires clarification. Load capacity separate.',
 291:'At least signals minimum named component inventory without numeral; steel/cast-iron and gas-source alternatives retained.',
 292:'Metric/imperial equivalents describe same measures, not additional independent constraints.',
 297:'9.5 mm shaft measurement lacks explicit dimension name; plausible diameter but not asserted as gold here.',
 299:'Historical code branch by date; not physical duration.',
 303:'Nested exclusion grammar combines cast-iron/material, processing state, permitted machining and connecting rods; grouping unresolved without authority. Do not flatten all not/or tokens.',
 304:'Host-engine/vehicle exclusions, not lifter material exclusions; cross-referenced headings need definitions.',
 305:'Same host exclusions; dimensions and mass attach to lifter.',
 311:'Scope includes shower heads and their parts; complete-head feature requirements should not automatically be assigned to every part.',
 314:'Three pads=two front/side+one back; member types and count cannot be interchanged.',
 317:'Excluded tariff heading and optional metal-leaf application separate.',
 328:'At least116 and at most118cm on an edge does not explicitly quantify every edge; preserve wording.',
 329:'Same edge quantifier issue; non-woven condition is separate.',
 338:'Side<=86mm if rectangular OR diameter<=28mm if circular, plus common thickness/mass/function requirements; other shapes unresolved.',
 342:'Protective Articles alone is under-specified in scope text. Do not invent a medical or tariff definition from title.',
 353:'DIN42802 is connector standard, not measurement; assembly requires electrode pad+insulated wire+connector.',
 365:'FDA Class1 and product codeNNI require external regulatory definition/status; digit1 is not quantity.',
 372:'Sticker marks center; width/length and material alternatives are independent conditions.',
 375:'Parenthetical other than for fuel or lubricants, not fitted... has scope attachment ambiguity; metered dispensing is not necessarily a metering device. Preserve unresolved reading.',
 395:'Tube inner/outer diameter, tube length, flange diameter, spike-end location and removable end caps are different targets.',
 396:'55–88g/m² is laminate areal mass; SSS layer designation is not an inferred independent measurement.'
}
target={'A':'article_or_material','P':'part_or_accessory','S':'set_or_assembly','M':'mixed_whole_and_parts_or_types','C':'code_only'}
data={}
for line in REGISTER.strip().splitlines():
 p=line.split('|');assert len(p)==5,line
 i=int(p[0]);assert str(i) not in data
 r=rules[i]
 data[str(i)]={'annotation_status':'AI_source_coded_silver','reviewed_fields':['target_level','logical_features','explicit_magnitude_types','external_identifier_types','binding_notes'],'source_scope_sha256':hashlib.sha256(r['scope'].encode()).hexdigest(),'target_level':target[p[1]],'logical_features':p[2].split(','),'explicit_magnitude_types':p[3].split(',') if p[3] else [],'external_identifier_types':p[4].split(',') if p[4] else [],'external_definition_resolved':None,'quantifier_formalization':None,'necessary_condition_count':None,'binding_note':NOTES.get(i,'Apply category/material/function modifiers to the source-described target; no exhaustive legal ontology or atomic count certified.'),'interpretive_resolution':'unresolved' if 'UNRESOLVED' in p[2] else 'source_surface_structure_only','coder':'AI assistant reading original scope; no independent human or legal expert validation'}
assert set(map(int,data))==set(range(397))
(OUT/'semantic_review_codes.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print('Explicit per-row reading codes:',len(data),'binding notes:',len(NOTES))
