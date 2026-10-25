"""AI source coding of the outcome-masked, frozen visible inputs.
No administrative outcomes, holding text, or model predictions are read here.
The semantic judgments below were drafted by an AI agent after reading each input.
They are diagnostic references, not human/expert annotations or an automatic gold parser.
"""
from pathlib import Path
import json,hashlib,re
from collections import Counter
R=Path(__file__).resolve().parent
INPUT=R/'evidence_visible_inputs.jsonl'
rows=[json.loads(x) for x in INPUT.read_text(encoding='utf8').splitlines()]
assert len(rows)==73 and all('y' not in r for r in rows)
codes={}
def add(i,*conditions):codes[i]=list(conditions)
# A condition tuple is literal rule fragment, S/R/U, literal fact fragment(s), rationale.
S='support';RFT='refute';U='unknown'
def c(rule,state,facts='',reason=''):
    return (rule,{'S':S,'R':RFT,'U':U}[state],facts,reason or ('Direct statement or transparent ordinary-language entailment.' if state=='S' else 'The visible facts do not establish this condition.' if state=='U' else 'The visible facts explicitly conflict with this condition.'))
add(0,c('[M]onopolar conductors','S','single conducting aluminum core','A single conducting core supplies the monopolar description; protective CN strands are separately described.'),c('for a voltage exceeding 1,000 V','S','2000V'),c('other than of copper','S','single conducting aluminum core','The conducting core is aluminum; copper protective CN strands are distinguished in the facts.'),c('not fitted with connectors','U'))
add(1,c('Portable','S',['designed to be placed in the user’s pocket','meant to be placed in a pocket or purse']),c('wireless enabled','U','transmit the user’s results to its built-in screen without the support of any external wiring','Cordlessness and an internal display do not establish a wireless communications capability.'),c('electrical gas monitors','S',['only the gases from the user’s breath are measured','powered by batteries']))
add(2,c('Vacuum cleaners, bagless, upright','S','bagless, upright vacuum cleaners'),c('capable of operating in wet mode or dry mode','S','capable of operating in dry mode'),c('self-contained electric motor','S','self-contained electric motor'),c('power not exceeding 1,500 W','S','power not exceeding 1,500 W'),c('tank capacity not over 4 liters','S','dust receptacle capacity not over 4 liters','Dust receptacle is the stated collection tank; no contrary capacity appears. Model identifiers are not measurements.'))
add(3,c('Mouse input devices','U','golf simulator pads','Whether this sensing pad is a mouse input device requires a category interpretation absent from the supplied rule.'),c('for automatic data processing (ADP) machines','S','connects to a user’s computer via the USB port'),c('each valued over $70','U'))
add(4,c('Wireless communication apparatus','S','Bluetooth-enabled'),c('can receive audio data','S','with that received data being converted into sound'),c('to be distributed to wireless speakers','U','They can also be wired to a stereo system to reproduce audio over speaker wire.','Reception and local playback do not establish distribution to separate wireless speakers.'))
add(5,c('Wireless communication apparatus','S','wireless transceiver modules (Bluetooth and/or Wi-Fi)'),c('capable of receiving audio data','S','receives the data and converts it into the appropriate format (i.e., audio, video, data text)'),c('to be distributed to wireless speakers','U','presents it to the user as either music, video, or text on the screen','External wireless audio distribution is not stated.'))
add(6,c('Electric fireplaces','S','electric fireplace inserts'),c('weighing not more than 21 kg','S','weigh less than 21Kg.'))
add(7,c('[s]upported catalysts','U',['commercial invoice for the merchandise also describes the merchandise as a zinc oxide catalyst','functioning as an adsorbent material'],'The invoice category and described adsorbent function do not resolve the technical catalyst classification.'),c('zinc oxide as the active substance','S','zinc oxide is an active substance'))
add(8,c('Programmable DC electronic load instruments','S','programmable DC electronic load devices'),c('capable of presenting a constant load to a device, such as constant resistance, constant voltage, constant current, or constant power','S','They can be programmed to present a constant current or constant voltage to a device under test.'),c('weighing more than 4 kg but less than 8kg','S','weigh between 4.3kg to 5.1kg.'))
add(9,c('[C]arts, not mechanically propelled','S','non-mechanically propelled portable folding wagons'),c('each with three or four wheels','U'),c('of the kind used for household shopping','U','groceries, household supplies, plants, gardening items, ice chests, sports equipment','The broad list includes shopping but does not resolve the required kind-of-use category.'))
add(10,c('fabrics of man-made micro-denier fibers','U','wholly or predominantly of polyester, which is a man-made fiber','Man-made composition is established; micro-denier fineness is not supplied.'),c('impregnated, coated, covered, or laminated with polyurethane','S','All the samples were impregnated, coated, covered or laminated with the cellular polyurethane material'),c('width of at least 135 cm but not more than 150 cm','U'),c('weighing at least 206 g/m2 but not more than 500 g/m2','U'))
add(11,c('Sets of flatware','U','grill tool sets','Whether these grill implements satisfy flatware is not resolved by an explicit definition in the inputs.'),c('of stainless steel','U','The ends for interacting with food are steel.','Steel is given but stainless composition for all four sets is not established by the text.'),c('containing no article plated with precious metal','U'),c('put up for retail sale','U'))
add(12,c('Torque rods, also known as torque arms, radius rods or radius arms','U','control arm and ball joint assemblies','Equating suspension control arms with the enumerated torque/radius members requires technical category interpretation.'))
add(13,c('Household furniture','U','metal modular cabinet sets','The supplied storage use does not explicitly establish the household use class.'),c('of metal and high-pressure laminated bamboo','R','are unfinished because they are imported without their countertops.','The goods as imported lack countertops; the only future bamboo component is attached after importation.'),c('other than ironing boards, furniture for infants or children or bed frames','S','metal storage lockers and cabinets','The described storage cabinet forms exclude the listed alternative furniture forms.'))
for i in [14,16]:
    add(i,c('Synthetic silica gel','S','synthetic silica gel granules'),c('granules measuring 0.25 to 0.6 mm in diameter','S','synthetic silica gel granules, 0.25 to 0.6 millimeters (mm)','Granule size is given; diameter interpretation is the ordinary size descriptor, not an independent microscopy result.'),c('put up in retail packaging','S','packages for retail sale'),c('of a kind used for drying and preserving flowers','S' if i==14 else 'U','eight steps for using the silica gel to dry flowers' if i==14 else 'how to use Ultra Micro Crystals to dry flowers in five steps','Flower-drying packaging establishes the stated kind.' if i==14 else 'Primary cat-litter presentation and secondary flower instructions leave the legally relevant kind-of-use interpretation unresolved.'))
