from fractions import Fraction as F
from decimal import Decimal, getcontext
import random, math, os, itertools
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon

FIG = '/home/claude/work/figs'
os.makedirs(FIG, exist_ok=True)
VUL = {(1,2):'½',(1,3):'⅓',(2,3):'⅔',(1,4):'¼',(3,4):'¾',(1,5):'⅕',(2,5):'⅖',(3,5):'⅗',(4,5):'⅘',
       (1,6):'⅙',(5,6):'⅚',(1,8):'⅛',(3,8):'⅜',(5,8):'⅝',(7,8):'⅞'}
SUP = str.maketrans('0123456789','⁰¹²³⁴⁵⁶⁷⁸⁹')
SUB = str.maketrans('0123456789','₀₁₂₃₄₅₆₇₈₉')
def sup(n): return str(n).translate(SUP)

def frac(f):
    f = F(f); sign = '−' if f < 0 else ''; f = abs(f)
    w = f.numerator // f.denominator
    n = f.numerator - w * f.denominator; d = f.denominator
    if n == 0: return sign + str(w)
    if (n, d) in VUL: fs = VUL[(n, d)]; return sign + (str(w) + fs if w else fs)
    fs = str(n).translate(SUP) + '⁄' + str(d).translate(SUB)
    return sign + (f'{w} {fs}' if w else fs)

def dec(x, dp=None):
    """exact decimal string, trailing zeros stripped (or fixed dp)"""
    x = F(x)
    if dp is not None: return f'{float(x):.{dp}f}'
    s = format(Decimal(x.numerator) / Decimal(x.denominator), 'f') if x.denominator != 1 else str(x.numerator)
    if '.' in s: s = s.rstrip('0').rstrip('.')
    return s

def gbp(pence):
    pence = F(pence)
    if pence % 100 == 0: return f'£{int(pence)//100}'
    return f'£{float(pence)/100:.2f}'

def hm(m):
    m %= 1440
    return f'{m//60:02d}:{m%60:02d}'
def dur(m):
    h, mm = divmod(int(m), 60)
    if h and mm: return f'{h} hour{"s" if h>1 else ""} {mm} minutes'
    if h: return f'{h} hour{"s" if h>1 else ""}'
    return f'{mm} minutes'
def clock12(m):
    m %= 1440; h, mm = divmod(m, 60)
    ap = 'am' if h < 12 else 'pm'; h12 = h % 12 or 12
    return f'{h12}:{mm:02d}{ap}'

def Q(intro=None, parts=(), fig=None, table=None, note=None):
    """parts: list of (text, answer) ; intro: str or list"""
    if isinstance(intro, str): intro = [intro]
    return dict(intro=intro or [], parts=[dict(text=t, ans=str(a)) for t, a in parts], fig=fig, table=table, note=note)

def _style(ax):
    for s in ('top', 'right'): ax.spines[s].set_visible(False)

def bar_chart(path, labels, values, xlabel, ylabel, ymax=None, title=None, step=1):
    fig, ax = plt.subplots(figsize=(5.4, 3.0), dpi=160)
    ax.bar(range(len(labels)), values, color='#9a9a9a', edgecolor='black', width=0.7)
    ax.set_xticks(range(len(labels))); ax.set_xticklabels(labels)
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel)
    ymax = ymax or (max(values) + 1)
    ax.set_ylim(0, ymax); ax.set_yticks(range(0, ymax + 1, step)); ax.yaxis.grid(True, color='#cccccc', lw=0.6); ax.set_axisbelow(True)
    if title: ax.set_title(title, fontsize=10)
    _style(ax); fig.tight_layout(); fig.savefig(path); plt.close(fig); return path

def line_chart(path, xs, ys, xlabels, xlabel, ylabel, ymin, ymax, ystep):
    fig, ax = plt.subplots(figsize=(5.6, 3.2), dpi=160)
    ax.plot(xs, ys, color='black', marker='o', ms=3.5, lw=1.4)
    ax.set_xticks(xs); ax.set_xticklabels(xlabels, fontsize=8)
    ax.set_yticks(range(ymin, ymax + 1, ystep)); ax.set_ylim(ymin, ymax)
    ax.grid(True, color='#cccccc', lw=0.6); ax.set_axisbelow(True)
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel); _style(ax); fig.tight_layout(); fig.savefig(path); plt.close(fig); return path

def pie_chart(path, labels, values, angle_label=None):
    fig, ax = plt.subplots(figsize=(3.8, 3.4), dpi=160)
    cols = ['#ffffff', '#d9d9d9', '#b5b5b5', '#8c8c8c', '#666666']
    w, _ = ax.pie(values, labels=labels, startangle=90, counterclock=False, colors=cols[:len(values)],
                  wedgeprops=dict(edgecolor='black', lw=1), textprops=dict(fontsize=9))
    ax.set_aspect('equal'); fig.tight_layout(); fig.savefig(path); plt.close(fig); return path

def grid_fig(path, polys, lim=(-6, 6), labels=True):
    """polys: list of dict(pts=[(x,y)..], names=[..]) """
    lo, hi = lim
    fig, ax = plt.subplots(figsize=(4.2, 4.2), dpi=160)
    ax.set_xlim(lo - .3, hi + .3); ax.set_ylim(lo - .3, hi + .3); ax.set_aspect('equal')
    ax.set_xticks(range(lo, hi + 1)); ax.set_yticks(range(lo, hi + 1))
    ax.grid(True, color='#cccccc', lw=0.6); ax.set_axisbelow(True)
    ax.axhline(0, color='black', lw=1.2); ax.axvline(0, color='black', lw=1.2)
    ax.tick_params(labelsize=7)
    for p in polys:
        pts = p['pts']
        if len(pts) > 1:
            ax.add_patch(Polygon(pts, closed=True, fill=False, edgecolor='black', lw=1.6))
        for (x, y), nm in zip(pts, p.get('names', [''] * len(pts))):
            ax.plot(x, y, 'ko', ms=3)
            if nm: ax.annotate(nm, (x, y), textcoords='offset points', xytext=(5, 5), fontsize=10, weight='bold')
    ax.set_xlabel('x', fontsize=9); ax.set_ylabel('y', fontsize=9)
    fig.tight_layout(); fig.savefig(path); plt.close(fig); return path

def rect_pair(path, left, right):
    """left/right: dict(w=label,h=label) labels as strings; drawn schematically"""
    fig, ax = plt.subplots(figsize=(6.0, 2.2), dpi=160)
    ax.set_xlim(0, 12.5); ax.set_ylim(0, 4.2); ax.axis('off')
    for (x0, wd, ht, d) in ((0.5, 5.0, 2.6, left), (7.0, 4.6, 2.2, right)):
        ax.add_patch(Rectangle((x0, 0.8), wd, ht, fill=False, lw=1.8))
        ax.text(x0 + wd / 2, 0.8 + ht + 0.2, d['top'], ha='center', va='bottom', fontsize=11)
        ax.text(x0 + wd + 0.2, 0.8 + ht / 2, d['side'], ha='left', va='center', fontsize=11)
    ax.text(0.5, 0.25, 'Left rectangle', fontsize=9); ax.text(7.0, 0.25, 'Right rectangle', fontsize=9)
    fig.tight_layout(); fig.savefig(path); plt.close(fig); return path

def make_fig_path(tag): return os.path.join(FIG, tag + '.png')
