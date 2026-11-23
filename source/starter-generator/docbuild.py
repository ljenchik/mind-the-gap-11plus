import re
from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

FONT = 'Arial'
def fixmin(s): return re.sub(r'(?<![\w\)])-(?=\d)', '−', str(s))

def _font(run, size=None, bold=None, italic=None, color=None):
    run.font.name = FONT; run._element.rPr.rFonts.set(qn('w:eastAsia'), FONT)
    if size: run.font.size = Pt(size)
    if bold is not None: run.bold = bold
    if italic is not None: run.italic = italic
    if color: run.font.color.rgb = RGBColor(*color)

def _field(par, instr, size=9):
    r = par.add_run(); _font(r, size)
    for t, txt in (('begin', None), (None, instr), ('end', None)):
        if t:
            e = OxmlElement('w:fldChar'); e.set(qn('w:fldCharType'), t); r._r.append(e)
        else:
            e = OxmlElement('w:instrText'); e.set(qn('xml:space'), 'preserve'); e.text = txt; r._r.append(e)

def new_doc(footer_text):
    d = Document()
    s = d.sections[0]; s.page_width = Cm(21); s.page_height = Cm(29.7)
    s.left_margin = s.right_margin = Cm(2); s.top_margin = Cm(1.8); s.bottom_margin = Cm(1.8)
    st = d.styles['Normal']; st.font.name = FONT; st.font.size = Pt(11); st.element.rPr.rFonts.set(qn('w:eastAsia'), FONT)
    st.paragraph_format.space_after = Pt(0); st.paragraph_format.space_before = Pt(0); st.paragraph_format.line_spacing = 1.15
    fp = s.footer.paragraphs[0]; fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = fp.add_run(footer_text + '  ·  Page '); _font(r, 9, color=(110, 110, 110)); _field(fp, 'PAGE'); r2 = fp.add_run(' of '); _font(r2, 9, color=(110, 110, 110)); _field(fp, 'NUMPAGES')
    return d

def para(d, text='', size=11, bold=False, italic=False, align=None, before=0, after=0, indent=None, hang=None, keep=False, color=None):
    p = d.add_paragraph(); pf = p.paragraph_format
    pf.space_before = Pt(before); pf.space_after = Pt(after); pf.keep_with_next = keep
    if indent is not None: pf.left_indent = Cm(indent)
    if hang is not None: pf.first_line_indent = Cm(-hang)
    if align == 'c': p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if text:
        r = p.add_run(text); _font(r, size, bold, italic, color)
    return p

def shade(cell, hexcol):
    tcPr = cell._tc.get_or_add_tcPr(); sh = OxmlElement('w:shd'); sh.set(qn('w:val'), 'clear'); sh.set(qn('w:color'), 'auto'); sh.set(qn('w:fill'), hexcol); tcPr.append(sh)

def set_cell_w(cell, w_cm):
    cell.width = Cm(w_cm)

def add_table(d, rows, widths_cm, header=True, size=10.5, center=True, grid=True, keep=True):
    t = d.add_table(rows=len(rows), cols=len(rows[0])); t.style = 'Table Grid' if grid else 'Normal Table'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER if center else WD_TABLE_ALIGNMENT.LEFT; t.autofit = False
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            c = t.cell(i, j); set_cell_w(c, widths_cm[j]); c.text = ''
            p = c.paragraphs[0]; p.paragraph_format.space_before = Pt(2); p.paragraph_format.space_after = Pt(2); p.paragraph_format.keep_with_next = keep
            lines = str(val).split('\n')
            for k, ln in enumerate(lines):
                if k: p = c.add_paragraph(); p.paragraph_format.space_after = Pt(1)
                r = p.add_run(fixmin(ln)); _font(r, size, bold=(header and i == 0))
            if header and i == 0: shade(c, 'E7E7E7')
    for j, w in enumerate(widths_cm): t.columns[j].width = Cm(w)
    return t

def answer_line(d, indent, width_cm=16.5):
    p = d.add_paragraph(); pf = p.paragraph_format; pf.left_indent = Cm(indent); pf.space_before = Pt(7); pf.space_after = Pt(5)
    pf.tab_stops.add_tab_stop(Cm(width_cm), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.LINES)
    r = p.add_run('Answer\t'); _font(r, 10, color=(90, 90, 90))
    return p

def build_paper(path, title, subtitle, q_list, info_lines, footer, time_text, total=None):
    d = new_doc(footer)
    total = total or sum(len(q['parts']) for q in q_list)
    para(d, title, 17, True, after=2)
    para(d, subtitle, 12, False, after=8, color=(80, 80, 80))
    add_table(d, [['Name: ', 'Date: ', f'Score:        / {total}']], [7.2, 4.6, 5.2], header=False, size=11, center=False)
    para(d, '', after=4)
    para(d, f'Total marks: {total}   ·   Suggested time: {time_text}', 10.5, True, after=3)
    for ln in info_lines: para(d, '•  ' + ln, 10, indent=0.5, hang=0.4, after=1)
    para(d, '', after=4)
    for n, q in enumerate(q_list, 1):
        marks = len(q['parts'])
        p = para(d, '', before=11, after=3, keep=True); p.paragraph_format.tab_stops.add_tab_stop(Cm(17), WD_TAB_ALIGNMENT.RIGHT)
        r = p.add_run(f'Question {n}'); _font(r, 12, True); r = p.add_run(f'\t[{marks} mark{"s" if marks>1 else ""}]'); _font(r, 9, color=(110, 110, 110))
        for line in q['intro']: para(d, fixmin(line), 11, after=3, keep=True)
        if q.get('table'):
            tb = q['table']; ws = [w / 567 for w in tb['widths']]
            add_table(d, tb['rows'], ws, header=True, size=10.5)
            para(d, '', after=3, keep=True)
        if q.get('fig'):
            path_, wd = q['fig']; fp = para(d, '', align='c', after=3, keep=True); fp.add_run().add_picture(path_, width=Inches(wd))
        single = len(q['parts']) == 1
        for k, pt in enumerate(q['parts']):
            lab = '' if single else f'({chr(97+k)})'
            ind = 0.0 if single else 0.9
            p = para(d, '', after=0, indent=ind, hang=(0 if single else 0.9), keep=True)
            if not single:
                p.paragraph_format.tab_stops.add_tab_stop(Cm(0.9)); r = p.add_run(lab + '\t'); _font(r, 11)
            r = p.add_run(fixmin(pt['text'])); _font(r, 11)
            answer_line(d, ind if single else ind).paragraph_format.keep_with_next = (k < len(q['parts']) - 1)
    d.save(path); return total

def build_answers(path, title, papers, footer):
    d = new_doc(footer)
    para(d, title, 17, True, after=4)
    para(d, 'Each lettered part is worth 1 mark. Accept equivalent forms (for example 0.5 or ½) unless the question asks for a particular form.', 10.5, after=6, color=(80, 80, 80))
    for i, (name, qs) in enumerate(papers):
        if i: d.add_page_break()
        total = sum(len(q['parts']) for q in qs)
        para(d, f'{name}   ({total} marks)', 14, True, before=4, after=4, keep=True)
        rows = [['Q', 'Answers', 'Marks']]
        for n, q in enumerate(qs, 1):
            single = len(q['parts']) == 1
            ans = '\n'.join(fixmin(p['ans']) if single else f'({chr(97+k)})  {fixmin(p["ans"])}' for k, p in enumerate(q['parts']))
            rows.append([str(n), ans, str(len(q['parts']))])
        add_table(d, rows, [1.2, 14.0, 1.8], size=10, keep=False, center=False)
    d.save(path)