for i in [15,17]:add(i,c('Synthetic silica gel','S','synthetic silica gel granules'),c('in amorphous granules','S','amorphous and porous form of silicon dioxide'),c('of a kind used as a catalyst support','U','widely used as desiccants','Desiccant and retail uses do not establish catalyst-support suitability; absence is not explicit contradiction.'))
add(18,c('Hydraulic floor jacks','S','Arcan 3-ton Professional Grade Hybrid Service Jack','The named service jack with lifting capacity supplies the ordinary product type.'),c('of steel','S','68.50% by weight of steel','The article has a stated steel majority; this is a source-coded material reading, not expert legal adjudication.'),c('not more than 81 cm by 41 cm by 25 cm','S','61 centimeters (cm) by 30.2 cm by 15.2 cm'),c('weighing not more than 52 kg','S','weighs 26.4 kilograms (kg)'))
add(19,c('Hydraulic jacks of a kind for raising vehicles','S','Arcan 3-ton Professional Grade Hybrid Service Jack','Service jack is read in its ordinary vehicle-lifting sense.'),c('lifting capacity of not more than 550 kg','R','lifting capacity of 6,000 pounds','6000 international avoirdupois pounds = 2721.55422 kg; this exceeds 550 kg.'))
add(20,c('Vacuum cleaners, bagless','S','Bagless Upright Backpack Vacuum'),c('upright','U','worn as a backpack','The marketing title uses upright but the operating form is a backpack; the relevant category boundary is unresolved.'),c('self-contained electric motor','S','battery-powered vacuum'),c('power not exceeding 1,500 W','U'),c('dust receptacle capacity not exceeding 1 liter','S','dust receptacle capacity is 0.64 L'))
add(21,c('Filtering or purifying machinery or apparatus','S','devices used to filter out dirt and debris'),c('of a kind used for waste water treatment','U','swimming pool water','Whether recirculating pool water falls within waste-water treatment requires an absent scope definition.'))
add(22,c('Gloves','S','Work Gloves'),c('containing less than 50 percent by weight of textile fibers','U',['48% polyester','approximately 76% textile'],'Importer composition and laboratory result conflict. No source-priority rule is assumed in the input-evidence task.'),c('coated with rubber or plastics','S','knit polyester fabric coated in polyurethane'),c('designed for enhanced grip','S','gloves are designed for enhanced grip'))
add(23,c('parts of counters, racks, display cases, and similar fixtures of base metal','S','steel shelves (both solid and wire) and posts used to assemble adjustable shelving units'),c('other than welded wire rack decking','U','both solid and wire','The wire shelves are not characterized sufficiently to exclude welded wire decking.'))
add(24,c('Regenerative speed drive controllers','S',['speed drive controller','braking (regenerative) mode']),c('for controlling speed of electric motors for elevators','S','designed to control electric motors, including elevator motors'))
add(25,c('Apparatus using passive infrared detection sensors','U',['infrared emitter and receiver diode','front light sensor uses infrared receiver diodes'],'The combined apparatus uses active rain sensing and infrared receivers; the passive-detection characterization for the light-control function is not explicitly established.'),c('designed for turning lights on and off','S','automatically control the vehicle’s low beams and instrument lighting'))
add(26,c('Thermostats designed for air conditioning or heating systems','S','provide HVAC controls'),c('not designed to connect to the internet','S','no functionality in an internet-based/wireless environment'),c('designed for wall mounting','S','affixed to the wall'))
add(27,c('Salad spinners','S','identified as a Salad Spinner'),c('of plastic','S','plastic body'),c('not electrically powered','S','mechanical feature, which incorporates a handle that initiates the spinner','The described manual actuation establishes the non-electrical operating design.'))
add(28,c('Vulcanized rubber tracks','S','encased in vulcanized rubber'),c('each incorporating cords and cleats of steel','S','dropped forged steel drive lugs and woven steel cords','Drive lugs are the described cleats.'),c('designed for use on construction equipment','S','excavators, loaders, crawlers, pavers, trenchers and other excavating machines'))
for i in [29,30,31]:
    qs=['wheel under consideration','axle supports','pedal assembly'][i-29]
    add(i,c('Tines, carriages, and other goods handling apparatus and parts','U',qs,'Whether these propulsion/chassis/control components are parts of goods-handling apparatus rather than other truck parts needs category interpretation.'),c('designed for use on fork lift and other works trucks','S',['aerial work platforms and scissor lifts','Telehandler fork-lifting machine','forklifts and other work trucks'][i-29]))
