"""Reproducible vector-first artwork; no interpolated raster detail."""
from pathlib import Path
import os,sys,json,itertools,hashlib
ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'artwork'
for p in [ART/'figures',ART/'previews',ART/'qa',ROOT/'temp/mpl']:
    p.mkdir(parents=True,exist_ok=True)
os.environ['MPLCONFIGDIR']=str(ROOT/'temp/mpl')
os.environ['TEMP']=os.environ['TMP']=str(ROOT/'temp')
sys.path.insert(0,r'C:\Users\Administrator\.agents\skills\sci-figures')
from figstyle import apply_house_style,mm,audit
from matplotlib.patches import Rectangle,FancyArrowPatch
from matplotlib.text import Text
from matplotlib.path import Path as MplPath
import numpy as np
plt=apply_house_style(styles=('science','nature','no-latex'),fontsize=8)
plt.rcParams.update({'font.family':'Arial','axes.labelsize':8,'xtick.labelsize':7.5,
 'ytick.labelsize':7.5,'savefig.bbox':None,'axes.linewidth':.65,'xtick.major.size':2.5,
 'xtick.minor.visible':False,'ytick.minor.visible':False,'xtick.direction':'out',
 'ytick.direction':'out','figure.facecolor':'white','svg.hashsalt':'tariff-evidence-audit-20261023'})
BLUE='#0072B2';ORANGE='#D55E00';TEAL='#008577';GREY='#A8B3BD';DARK='#253039'
PALE='#F1F5F7'
def txt(fig,x,y,s,**kw):
    return fig.text(x,y,s,fontfamily='Arial',fontsize=kw.pop('fontsize',8),
                    color=kw.pop('color',DARK),**kw)
def header(fig,y,letter,title):
    txt(fig,.025,y,letter,fontweight='bold',fontsize=9,va='center')
    txt(fig,.062,y,title,fontweight='bold',fontsize=9,va='center')
def box(fig,x,y,w,h,title,body,color=BLUE):
    fig.patches.append(Rectangle((x,y),w,h,transform=fig.transFigure,
                                facecolor=PALE,edgecolor='#CBD3DA',lw=.65,zorder=-1))
    fig.patches.append(Rectangle((x,y+h-.007),w,.007,transform=fig.transFigure,
                                facecolor=color,lw=0,zorder=-1))
    txt(fig,x+.015,y+h-.045,title,fontweight='bold',va='top',fontsize=8)
    txt(fig,x+.015,y+h-.105,body,va='top',linespacing=1.55,fontsize=7.6)
def arrow(fig,x1,y1,x2,y2):
    p=FancyArrowPatch((x1,y1),(x2,y2),transform=fig.transFigure,
       arrowstyle='-|>',mutation_scale=8,linewidth=.85,color='#6C7B86',
       shrinkA=0,shrinkB=0)
    fig.patches.append(p)
