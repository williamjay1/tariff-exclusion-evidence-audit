"""Explicit AI source readings of every product-description row.

PLAN is a manually selected, per-row list of exact start anchors, not a parser.
Each first group begins at 0. Anchors divide the complete wording into coarse
requirements; OR inventories, scoped exceptions and shape guards stay internal.
The 30 previously source-coded readings retain their more explicit group quotes.
Atomic count and independent legal validity are not asserted.
"""
from pathlib import Path
import json,hashlib,collections
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).resolve().parent
rules=[json.loads(x) for x in (ROOT/'datasets/statutory_rules.jsonl').read_text(encoding='utf-8').splitlines()]
# '-' = the scope constitutes one inseparable coarse category/configuration group.
# Blank/code-only rows are excluded explicitly by frozen scope metadata plus two date rows.
PLAN=r'''
1|for water pumps
2|-
3|-
4|of plastics|each valued
5|other than screw type|used in air conditioning|each valued
7|incorporating glass tube
8|-
9|each valued
10|designed for cutting|manually powered
12|with dies for embossing|manually powered
13|of a kind used|such sheets measuring
14|which function as guides
16|powered by batteries
17|submersible|powered by batteries|manually operated|such machinery designed
18|designed to remove
19|electrically powered|weighing
21|-
23|designed for use
24|-
25|diesel powered
26|of iron or steel|designed for use
28|designed to support
30|-
31|-
32|not assembled in cabinets|not presented with
34|of iron or steel|the foregoing parts
35|of cast iron|for oleohydraulic
36|of aluminum|of valves for
37|of iron and steel|each measuring
38|designed for use
39|of steel|designed for use
40|of aluminum|designed for use
41|of aluminum|each with 4 ports|the foregoing measuring|designed for installation
42|of steel|designed for use
43|of steel|designed for use
45|of steel|designed for use
46|-
47|AC|permanent split|not exceeding
48|of an output|other than brushless|measuring
49|of an output|valued over
50|electronically commutated|three-phase|eight-pole|of a kind used|of an output|valued not
51|multi-phase|of rolled steel
52|multi-phase|of an output|having a cast iron
53|each of an output|fitted with pulleys
56|each such controller measuring
57|each valued
58|for industrial furnaces
59|each valued
60|rated at|measuring|each with 2
61|single pole, single throw (SPST)|rated at|each measuring
62|for a voltage|presented in|designed for use
63|designed for use|driver or passenger activated
64|for a voltage|valued over
65|for a voltage|each valued
66|each rated at|valued over
67|for a voltage
68|for a voltage|each valued
69|for use with
70|not provided with|valued not
71|all the foregoing designed
72|each valued
73|each consisting|having a transmission|valued not
74|with set dimensional|used as
75|-
76|with electrical connectors
77|submersible|other than for use|the foregoing pumps rated
78|which utilize
79|each encased
80|-
81|-
82|of radiotherapy systems
83|of a kind designed
84|specially designed
85|of plastics|each consisting|when assembled
88|-
89|presented in dry form
90|each having a displacement
91|whether employing|each article weighing
92|electric powered|individually weighing
93|of 18.65 W|each with attached
94|with an output|with attached cables|designed for use
96|230 V|with an output|measuring
97|24 V|with an output|measuring|with a shaft
98|with an output|containing lead
99|with a power output|measuring
100|of polyvinyl chloride|in rolls|measuring
101|of an output|each valued
102|-
103|-
104|for motor vehicle|each valued
105|for anti-lock|each valued
107|-
108|programmable|measuring|incorporating
110|designed for use
111|of plastics|with an acrylic|in rolls measuring|valued not
112|with reciprocating|valued not
114|-
115|valued not
117|coated with
118|20.32 to|coated on|clear or|in rolls
119|measuring
120|coated on|any of the foregoing
121|laminated with|in rolls|of a kind used
122|consisting of|of a width
125|for use in|each measuring
126|each measuring|of an output|weighing
127|incorporating refrigerating|designed for commercial|each with a glass
128|incorporating refrigerating|each measuring|weighing|with one swing-type
130|each comprising|weighing|with a weight limit
131|not of the household|not specially designed|each such machine weighing|suitable for sewing
132|for automatic|each valued
133|for rendering
134|to enhance
136|constituting
138|each consisting of
139|of plastics|each comprising
140|of an output|each measuring|weighing|in a housing|with a switch
141|single phase AC|of an output|each with a spring|the assembly measuring
142|single phase|each of an output|measuring|with a shaft
143|incorporating permanent|each of an output|operating at|capable of operating|each weighing|measuring
144|other than gear motors, whether or not|each of an output|operating at|capable of operating|each weighing|measuring
145|for cable networks|that convert|each measuring|containing printed
148|for a weather sensor
151|for internal combustion
152|of plastics|for air horns
153|each with a ceramic
154|each having a power consumption|weighing
155|rated at
156|weighing
158|of a kind used
159|-
160|each consisting|put up for retail
161|for use with|each camera with|weighing|measuring|presented with
162|for use with|each camera with|weighing|measuring|presented with
163|for use with|each camera with|weighing|measuring|presented with
165|with a base|not flexible|with 10 layers|designed for use|measuring
166|each with a base|not flexible|with 2 layers
167|measuring|weighing|valued|of a kind used
169|capable of connecting|each capable of mixing|each measuring
170|for a voltage|fitted with connectors|each valued
171|of copper wire|for a voltage|each measuring|with National
172|of copper wire|for a voltage|each measuring|with National|with handles
173|not of a kind used|for a voltage|each with|for use in connecting
174|of a kind used|incorporating three|for a voltage
175|of plastics and steel
177|designed for use
178|of Society
180|of Society
181|of Society
182|of Stahlwerk
183|of Society|suitable for use
184|of steel|not suitable for towing|each receiver to be clamped|such bumpers
185|not motorized|each having
186|having both wheels|weighing|not designed for use
187|not motorized|having both wheels|each having
188|of carbon fiber|valued not
191|with diameter
192|each with magnification|weighing
193|each with magnification|weighing
194|each consisting
196|each consisting
197|designed for use
198|each consisting|weighing
199|-
200|with wooden frames other than chairs|not of cane|each measuring
202|for religious|capable of interlocking|each with attached
203|with metal frames|other than household|with seats and backs
204|of steel or aluminum|each of which
205|with metal frames|with seats and backs
206|of unfinished plywood
207|of cast aluminum|each measuring
208|of metal|each with integral|capable of being stacked
209|of base metal and rubber|designed for
211|of steel|other than for household|comprising vertical|each when fully assembled
213|of powder coated steel, whether or not|each measuring|with slanted shelves
214|with frames|each measuring|with a tabletop
215|of high-pressure|other than
217|with LED lamps|each measuring|having a wax
219|for outdoor use
220|of fabric
223|frozen in blocks|in cases with
224|frozen in blocks|in airtight containers
225|frozen in blocks|in airtight containers
226|frozen in blocks|in airtight containers
227|frozen in blocks|in airtight containers
228|-
229|-
230|-
231|in powder form
232|in powder or flake form|for manufacturing
234|in powder form
235|consisting of
236|of a kind used
237|for reduction|with oxides|applied to
238|for reduction|with base metals|applied on
239|for polymerization
240|of copper oxide|for arsine removal
241|with copper carbonate|for low temperature
242|with metal sulfide|for mercury removal
243|with molybdenum compounds|for hydrogenation
246|containing
247|containing
248|comprising mixtures
249|each weighing|designed for dispensing
250|of polypropiolactone|each comprising|measuring|weighing|of a kind used
251|of vulcanized rubber|each of an outside circumference|weighing
252|of polyester|each measuring|weighing
253|with hydration system|each measuring|weighing
254|with outer surface|each measuring
256|made predominantly|weighing|with wheels
257|of polyester|weighing
258|of leather|designed for use
259|of molded or pressed|each weighing
260|of molded or pressed|each weighing
261|containing|the foregoing not printed|not jacquard woven|measuring
262|containing|the foregoing not printed|not jacquard woven|measuring
263|of cashmere or camel hair|carded but not combed|not put up
264|of 100 percent|measuring|weighing
265|of 100 percent|dyed|weighing|measuring
267|containing|dyed|measuring|weighing
268|wholly of|weighing|measuring
269|wholly of polyester|dyed|not flat|containing|weighing|measuring
270|wholly of polyester|dyed|containing|weighing|measuring
271|containing by weight|dyed|containing textured|weighing|measuring
272|measuring
273|measuring
274|wholly of|weighing|measuring
275|of polyethylene|in sheets measuring|weighing
276|of hand-knotted pile|of nylon|measuring
278|containing by weight|weighing|measuring
279|of acrylic pile|valued not
280|of artificial staple fibers
281|known as brown wave|of a kind used|containing one textured|with a density
282|with a flamed finish|a length
283|of yttria-stabilized
284|of tempered safety glass|transparent, cut, and treated|with adhesive|in rectangular sheets|each weighing|each measuring
285|of tempered safety glass|coated with|having a surface area|designed to be placed
286|of convex glass|for motor vehicles|each measuring|weighing
287|of flat glass|for motor vehicles|each measuring|weighing
289|of non-recycled glass|on a vinyl mesh backing|in a grid pattern|for mosaics
290|comprising powder coated|the foregoing for assembly|with a load capacity
292|composed of steel wire|each measuring|weighing|designed as
293|of steel|each weighing|measuring|with spring loaded
294|-
295|of aluminum|for guitar sound modifying|each consisting
296|of iron or steel|non-electric, including
297|specially designed|each attachment including
298|of carbon alloy steel|of a kind used
300|of base metal
301|of steel
302|with digital keypads|of base metal|each weighing|measuring
303|suitable for use
304|of steel with rollers|suitable for use|each measuring|weighing
305|of steel|suitable for use|each measuring|weighing
306|-
307|for internal combustion
308|each composed|measuring|with a pump volume|for use in
309|each weighing|with a maximum pressure|imported with
311|-
312|of molded plastics|with clips
313|of plastics
314|of plastics|of a kind used|each set comprising
315|of plastics|of a kind used
316|of polystyrene plastics|each of a kind used
317|other than described|with floral
318|in chief weight|with hook and loop
319|of cotton knitted interlock|each with
320|of cotton interlock|sleeveless|each with
322|knitted|of cotton|each with
323|of cotton knitted interlock|each with
324|of polyester knitted fleece|sleeveless|each with
325|with muslin trim|each beltless
326|with muslin trim|each beltless
327|each beltless
328|of cotton|woven|each measuring
329|of cotton|other than woven|each measuring
330|of knitted polyester fabric|designed for
331|of muslin cotton|fitted with
333|of cotton for pillows|not knitted or crocheted|not napped or printed|each with
334|of cotton
335|-
336|comprising shells|each with an inner liner|designed for
337|of the household type|each weighing|having a touch screen
340|not capable of|each with a video
341|each consisting
342|-
344|other than for use|comprising a|with magnification
345|-
346|of cotton|each filled with
351|-
352|of a kind suitable
353|for Intra-operative|each composed
354|suitable for use
355|-
356|each having dimensions
363|of polyvinyl chloride|with lock connectors
364|presented with integrated|of polyvinyl chloride
366|each with display capabilities|of a kind used
368|of transparent plastics
369|in powder form
371|of nonwoven textile materials|impregnated, coated or covered|put up for retail
372|of high-density or low-density|111.75 cm|with a sticker|of a kind used
373|in bulk solid form
374|of acrylonitrile
375|each used to dispense
376|of plastics|each comprising|configured or fitted
377|incorporating LEDs|designed for use
378|designed for use
379|-
380|suitable for use
381|suitable for use
382|each incorporating
383|-
384|-
385|designed for use
386|of metal|for mobile
387|of polycaprolactone|for the use of
388|consisting of
389|of textile material|single-use
390|of textile materials
391|of cotton|in square or rectangular sizes
392|of plastics|designed to fit
395|of a kind used|each tube measuring|one end having|having an integrated flange|removable polyethylene caps|put up in sterile packing
396|laminated with|measuring|weighing
'''