# Shared rule family: legal motorcycle taxonomy is not silently inferred from
# motor presence or from compatible digits. Numeric predicates are coded apart.
motor_indices=[32,34,40,41,42,49,51,60,61,65,66,67,68,69,71]
power_quotes={32:['300-watt','250-watt'],34:'250 watt electric motor',40:['350 watts','450 watts','600 watts','720 watts','500 watt'],41:'500 watt electric motor',42:'500-watt',49:'750W rear-mounted hub motor',51:'1,000W rear-mounted brushless motor',60:['350W','500W'],61:['750W','350W'],65:'750W motor',66:'350W electric bicycle',67:'2 x 500-Watt electric motors',68:'350-watt capacity',69:['nominal power of 1,000W','maximum peak power of 3,000W'],71:'250W electric motor'}
for i in motor_indices:
    rule=rows[i]['rule_text']; typ='[m]otorcycles' if '[m]otorcycles' in rule else 'Motorcycles'
    pq=power_quotes[i]
    add(i,c(typ,'U',rows[i]['facts'],'The literal rule supplies no legal definition connecting this bicycle, scooter or other vehicle form to the motorcycle category. Compatible tariff digits alone do not establish this narrower description.'),c('with electric power for propulsion','S',pq,'An electric drive is stated; whether pedal-only assistance satisfies the legal category is retained in the separate type uncertainty.'),c('each of a power not exceeding 1,000 W','U' if i==69 else 'S',pq,'Nominal and peak ratings straddle the ceiling and the supplied rule does not identify the relevant rating.' if i==69 else 'All explicitly specified drive powers satisfy the inclusive ceiling; for two 500-W motors their stated sum is 1000 W.'))
add(33,c('Power supplies suitable for physical incorporation into automatic data processing (ADP) machines or units thereof of heading 8471','S','Power Supply for a Personal Computer'),c('power output exceeding 500 W','S','maximum power output of 850 Watts'),c('measuring 148mm in length, 43 mm in width and 335 mm in height','R','measuring 140 mm by 150 mm by 86 mm','No permutation of the three actual enclosure dimensions equals the specified dimensions.'))
for i in [35,47,52,53]:
    add(i,c('Upholstered dining chairs','U',rows[i]['facts'],'The articles are bar/counter stools; whether these constitute dining chairs needs a category definition absent from the input.'),c('with a wooden frame','S',['wood frame','wood frame','eucalyptus and birch wood frame','rubberwood frame'][[35,47,52,53].index(i)]),c('other than of teak','S' if i in [52,53] else 'U','eucalyptus and birch wood frame' if i==52 else 'rubberwood frame' if i==53 else ''))