def finish(fig,stem,sources=(),data_axes=()):
    fig.canvas.draw();ren=fig.canvas.get_renderer()
    ts=[t for t in fig.findobj(Text) if t.get_visible() and t.get_text().strip()]
    # Matplotlib creates invisible tick/title copies. Only nonempty visible text
    # is checked, including title slots and figure-level annotations.
    boxes=[(t,t.get_window_extent(ren)) for t in ts]
    outside=[];overlap=[];intrusions=[]
    for t,b in boxes:
        if b.x0<-.2 or b.y0<-.2 or b.x1>fig.bbox.width+.2 or b.y1>fig.bbox.height+.2:
            outside.append(t.get_text())
        for ax in data_axes:
            r=ax.get_window_extent(ren)
            if min(b.x1,r.x1)-max(b.x0,r.x0)>.5 and min(b.y1,r.y1)-max(b.y0,r.y0)>.5:
                intrusions.append(t.get_text())
    for (ta,a),(tb,b) in itertools.combinations(boxes,2):
        w=min(a.x1,b.x1)-max(a.x0,b.x0);h=min(a.y1,b.y1)-max(a.y0,b.y0)
        if w>.5 and h>.5:overlap.append([ta.get_text(),tb.get_text()])
    line_hits=[]
    # Diagram arrows and plot Line2D paths must not cross annotation boxes.
    paths=[]
    for p in fig.patches:
        if isinstance(p,FancyArrowPatch):paths.append(p.get_path().transformed(p.get_transform()))
    for ax in fig.axes:
        for line in ax.lines:
            paths.append(line.get_path().transformed(line.get_transform()))
    for t,b in boxes:
        for path in paths:
            # CLOSEPOLY's dummy (0,0) is not a drawn vertex. Test each real
            # segment separately, preventing a spurious line to the origin.
            hit=False; previous=None; first=None
            for vertices,code in path.iter_segments(curves=False,simplify=False):
                endpoint=vertices[-2:]
                if code==MplPath.MOVETO:previous=endpoint;first=endpoint;continue
                if code==MplPath.CLOSEPOLY:endpoint=first
                if previous is not None and endpoint is not None:
                    segment=MplPath([previous,endpoint])
                    if segment.intersects_bbox(b.padded(1.0),filled=False):hit=True;break
                previous=endpoint
            if hit:line_hits.append(t.get_text())
    house=audit(fig,verbose=False)
    report={'status':'PASS' if house['ok'] and not (outside or overlap or intrusions or line_hits) else 'FAIL',
     'house_style':house,'fixed_canvas_mm':[round(v*25.4,2) for v in fig.get_size_inches()],
     'dpi':1200,'min_font_pt':min(t.get_fontsize() for t in ts),'text_boxes':len(boxes),
     'outside_canvas':outside,'text_text_overlap':overlap,'text_in_data_regions':intrusions,
     'text_line_intersections':line_hits,
     'sources':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}}
    (ART/'qa'/f'{stem}.json').write_text(json.dumps(report,indent=2,default=lambda v:v.item()),encoding='utf8')
    assert report['status']=='PASS',report
    for ext in ['pdf','svg','png']:
        fig.savefig(ART/'figures'/f'{stem}.{ext}',dpi=1200,bbox_inches=None,pad_inches=0,facecolor='white')
    fig.savefig(ART/'previews'/f'{stem}.png',dpi=220,bbox_inches=None,pad_inches=0,facecolor='white')
    plt.close(fig)
    print(json.dumps({'figure':stem,'status':report['status'],'size_mm':report['fixed_canvas_mm'],'dpi':1200}))

def figure1():
    fig=plt.figure(figsize=(mm(183),mm(153)))
    header(fig,.963,'a','Audit the construction of the model input')
    x=[.03,.365,.70];w=.27
    box(fig,x[0],.665,w,.235,'Public source','Rule quoted in the ruling\nComplete retained public text\nParty / laboratory / agency')
    box(fig,x[1],.665,w,.235,'Admitted attributes','Descriptive assertions\nExact spans and attribution\nOriginal and restored inputs')
    box(fig,x[2],.665,w,.235,'Separate interpretation','Definitions and categories\nApplication and holding\nDisputed scope or sources',ORANGE)
    arrow(fig,.304,.779,.351,.779);arrow(fig,.639,.779,.686,.779)
    header(fig,.595,'b','Represent what the evidence is about')
    box(fig,.03,.315,.44,.22,'Condition record','Object + signed predicate + logical role\nQuantifier + attribute + unit / rating basis\nDirect / interpretive / insufficient / disputed')
    box(fig,.53,.315,.44,.22,'Evidence record','Quote + source locator + statement class\nAvailable in excerpt or restored from source\nExplicit mapping options; unresolved stays visible',TEAL)
    arrow(fig,.482,.425,.518,.425)
    header(fig,.246,'c','Evaluate state tracking and required action')
    txt(fig,.037,.178,'Supported / refuted / unknown',fontweight='bold',fontsize=8.2)
    txt(fig,.037,.115,'Aggregate mandatory conjuncts under the stated policy; preserve decisive refutations.',fontsize=7.8)
    txt(fig,.037,.066,'Test gaps, restoration, irrelevant facts, decisive changes and object binding.',fontsize=7.8)
    finish(fig,'figure1_source_protocol')