def main():
 existing={x['index']:x for x in map(json.loads,(OUT/'reviewed_condition_groups.jsonl').read_text(encoding='utf-8').splitlines())}
 # Only preserve the originally written non-contiguous complete source readings.
 initial={15,20,27,29,54,86,106,109,113,116,147,150,176,210,245,339,6,87,95,129,137,149,164,189,195,216,218,291,338,365}
 prior={i:v for i,v in existing.items() if i in initial}
 plan={}
 for line in PLAN.strip().splitlines():
  line=line.strip()
  if not line:continue
  parts=line.split('|'); i=int(parts[0]); assert i not in plan
  plan[i]=parts[1:]
 out=[]
 for i,r in enumerate(rules):
  s=r['scope']; digest=hashlib.sha256(s.encode()).hexdigest()
  if r['whole_code'] or i in (135,299):
   out.append({'index':i,'rule_id':r['rule_id'],'scope':s,'scope_sha256':digest,
    'coarse_required_group_count':0,'groups':[],
    'taxonomic_temporal_gate':{'quote':s,'start':0,'end':len(s),'kind':'dated_code_transition' if i in (135,299) else 'whole_code_identity'},
    'complete_coarse_reading_silver':True,'atomic_necessary_condition_count':None,
    'note':'Zero additional product-description groups; code identity and any stated date branch remain legal requirements, not zero total conditions.',
    'status':'AI source-coded silver; code/date string is not a physical product predicate'})
   continue
  if i in prior:out.append(prior[i]);continue
  assert i in plan,('missing explicit reading',i,s)
  anchors=plan[i]; positions=[0]
  if anchors!=['-']:
   for anchor in anchors:
    p=s.find(anchor,positions[-1]+1);assert p>positions[-1],(i,anchor,s)
    positions.append(p)
  positions.append(len(s));groups=[]
  for a,b in zip(positions,positions[1:]):
   while a<b and (s[a].isspace() or s[a] in ',;'):a+=1
   while b>a and (s[b-1].isspace() or s[b-1] in ',;'):b-=1
   groups.append({'quote':s[a:b],'start':a,'end':b})
  out.append({'index':i,'rule_id':r['rule_id'],'scope':s,'scope_sha256':digest,
    'coarse_required_group_count':len(groups),'groups':groups,
    'aggregation_reading':'AND across coarse groups; internal category alternatives, constituent inventories, excluded alternatives, optional modifiers, dimensions of one entity, and guarded implications retain their source wording.',
    'complete_coarse_reading_silver':True,'atomic_necessary_condition_count':None,
    'note':'Explicit AI-selected start anchors after row-level source reading. A group can contain several atomic requirements or non-required optional modifiers. Count describes this coarse representation, not intrinsic legal complexity or independent expert truth.',
    'status':'AI source-coded silver; source span validated, semantic correctness not independently expert-validated'})
 for x in out:
  assert all(x['scope'][g['start']:g['end']]==g['quote'] for g in x['groups'])
 assert len(out)==397
 assert sum(bool(x['groups']) for x in out)==354
 (OUT/'reviewed_condition_groups.jsonl').write_text('\n'.join(json.dumps(x,ensure_ascii=False) for x in out)+'\n',encoding='utf-8')
 summary={'rows':len(out),'product_descriptions_with_coarse_groups':354,'code_only_with_no_extra_product_groups':43,'total_product_groups':sum(x['coarse_required_group_count'] for x in out),'representation_count_distribution':dict(collections.Counter(x['coarse_required_group_count'] for x in out if x['groups'])),'atomic_counts_asserted':False,'independent_expert_validation':False,'scope':'Counts concern explicit coarse source representation; no claim of intrinsic complexity or legal gold.'}
 (OUT/'coarse_group_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