add(36,c('Electromechanical relays','S','electromechanical power relay'),c('for a voltage exceeding 60 V but not over 250 V','U',['coil voltage rating of 12 VAC','contact voltage rating of 277 VAC'],'Coil and contact voltages differ; the excerpted rule does not identify which rating controls. Under contact-voltage reading all exceed 250 V; the ambiguity is retained.'),c('with contacts rated at 10 A or more','S',['rated at 30 A','at 40 A']))
add(37,c('Parts and accessories of machines of heading 8471','S','aluminum alloy enclosures for all-in-one personal computers'),c('not incorporating goods of headings 8541 or 8542','R','diodes, transistors, and integrated circuits','The named components are the semiconductor/IC categories referred to by those headings; this standard heading-to-component mapping is an explicit coding assumption.'))
add(38,c('Push-pull switches','S','Push-Pull Switches'),c('for a voltage not exceeding 1,000 V','S','rated at 12 VDC'),c('designed for use in motor vehicles','S','of an automobile'))
add(39,c('Skateboards','U','one-wheeled electric vehicle','Whether the single-wheel cycle falls in the skateboard category is not established by the quoted text.'),c('with electric power for propulsion','S','powered by a 250W brushless motor'),c('of a power not exceeding 250W','S','250W brushless motor'))
add(43,c('Knobs','S',['operating knob','pushbutton style operating knob']),c('of injection molded plastics','S',['two injection molded plastic parts','three injection molded plastic parts']))
add(44,c('Molded buttons','S',['injection molded plastic buttons','compression molded silicone switch pad'],'Both are molded external switch actuation elements; grouping the switch-pad buttons is an explicit ordinary component reading.'))
for i in [45,46,48,62]:
    f=rows[i]['facts']; fabric=next(q for q in ['nonwoven polypropylene fabric','non-woven polypropylene material','nonwoven fabric comprised of manmade fibers','nonwoven textile fabric'] if q in f)
    add(i,c('Face masks','S','face mask'),c('single-use','S','disposable'),c('of textile fabrics','S',fabric))
add(50,c('Disposable shoe and boot covers','S','disposable shoe cover'),c('of man-made fiber fabrics','S','nonwoven polypropylene fabric'))
for i in [54,57,59,63]:
    f=rows[i]['facts'];fq=next(q for q in ['polyester and 10 percent spandex knit fabric','polyester and 5 percent spandex knit jersey fabric','polyester and 20 percent cotton woven fabric','nonwoven polypropylene textile fabric'] if q in f)
    add(i,c('Face masks, and particulate facepiece respirators','S','face covering' if 'face covering' in f else 'face mask','The listed product alternatives include face masks; a particulate-respirator function is not imposed on the mask branch.'),c('of textile fabrics','S',fq))
add(55,c('Photovoltaic generators','S',['USB Solar Panel Power Source (Generator)','polycrystalline panel']),c('of a kind described in statistical note 9 to chapter 85','U','Generator','The incorporated note is not part of the visible input; its full conditions cannot be verified.'),c('output not exceeding 150 W','S','maximum power output of 1.5 W'))
add(56,c('Outdoor household seats','S',['outdoor armless chair','outdoor seat'],'The listed patio-style seating is read in its ordinary household seating sense.'),c('aluminum frames','S','frame are constructed of aluminum metal'),c('covered in polyethylene rattan wicker','S','Interlacing PE imitation rattan wicker covers the metal frame'),c('with textile covered cushions','S','textile covered cushion'))
add(58,c('Printed circuit board assemblies','S','models of PCB’s'),c('of a kind used in motor vehicle lighting systems','S','used in motor vehicle LED lighting'))
add(64,c('Parts of chairs','S','unassembled seat components'),c('of unfinished plywood','U',['metal frames, plywood seat decks','PP injection molded fire rated foam seat shells'],'Some components are plywood but unfinished status and which component the pair denotes are not specified uniformly.'),c('including bodies, legs and arms','S','unassembled seat components','Including is illustrative, not an additional mandatory conjunction.'))
add(70,c('Tire carrier attachments, roof racks, fender liners, side protective attachments','R','components that are used to make a sound/speaker bar housing','A speaker-bar housing does not have any of the listed carrier/protective functions in the described use.'),c('the foregoing of steel','R','made of acrylonitrile styrene acrylate (ASA) plastic'))
add(72,c('Parts and accessories of machines of heading 8471','S','specifically designed to accommodate Intel 115x,1200,1700 processors, as well as the AMD AM5, AM4 processors'),c('whether or not incorporating fan hubs or LEDs','S','three LED lighted fans','Fan hubs and LEDs are expressly allowed, so presence is not a defeating exception.'),c('but not incorporating other goods of headings 8541 or 8542','U','an aluminum radiator, a copper block, three LED lighted fans, and a pump','The list does not explicitly exclude other semiconductor/control electronics inside the pump or fans.'))