def figure2():
    source=ROOT/'source_audit/source_audit_summary.json'
    d=json.loads(source.read_text(encoding='utf8'))
    assert d['conditions']==208 and d['cases']==73
    fig=plt.figure(figsize=(mm(183),mm(145)))
    header(fig,.957,'a','Condition coding layers')
    txt(fig,.965,.920,'208 historical condition units',ha='right',fontsize=7.7)
    cats=['Direct, scored','Direct, nonbinding','Interpretive','Insufficient','Disputed']
    vals=[d['reference_tier_counts']['direct']-2,2,d['reference_tier_counts']['interpretive'],
          d['reference_tier_counts']['insufficient'],d['reference_tier_counts']['disputed']]
    assert sum(vals)==208
    ax=fig.add_axes([.32,.565,.57,.29]);y=np.arange(5)[::-1]
    ax.barh(y,vals,height=.57,color=[BLUE,'#D8E1E7',TEAL,GREY,ORANGE],edgecolor='white',lw=.4)
    ax.set(xlim=(0,140),ylim=(-.5,4.5),yticks=[],xticks=[0,50,100])
    ax.spines[['top','right','left']].set_visible(False)
    ax.tick_params(top=False,bottom=True,labeltop=False)
    ax.set_xlabel('Number of condition units',labelpad=5)
    for yi,label,n in zip(y,cats,vals):
        yf=fig.transFigure.inverted().transform(ax.transData.transform((0,yi)))[1]
        txt(fig,.035,yf,label,va='center')
        txt(fig,.96,yf,str(n),ha='right',va='center',fontweight='bold')
    header(fig,.443,'b','Direct-text policy before and after source restoration')
    bx=fig.add_axes([.32,.178,.40,.17]);yy=np.array([1,0]);left=np.zeros(2)
    keys=['support','refute','unknown','not_applicable']
    colors=[BLUE,ORANGE,GREY,'#E5EBEF']
    for k,c in zip(keys,colors):
        values=[d['strict_excerpt_condition_counts'][k],d['strict_full_condition_counts'][k]]
        bx.barh(yy,values,left=left,height=.48,color=c,edgecolor='white',lw=.55);left+=values
    bx.set(xlim=(0,208),ylim=(-.5,1.5),yticks=[],xticks=[0,100,200])
    bx.spines[['top','right','left']].set_visible(False)
    bx.tick_params(top=False,bottom=True,labeltop=False)
    bx.set_xlabel('Number of condition units',labelpad=5)
    colx=[.78,.835,.895,.956]
    for xf,s in zip(colx,['S','R','U','N/A']):txt(fig,xf,.376,s,ha='center',fontsize=7.5,fontweight='bold')
    for yi,key,label in zip(yy,['strict_excerpt_condition_counts','strict_full_condition_counts'],['Original excerpt','Direct facts restored']):
        yf=fig.transFigure.inverted().transform(bx.transData.transform((0,yi)))[1]
        txt(fig,.035,yf,label,va='center')
        for xf,k in zip(colx,keys):txt(fig,xf,yf,str(d[key][k]),ha='center',va='center')
    txt(fig,.035,.060,'Four attributes recovered in three cases; none alone resolves the full case.',fontsize=7.6)
    txt(fig,.035,.023,'S, supported; R, refuted; U, unknown. Two units are nonbinding examples or permissions.',fontsize=7.3)
    finish(fig,'figure2_source_audit',[source],[ax,bx])

