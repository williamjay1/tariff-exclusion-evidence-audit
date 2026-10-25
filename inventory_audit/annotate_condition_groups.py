"""Source-anchored clause-group readings; no primitive-atom/legal-truth claim."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
rules=[json.loads(x) for x in (ROOT/'datasets/statutory_rules.jsonl').read_text(encoding='utf-8').splitlines()]
# Explicitly selected complete coarse groups. A categorical alternative or component inventory
# remains ONE group; numeric lower+upper for one attribute remain ONE group.
GROUPS={
15:['Filtering or purifying machinery or apparatus','of a kind used for waste water treatment'],
20:['Filter housings, covers, or couplings','of steel','comprising parts of machinery or apparatus for filtering liquids'],
27:['Tines, carriages, and other goods handling apparatus and parts','designed for use on fork lift and other works trucks'],
29:['Vulcanized rubber tracks','each incorporating cords and cleats of steel','designed for use on construction equipment'],
54:['Regenerative speed drive controllers','for controlling speed of electric motors for elevators'],
86:['Thermostats','designed for air conditioning or heating systems','not designed to connect to the internet','designed for wall mounting'],
106:['Apparatus','using passive infrared detection sensors','designed for turning lights on and off'],
109:['Monopolar conductors','for a voltage exceeding 1,000 V','other than of copper','not fitted with connectors'],
113:['Motorcycles','with electric power for propulsion','each of a power not exceeding 1,000 W'],
116:['electrical gas monitors','Portable','wireless enabled'],
147:['Static converters','of a kind used to charge telecommunication apparatus in cars or homes','valued not over $2 each'],
150:['Vacuum cleaners','bagless','upright','each with self-contained electric motor of a power not exceeding 1,500 W','having a dust receptacle capacity not exceeding 1 liter'],
176:['Tire carrier attachments, roof racks, fender liners, side protective attachments','of steel'],
210:['Household furniture','of metal and high-pressure laminated bamboo','other than ironing boards, furniture for infants or children or bed frames'],
245:['Supported catalysts','with zinc oxide as the active substance'],
339:['Wireless communication apparatus','that can receive audio data to be distributed to wireless speakers'],
6:['Rotary compressors','each exceeding 746 W but not exceeding 2,238 W','with a cooling capacity ranging from 2.3 kW to 5.5 kW'],
87:['Battery balancers','designed for regulating voltage across batteries','other than for 6, 12 or 24 volt systems'],
95:['DC electric motors','12 V','with an output exceeding 74.6 W but not exceeding 735 W','with lead wires and electrical connector','measuring not over 75 mm outside diameter','with a housing not over 100 mm in length','a shaft not over 60 mm in length'],
129:['Compact portable shipping scales','of stainless steel','with a maximum weighing capacity of not more than 16 kg','with a digital display, weight below hook, and handles','measuring not less than 19 cm in width, not less than 21 cm in depth, not less than 3 cm in height but not more than 52 cm in width, not more than 41 cm in depth, not more than 13 cm in height'],
137:['Parts and accessories of machines of heading 8471','not incorporating other goods of heading 8541 or 8542'],
149:['Robotic vacuum cleaners','designed for residential use','each with a self-contained electric motor of a power not exceeding 50 W','dust bag/receptacle capacity not exceeding 1 L'],
164:['Printed circuit boards','each with a base wholly of plastics impregnated glass','not flexible','with 4 layers of copper'],
189:['Wheeled trailers','suitable for towing behind an adult bicycle','each comprising a frame of aluminum with a hitch mechanism','weighing not more than 17.5 kg','with a capacity of not more than 46 kg','with those trailers designated for carrying children meeting ASTM International standard F1975'],
195:['Parts and accessories of meteorological instruments and appliances','each consisting of an assembly comprising 3 rotating wind cups, bearings, an internal aspirating fan and one or more solar panels'],
216:['Baby crib liners','each composed of two pieces of multi-layer warp polyester knit mesh','without any padding','one measuring no more than 29 cm by 283 cm and the other measuring no more than 29 cm by 210 cm'],
218:['Flexible strips','each having embedded light-emitting diodes electrically connected to a molded electrical end connector','each strip wound onto a reel measuring not more than 25 cm in diameter and not more than 1.5 cm in width'],
291:['Portable outdoor cooker kits','consisting of at least a burner and stand made from steel and/or cast iron','with an adjustable pressure regulator/hose combination for connecting the burner to a source of natural gas or a portable container of liquefied propane'],
338:['Tracking devices','each device measuring not more than 86 mm on a side (if rectangular) or 28 mm in diameter (if circular)','not more than 7.5 mm in thickness','not weighing more than 15 g','designed to be attached to another article','to establish a Bluetooth connection with another device for the purposes of providing relative location information'],
365:['Sacks and bags','of polymers of ethylene','reclosable','qualifying as Class 1 medical devices by the U.S. Food and Drug Administration under product code NNI'],
}
NOTES={
 6:'Two different power-related attributes; one class group and two magnitude groups.',
 87:'Third group is NOT(any of discrete voltage-system alternatives).',
 95:'Lead-wire/connector inventory grouped once; motor, housing and shaft have distinct dimensions.',
 109:'Material and monopolar interpretation require legal/domain reading; four groups are not four resolved Boolean facts.',
 129:'Dimensions grouped as one vector; capacity and actual scale mass must not be confused. This index wording does not settle every measurement boundary.',
 137:'Optional fan hubs/LEDs are not required groups; whether goods are within referenced headings remains external.',
 149:'Optional accessories omitted from necessary groups, but retained in original scope.',
 189:'Last group is an implication: child-carrying designation => standard compliance; it is NOT unconditional certification requirement.',
 195:'Inventory group expands to distinct count predicates and required bearings/fan; count2 is coarse groups, not primitive atoms.',
 216:'One/other dimension assignment is paired to separate pieces, not interchangeable total size.',
 218:'Dimensions attach to reel, not strip.',
 291:'Minimum inventory burner+stand; material and fuel alternatives nested within component relations.',
 338:'Shape-guarded dimension branch; no interpretation for unspecified other shapes is imposed.',
 365:'External regulatory meaning not supplied by this inventory.'
}
out=[]
for i,groups in GROUPS.items():
 s=rules[i]['scope'];a=[]
 for g in groups:
  p=s.find(g);assert p>=0,(i,g)
  a.append({'quote':g,'start':p,'end':p+len(g)})
 out.append({'index':i,'rule_id':rules[i]['rule_id'],'scope':s,'scope_sha256':hashlib.sha256(s.encode()).hexdigest(),'coarse_required_group_count':len(a),'groups':a,'aggregation_reading':'AND across groups, with category alternatives, component inventories, vectors and guarded implications internal to groups','complete_coarse_reading_silver':True,'atomic_necessary_condition_count':None,'note':NOTES.get(i,'Category alternatives and composite attribute clauses are retained inside groups; this is not an executable legal ontology.'),'status':'AI source-coded silver; source span validated, semantic correctness not independently expert-validated'})
(OUT/'reviewed_condition_groups.jsonl').write_text('\n'.join(json.dumps(x,ensure_ascii=False) for x in out)+'\n',encoding='utf-8')
print('Coarse group source-span checks passed:',len(out))