def span(text,quote):
    found=text.find(quote)
    if found<0:raise ValueError(('quote-not-found',quote,text[:100]))
    return [found,found+len(quote)]
def structured_node(cid,rule):
    # Keep signed literal clauses and the original operator instead of flattening
    # an alternative or exception into unrelated conjunctive requirements.
    if rule=='capable of operating in wet mode or dry mode':
        return {'op':'any','source_condition':cid,'children':[{'literal':'wet mode'},{'literal':'dry mode'}], 'evaluate':'source_coded_whole_disjunction'}
    if 'other than' in rule or rule.startswith('not ') or 'but not incorporating' in rule:
        return {'op':'exclusion','source_condition':cid,'signed_literal':rule,'evaluate':'source_coded_signed_condition'}
    if 'whether or not' in rule:return {'op':'permitted_optional','source_condition':cid,'literal':rule}
    if re.search(r'\bor\b|Face masks, and particulate|Tire carrier attachments|Tines, carriages',rule):
        return {'op':'any_or_illustrative_list','source_condition':cid,'literal':rule,'evaluate':'source_coded_whole_clause','no_flattening':True}
    if 'such as' in rule or rule.startswith('including'):return {'op':'illustrative','source_condition':cid,'literal':rule}
    return {'op':'condition','ref':cid}

assert set(codes)==set(range(73)),set(range(73))-set(codes)
out=[]
for i,row in enumerate(rows):
    conditions=[]
    for j,(rq,state,fq,reason) in enumerate(codes[i]):
        # Bracketed initial capitals from official quotations are substantive
        # source strings; retain exact source spelling, not editorial repair.
        if rq not in row['rule_text'] and rq.startswith('parts') and '[p]arts' in row['rule_text']:rq='[p]arts'+rq[5:]
        if rq not in row['rule_text'] and rq.startswith('fabrics') and '[f]abrics' in row['rule_text']:rq='[f]abrics'+rq[7:]
        quotes=[fq] if isinstance(fq,str) and fq else fq if isinstance(fq,list) else []
        conditions.append({'condition_id':f'c{j+1}','rule_quote':rq,'rule_span':span(row['rule_text'],rq),
                           'evidence_state':state,'fact_evidence':[{'quote':q,'span':span(row['facts'],q)} for q in quotes],
                           'rationale':reason,'coding_status':'AI_source_coded_diagnostic_reference'})
    state='refute' if any(c['evidence_state']=='refute' for c in conditions) else 'unknown' if any(c['evidence_state']=='unknown' for c in conditions) else 'support'
    out.append({'case_id':row['case_id'],'visible_input_sha256':hashlib.sha256(json.dumps(row,sort_keys=True,ensure_ascii=False).encode()).hexdigest(),
                'conditions':conditions,'logical_structure':{'op':'all','children':[structured_node(c['condition_id'],c['rule_quote']) for c in conditions]},
                'aggregate_evidence_state':state,'administrative_label_visible_during_coding':False,
                'reference_status':'AI-assisted diagnostic reference; no human or expert annotation',
                'scope':'Only frozen visible facts plus literal candidate scope; no ruling analysis or administrative decision supplied.'})
(R/'evidence_condition_codes.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in out),encoding='utf8')
summary={'n_cases':len(out),'n_conditions':sum(len(r['conditions']) for r in out),'states':dict(Counter(r['aggregate_evidence_state'] for r in out)),
         'input_sha256':hashlib.sha256(INPUT.read_bytes()).hexdigest(),'all_spans_valid':True,'coding_agent':'Codex / tariff_data',
         'independence_limit':'Administrative outcomes and model predictions were excluded from this coding script and coding view. The coding agent had participated in the prior study and remembered some cases; this is outcome-masked coding, not a claim of uninformed human blinding.',
         'second_pass_status':'pending independent AI read-only review','human_expert_review':False}
(R/'evidence_coding_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
print(json.dumps(summary,indent=2))