def figure3():
    source=ROOT/'experiments/outputs/qwen14_controlled_cases_functional_analysis.json'
    d=json.loads(source.read_text(encoding='utf8'))
    direct=d['reports']['direct']; structured=d['reports']['checklist']
    a=direct['overall'];b=structured['overall']
    assert a['n']==b['n']==108 and b['condition_n']==216
    fig=plt.figure(figsize=(mm(183),mm(170)))
    header(fig,.967,'a','Whole-input state tracking')
    ax=fig.add_axes([.36,.790,.43,.103])
    vals=[a['decision_correct'],b['decision_correct']]
    ax.barh([1,0],vals,height=.46,color=[GREY,BLUE],edgecolor='white',lw=.5)
    ax.set(xlim=(0,108),ylim=(-.6,1.6),yticks=[],xticks=[0,36,72,108])
    ax.spines[['top','right','left']].set_visible(False)
    ax.tick_params(top=False,labeltop=False)
    for yi,label,n in zip([1,0],['Direct decision','Supplied checklist'],vals):
        yf=fig.transFigure.inverted().transform(ax.transData.transform((0,yi)))[1]
        txt(fig,.035,yf,label,va='center')
        txt(fig,.96,yf,f'{n}/108',ha='right',va='center',fontweight='bold')
    txt(fig,.79,.749,'Correct inputs',ha='right',fontsize=7.5)
    header(fig,.702,'b','Inspect the checklist outputs')
    metrics=[('Condition states',b['condition_correct'],b['condition_n']),
             ('Acceptable evidence IDs',b['evidence_id_acceptable']['correct'],b['evidence_id_acceptable']['scored']),
             ('State and evidence jointly',b['evidence_id_acceptable']['joint_state_and_evidence_correct'],b['evidence_id_acceptable']['scored']),
             ('Exact request sets',b['requests']['exact_case_sets'],b['n'])]
    bx=fig.add_axes([.36,.476,.43,.164]);yy=np.arange(4)[::-1]
    bx.barh(yy,[100*n/m for _,n,m in metrics],height=.47,color=BLUE,edgecolor='white',lw=.5)
    bx.set(xlim=(0,100),ylim=(-.5,3.5),yticks=[],xticks=[0,50,100])
    bx.spines[['top','right','left']].set_visible(False)
    bx.tick_params(top=False,labeltop=False)
    for yi,(label,n,m) in zip(yy,metrics):
        yf=fig.transFigure.inverted().transform(bx.transData.transform((0,yi)))[1]
        txt(fig,.035,yf,label,va='center')
        txt(fig,.96,yf,f'{n}/{m}',ha='right',va='center',fontweight='bold')
    txt(fig,.79,.433,'Agreement (%)',ha='right',fontsize=7.5)
    header(fig,.389,'c','Correct paired behavior under controlled changes')
    operations=[('delete_evidence','Evidence deletion'),('restore_evidence','Evidence restoration'),
                ('irrelevant_addition','Irrelevant addition'),('decisive_change','Decisive change'),
                ('retain_refutation','Refutation retained'),('binding_swap','Object-binding swap'),
                ('equivalent_expression','Equivalent expression'),('other_object_only','Other object only')]
    actual=set(direct['pairs']['by_operation'])
    # Accept only explicitly mapped saved operation identifiers, never inferred
    # metric values or partial response files.
    aliases={
       'delete_evidence':['evidence_deletion','deletion'],
       'restore_evidence':['evidence_restoration','restoration'],
       'irrelevant_addition':['irrelevant_addition','irrelevant_invariance'],
       'decisive_change':['decisive_attribute'],
       'retain_refutation':['refutation_preservation'],
       'binding_swap':['object_binding_swap'],
       'equivalent_expression':['semantic_equivalence'],
       'other_object_only':['wrong_object_only']}
    mapped=[]
    for key,label in operations:
        options=[v for v in [key]+aliases[key] if v in actual]
        options=list(dict.fromkeys(options));assert len(options)==1,(key,actual)
        mapped.append((options[0],label))
    assert {k for k,_ in mapped}==actual
    cx=fig.add_axes([.36,.072,.43,.251]);yy=np.arange(8)[::-1]
    cx.set(xlim=(-.35,12.35),ylim=(-.5,7.5),yticks=[],xticks=[0,4,8,12])
    for yi,(key,label) in zip(yy,mapped):
        p=direct['pairs']['by_operation'][key];q=structured['pairs']['by_operation'][key]
        assert p['n']==q['n']==12
        cx.plot([p['success'],q['success']],[yi,yi],color='#C8D1D8',lw=1.2,zorder=1)
        cx.scatter(p['success'],yi+.10,s=15,marker='o',facecolor=GREY,edgecolor='white',linewidth=.45,zorder=3)
        cx.scatter(q['success'],yi-.10,s=17,marker='s',facecolor=BLUE,edgecolor='white',linewidth=.45,zorder=3)
        yf=fig.transFigure.inverted().transform(cx.transData.transform((0,yi)))[1]
        txt(fig,.035,yf,label,va='center',fontsize=7.6)
        txt(fig,.875,yf,str(p['success']),ha='right',va='center',fontsize=7.7)
        txt(fig,.96,yf,str(q['success']),ha='right',va='center',fontsize=7.7)
    cx.set(xlim=(-.35,12.35),ylim=(-.5,7.5),yticks=[],xticks=[0,4,8,12])
    cx.spines[['top','right','left']].set_visible(False)
    cx.tick_params(top=False,labeltop=False)
    txt(fig,.875,.349,'Direct',ha='right',fontsize=7.3)
    txt(fig,.96,.349,'Checklist',ha='right',fontsize=7.3,color=BLUE)
    txt(fig,.79,.029,'Correct pairs / 12',ha='right',fontsize=7.5)
    finish(fig,'figure3_controlled_diagnostics',[source],[ax,bx,cx])

if __name__=='__main__':
    requested=sys.argv[1:]
    if not requested or '1' in requested:figure1()
    if not requested or '2' in requested:figure2()
    if not requested or '3' in requested:figure3()
