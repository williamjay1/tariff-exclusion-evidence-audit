"""Verify native vector and raster export properties after figure rendering."""
from pathlib import Path
import json,hashlib,xml.etree.ElementTree as ET
from PIL import Image
import pymupdf
R=Path(__file__).resolve().parents[1];A=R/'artwork'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    reports=[]
    for stem in ['figure1_source_protocol','figure2_source_audit','figure3_controlled_diagnostics']:
        geom=json.loads((A/'qa'/f'{stem}.json').read_text(encoding='utf8'))
        assert geom['status']=='PASS'
        svg=A/'figures'/f'{stem}.svg';pdf=svg.with_suffix('.pdf');png=svg.with_suffix('.png')
        root=ET.fromstring(svg.read_bytes());ns={'s':'http://www.w3.org/2000/svg'}
        texts=root.findall('.//s:text',ns);images=root.findall('.//s:image',ns)
        assert texts and not images,'SVG must retain text and vector marks'
        with Image.open(png) as im:
            pix=im.size;dpi=im.info.get('dpi',(0,0))
            assert min(dpi)>=1199
            expected=[round(mm/25.4*1200) for mm in geom['fixed_canvas_mm']]
            assert all(abs(x-y)<=2 for x,y in zip(pix,expected)),(stem,pix,expected)
        with pymupdf.open(pdf) as doc:
            assert len(doc)==1
            page=doc[0];assert not page.get_images(),'No rasterized figure content in PDF'
            fonts=page.get_fonts(full=True);assert fonts
            font_report=[]
            for font in fonts:
                xref,ext,kind,base=font[:4]
                assert kind!='Type3' and 'Arial' in base,(stem,font)
                extracted=doc.extract_font(xref)
                assert extracted[3],(stem,'Unembedded font',base)
                font_report.append({'base':base,'type':kind,'embedded_bytes':len(extracted[3])})
            mm=[page.rect.width/72*25.4,page.rect.height/72*25.4]
            assert all(abs(x-y)<.05 for x,y in zip(mm,geom['fixed_canvas_mm']))
        reports.append({'figure':stem,'status':'PASS','svg_editable_text_nodes':len(texts),
         'svg_raster_images':len(images),'pdf_fonts':font_report,'physical_size_mm':geom['fixed_canvas_mm'],
         'png_pixels':pix,'png_dpi':dpi,'geometry_qa':geom['status'],
         'files':{p.name:sha(p) for p in [svg,pdf,png]}})
    report={'status':'PASS','figures':reports,'raster_method':'Direct 1200dpi export at final canvas dimensions; no upsampling',
      'vector_note':'Vector PDF/SVG have physical dimensions and scalable marks, not a fixed raster DPI.',
      'style_source':'SciencePlots 2.2.2 nature style plus explicit Arial, colourblind-safe palette and final physical dimensions',
      'visual_inspection_required':True}
    (A/'qa/export_integrity.json').write_text(json.dumps(report,indent=2),encoding='utf8')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
