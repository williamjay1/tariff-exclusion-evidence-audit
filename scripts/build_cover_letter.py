from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()
sec = doc.sections[0]
sec.page_width = Inches(8.27)
sec.page_height = Inches(11.69)
sec.top_margin = sec.bottom_margin = Inches(1.0)
sec.left_margin = sec.right_margin = Inches(1.05)
st = doc.styles['Normal']
st.font.name = 'Times New Roman'
st.font.size = Pt(11)
st.paragraph_format.line_spacing = 1.15
st.paragraph_format.space_after = Pt(8)

paras = [
    ("23 October 2026", False),
    ("The Editors\nArtificial Intelligence and Law", False),
    ("Dear Editors,", False),
    ("I am submitting an original research article, \u201cAuditing evidence construction in legal AI evaluation: a source to input protocol for tariff exclusion decisions\u201d, for consideration as a research article.", False),
    ("The article addresses a validity problem that current legal AI evaluation leaves unrecorded. An evaluation presents a model with a text and scores its output against a label, while the step that turns a public decision into that text stays invisible. When a condition is recorded as unresolved, three different situations can lie behind the label: the input omitted a statement that the source contains, the public record lacks the attribute, or an interpretation was withheld. Each calls for a different remedy, and a benchmark that reports only the label cannot say which occurred. In the ruling analysed in Section 6.1, restoring a single sentence from the public source changes the reference state of a product from unresolved to supported, with no change to the legal question.", False),
    ("The contribution is a protocol and an inspectable resource rather than a model. For 208 condition units drawn from 67 US customs rulings, every record links the rule span, the governed product, the signed requirement, the object and attribute, the statement class, the admitted input version and the interpretation option, so that an evidence state can be recomputed. The audit attributes the 67 unresolved conditions inside 47 historically unresolved cases: source restoration settles 4, a declared interpretation option settles 17, and 47 persist under every operation recorded. Three fully specified interpretation packages support 10, 17 and 19 of 58 conjunctive cases, which makes the mapping dependence of a reported count explicit.", False),
    ("A qualified local model then shows that the audit dimensions are operationally separable. On 108 constructed inputs the two output contracts reach 98 and 104 correct whole case states, and they produce different failure profiles: ten unsupported affirmative decisions in one arm, three affirmations and one unsupported refutation in the other, with four necessary requests missing. A high whole case score therefore coexists with wrong condition states, which is the practical reason to score state, citation and request separately.", False),
    ("The work fits the journal\u2019s interest in evaluation and auditing methods for legal AI. It combines a technical instrument, a legal domain whose rules are dated and versioned, and an empirical audit reported with explicit denominators. It states its validation boundary, including the absence of independent expert adjudication, and identifies where expert judgement would enter. The manuscript is original, is not under consideration elsewhere, and has a single author with no competing interests. A reproducibility package containing the records, scripts, prompts and raw outputs accompanies the submission, and an artificial intelligence use statement is included in the manuscript.", False),
    ("I would be glad to provide any further information.", False),
    ("Yours sincerely,", False),
    ("Junjie Zhang\nShanghai International Studies University\njunjiezhang2024@shisu.edu.cn\nORCID 0009-0004-8821-4018", False),
]

for text, _ in paras:
    p = doc.add_paragraph()
    for i, line in enumerate(text.split('\n')):
        if i:
            p.add_run().add_break()
        p.add_run(line)

doc.core_properties.title = 'Cover letter'
doc.core_properties.author = 'Junjie Zhang'
doc.save(r'D:\MLWork\tariff_scope_20261007\revision_20261023\deliverables\Cover_Letter_Tariff_Evidence_Audit.docx')
print('saved')
