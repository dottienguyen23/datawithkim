import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
import sys; sys.path.insert(0, HERE)
from cat import rects, SIT

def box(x, y, w, h, stroke, fill='#252038', sw=3):
    # notched pixel box
    n = 4
    return (f'<path d="M{x+n} {y} H{x+w-n} V{y+n} H{x+w} V{y+h-n} H{x+w-n} V{y+h} H{x+n} V{y+h-n} H{x} V{y+n} H{x+n} Z" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

def t(x, y, s, cls='', anchor='start', size=None):
    sz = f' font-size="{size}"' if size else ''
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}"{sz}>{s}</text>'

def mini_cat(x, y, scale):
    return f'<g transform="translate({x} {y}) scale({scale})" shape-rendering="crispEdges">{rects(SIT)}</g>'

ARROW = ('<defs><marker id="ah-{id}" viewBox="0 0 8 8" refX="6" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
         '<path d="M0 0 L8 4 L0 8 Z" fill="{c}"/></marker></defs>')

def arrow_defs(i, c):
    return ARROW.replace('{id}', i).replace('{c}', c)

# ---------------------------------------------------------------- A: old way vs Codd's way
def fig_ways():
    W, H = 720, 300
    o = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Two ways to ask which customers live in Milan. 1960s: a programmer walks a tree of records step by step. 1970 onward: you write one SQL sentence and the optimizer picks the route.">']
    o.append(arrow_defs('a', '#f6c58f') + arrow_defs('b', '#9ed8c3'))
    # left panel
    o.append(box(6, 6, 340, 288, '#4a4068', '#2c2643'))
    o.append(t(22, 36, '1960s · you walk the tree', 'h'))
    o.append(t(22, 58, 'question: who lives in Milan?', 'm'))
    # tree
    nodes = {'root': (176, 92, 'customers')}
    o.append(box(126, 76, 100, 30, '#a99fbf'))
    o.append(t(176, 97, 'customers', 'n', 'middle'))
    kids = [(60, 'C1 Rome'), (176, 'C2 Milan'), (292, 'C3 Turin')]
    for i, (x, lab) in enumerate(kids):
        o.append(f'<line x1="176" y1="106" x2="{x}" y2="146" stroke="#4a4068" stroke-width="3"/>')
        hl = '#9ed8c3' if 'Milan' in lab else '#a99fbf'
        o.append(box(x - 46, 146, 92, 28, hl))
        o.append(t(x, 166, lab, 'n', 'middle'))
        for j, dx in enumerate((-22, 22)):
            o.append(f'<line x1="{x}" y1="174" x2="{x+dx}" y2="206" stroke="#4a4068" stroke-width="3"/>')
            o.append(box(x + dx - 16, 206, 32, 20, '#4a4068'))
            o.append(t(x + dx, 221, 'ord', 's', 'middle'))
    # numbered steps
    steps = [(110, 118, '1'), (52, 192, '2'), (118, 192, '3'), (232, 118, '4'), (168, 192, '5'), (232, 192, '6')]
    for x, y, n in steps:
        o.append(f'<circle cx="{x}" cy="{y}" r="10" fill="#f6c58f"/>')
        o.append(t(x, y + 5, n, 'stepn', 'middle'))
    o.append(t(22, 256, '→ follow pointers,', 'm'))
    o.append(t(22, 278, '  one record at a time', 'm'))
    # right panel
    o.append(box(374, 6, 340, 288, '#4a4068', '#2c2643'))
    o.append(t(390, 36, '1970 → · you describe it', 'h'))
    o.append(box(390, 50, 308, 86, '#9ed8c3', '#1e1a2e'))
    o.append(t(404, 74, '<tspan class="kw">SELECT</tspan> name', 'code2'))
    o.append(t(404, 98, '<tspan class="kw">FROM</tspan> customers', 'code2'))
    o.append(t(404, 122, '<tspan class="kw">WHERE</tspan> city = <tspan class="str">\'Milan\'</tspan>', 'code2'))
    o.append('<line x1="544" y1="138" x2="544" y2="150" stroke="#9ed8c3" stroke-width="3" marker-end="url(#ah-b)"/>')
    o.append(box(410, 154, 268, 54, '#c9b6f2', '#1e1a2e'))
    o.append(mini_cat(420, 161, 2.3))
    o.append(t(470, 176, 'optimizer', 'h2'))
    o.append(t(470, 198, 'picks the route for you', 's2'))
    o.append('<line x1="544" y1="210" x2="544" y2="226" stroke="#9ed8c3" stroke-width="3" marker-end="url(#ah-b)"/>')
    o.append(box(484, 230, 120, 50, '#9ed8c3', '#1e1a2e'))
    o.append(t(544, 250, 'name', 's', 'middle'))
    o.append(f'<line x1="492" y1="256" x2="596" y2="256" stroke="#4a4068" stroke-width="2"/>')
    o.append(t(544, 274, 'Giulia', 'n', 'middle'))
    o.append('</svg>')
    return ''.join(o)

# ---------------------------------------------------------------- B: lab bar chart (HTML, single series)
def fig_lab():
    rows = [('Seq Scan · no index', 30.787, 'Read every row: ~1,000,000 checked, 96 kept. 30.8 ms.'),
            ('Bitmap Index Scan · with index', 0.211, 'Jumped straight to the 96 matching rows via the index. 0.2 ms.')]
    mx = 32
    o = ['<div class="bars" role="img" aria-label="Execution time of the same query on 1 million rows: 30.8 milliseconds without an index, 0.2 milliseconds with an index, about 145 times faster.">',
         '<div class="bars-title">Same query, 1 million rows · execution time (ms)</div>']
    for lab, v, tip in rows:
        w = max(v / mx * 100, 0.6)
        o.append(f'<div class="bar-row" tabindex="0" data-tip="{tip}"><span class="bar-lab">{lab}</span>'
                 f'<span class="bar-track"><span class="bar" style="--w:{w:.2f}%"></span></span>'
                 f'<span class="bar-val">{v:.1f} ms</span></div>')
    o.append('<div class="bars-axis"><span>0</span><span>10</span><span>20</span><span>30 ms</span></div>')
    o.append('<div class="bars-note">≈ 145× faster. Same <code>WHERE customer_id = 42</code>, I only added an index.</div></div>')
    return ''.join(o)

# ---------------------------------------------------------------- C: written vs executed order
def fig_order():
    W, H = 720, 260
    written = ['SELECT', 'FROM', 'WHERE', 'GROUP BY', 'HAVING', 'ORDER BY', 'LIMIT']
    runs = ['FROM', 'WHERE', 'GROUP BY', 'HAVING', 'SELECT', 'ORDER BY', 'LIMIT']
    x0, step, bw = 14, 100, 92
    o = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="You write SELECT first, but the database runs FROM, WHERE, GROUP BY and HAVING before SELECT. So WHERE runs before the SELECT alias exists.">']
    o.append(t(14, 22, 'you write ↓', 'h'))
    o.append(t(706, 255, 'the database runs ↑', 'h', 'end'))
    color = {'SELECT': '#f6c58f', 'WHERE': '#9ed8c3'}
    for i, k in enumerate(written):
        j = runs.index(k)
        c = color.get(k, '#4a4068')
        w = 4 if k in color else 2
        o.append(f'<line x1="{x0+i*step+bw/2}" y1="68" x2="{x0+j*step+bw/2}" y2="162" stroke="{c}" stroke-width="{w}" stroke-dasharray="{"" if k in color else "6 5"}"/>')
    for row, y, items in (('w', 34, written), ('r', 164, runs)):
        for i, k in enumerate(items):
            c = color.get(k, '#a99fbf')
            o.append(box(x0 + i * step, y, bw, 34, c, '#1e1a2e'))
            o.append(t(x0 + i * step + bw / 2, y + 23, k, 'kwbox', 'middle'))
            if row == 'r':
                o.append(t(x0 + i * step + bw / 2, y + 54, f'step {i+1}', 's', 'middle'))
    o.append('</svg>')
    return ''.join(o)

# ---------------------------------------------------------------- D: standards staircase
def fig_stairs():
    W, H = 720, 300
    eds = [('1986', 'SQL-86', 'first one', 'SELECT…'),
           ('1989', 'SQL-89', 'keys, checks', 'PK / FK'),
           ('1992', 'SQL-92', 'JOIN, CASE', 'everyday'),
           ('1999', 'SQL:1999', 'CTE, triggers', 'updated_at'),
           ('2003', 'SQL:2003', 'window funcs', 'RANK, LAG'),
           ('2016', 'SQL:2016', 'JSON', 'my JSONB')]
    o = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The SQL standard grows like a staircase: SQL-86 first standard, SQL-89 keys and checks, SQL-92 JOIN and CASE, SQL:1999 CTEs and triggers, SQL:2003 window functions, SQL:2016 JSON.">']
    sw, x0, base, h0, rise = 118, 4, 292, 120, 30
    for i, e in enumerate(eds):
        x = x0 + i * sw; y = base - h0 - i * rise
        hl = e[0] == '2003'
        col = '#f6c58f' if hl else '#c9b6f2'
        o.append(f'<rect x="{x}" y="{y}" width="{sw-6}" height="{base-y}" fill="{"#4a3a3a" if hl else "#3a3155"}"/>')
        o.append(f'<rect x="{x}" y="{y}" width="{sw-6}" height="5" fill="{col}"/>')
        o.append(t(x + 8, y + 32, e[0], 'yr'))
        o.append(t(x + 8, y + 52, e[1], 'stepl'))
        o.append(t(x + 8, y + 78, e[2], 'nsm'))
        o.append(t(x + 8, y + 98, '↳ ' + e[3], 's'))
    o.append(f'<line x1="{x0}" y1="{base}" x2="{x0+6*sw-6}" y2="{base}" stroke="#4a4068" stroke-width="3"/>')
    o.append('</svg>')
    return ''.join(o)

# ---------------------------------------------------------------- E: window functions arrival
def fig_window():
    W, H = 720, 210
    y0, yr0, yr1, x0, x1 = 120, 2002, 2019, 40, 680
    X = lambda yr: x0 + (yr - yr0) / (yr1 - yr0) * (x1 - x0)
    o = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Window functions entered the SQL standard in 2003. PostgreSQL added them in 2009 with version 8.4. MySQL added them in 2018 with version 8.0, nine years after PostgreSQL.">']
    o.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="#4a4068" stroke-width="4"/>')
    for yr in range(2003, 2019, 3):
        o.append(f'<rect x="{X(yr)-1}" y="{y0-5}" width="3" height="10" fill="#4a4068"/>')
        o.append(t(X(yr), y0 + 28, str(yr), 's', 'middle'))
    ev = [(2003, 'SQL:2003', 'in the standard', '#c9b6f2', 'start', 64),
          (2009, 'PostgreSQL 8.4', 'has them ✓', '#8fb8f2', 'start', 64),
          (2018, 'MySQL 8.0', 'finally ✓', '#f2a7b8', 'end', 64)]
    for yr, a, b, c, anchor, h in ev:
        x = X(yr)
        o.append(f'<rect x="{x-8}" y="{y0-8}" width="16" height="16" fill="{c}"/>')
        o.append(f'<line x1="{x}" y1="{y0-10}" x2="{x}" y2="{y0-30}" stroke="{c}" stroke-width="2"/>')
        dx = -8 if anchor == 'start' else 8
        o.append(t(x + dx, y0 - h, a, 'n', anchor))
        o.append(t(x + dx, y0 - h + 22, b, 's', anchor))
    a, b = X(2009), X(2018)
    o.append(f'<path d="M{a} {y0+44} V{y0+52} H{b} V{y0+44}" fill="none" stroke="#f6c58f" stroke-width="2"/>')
    o.append(t((a + b) / 2, y0 + 76, 'MySQL arrived 9 years after PostgreSQL', 'hl', 'middle'))
    o.append('</svg>')
    return ''.join(o)

# ---------------------------------------------------------------- F: everything speaks SQL
def fig_hub():
    import math
    W, H = 720, 330
    cx, cy = 360, 165
    names = ['Hive', 'Spark SQL', 'Presto', 'BigQuery', 'Snowflake', 'Databricks', 'Microsoft Fabric', 'dbt', 'AI text-to-SQL']
    o = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="SQL in the middle, connected to Hive, Spark SQL, Presto, BigQuery, Snowflake, Databricks, Microsoft Fabric, dbt and AI text-to-SQL: modern data platforms all speak SQL.">']
    pos = []
    for i, n in enumerate(names):
        ang = -math.pi / 2 + i * 2 * math.pi / len(names)
        x = cx + math.cos(ang) * 272; y = cy + math.sin(ang) * 130
        pos.append((x, y, n))
        o.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.0f}" y2="{y:.0f}" stroke="#4a4068" stroke-width="3" stroke-dasharray="6 6" class="flow"/>')
    for x, y, n in pos:
        w = 22 + len(n) * 10.5
        o.append(box(x - w / 2, y - 17, w, 34, '#a99fbf', '#2c2643'))
        o.append(t(x, y + 6, n, 'n', 'middle'))
    o.append(box(cx - 76, cy - 34, 152, 68, '#f6c58f', '#1e1a2e', 4))
    o.append(t(cx - 20, cy + 13, 'SQL', 'big'))
    o.append(mini_cat(cx - 66, cy - 17, 2))
    o.append('</svg>')
    return ''.join(o)

def fig_terms():
    W, H = 720, 250
    o = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Codd\'s math words and the words we use today: relation means table, tuple means row, attribute means column.">']
    # little table
    tx, ty, cw, rh = 30, 40, 110, 34
    cols = ['id', 'name', 'city']
    rows = [('1', 'Giulia', 'Milan'), ('2', 'Marco', 'Rome'), ('3', 'Tuyen', 'Pordenone')]
    o.append(f'<rect x="{tx}" y="{ty}" width="{cw*3}" height="{rh*4}" fill="#1e1a2e" stroke="#9ed8c3" stroke-width="3"/>')
    o.append(f'<rect x="{tx+cw}" y="{ty}" width="{cw}" height="{rh*4}" fill="rgba(246,197,143,.12)"/>')
    o.append(f'<rect x="{tx}" y="{ty+rh*2}" width="{cw*3}" height="{rh}" fill="rgba(242,167,184,.16)"/>')
    for i, c in enumerate(cols):
        o.append(t(tx + i*cw + 12, ty + 23, c, 'h'))
    o.append(f'<line x1="{tx}" y1="{ty+rh}" x2="{tx+cw*3}" y2="{ty+rh}" stroke="#4a4068" stroke-width="2"/>')
    for r, row in enumerate(rows):
        for i, v in enumerate(row):
            o.append(t(tx + i*cw + 12, ty + rh*(r+1) + 23, v, 'n'))
    o.append(t(tx, ty - 12, 'customers', 'h2'))
    # legend-style labels with leader lines
    lx = 420
    items = [(ty + 4, '#9ed8c3', 'relation', '= table', (tx + cw*3, ty + 10)),
             (ty + 74, '#f2a7b8', 'tuple', '= row', (tx + cw*3, ty + rh*2 + 17)),
             (ty + 144, '#f6c58f', 'attribute', '= column', (tx + cw*1.5, ty + rh*4))]
    for y, c, a, b, (px_, py_) in items:
        o.append(f'<path d="M{px_} {py_} H{lx-20} V{y+14} H{lx-6}" fill="none" stroke="{c}" stroke-width="2" stroke-dasharray="4 4"/>' if a != 'attribute' else
                 f'<path d="M{px_} {py_} V{H-12} H{lx-20} V{y+14} H{lx-6}" fill="none" stroke="{c}" stroke-width="2" stroke-dasharray="4 4"/>')
        o.append(f'<rect x="{lx}" y="{y}" width="14" height="14" fill="{c}"/>')
        o.append(t(lx + 24, y + 13, a, 'h'))
        o.append(t(lx + 160, y + 13, b, 'm'))
    o.append(t(lx, ty + 200, "math word → today's word", 's'))
    o.append('</svg>')
    return ''.join(o)

def fig(svg, cap, scroll=True):
    inner = f'<div class="fig-scroll">{svg}</div>' if scroll else svg
    return f'<figure class="px fig reveal">{inner}<figcaption>{cap}</figcaption></figure>'

FIGS = {
    'FIG_TERMS': fig(fig_terms(), 'Codd wrote in math, we speak in tables. Linking tables by matching values (like a customer id) instead of disk pointers is what makes data independence possible.'),
    'FIG_WAYS': fig(fig_ways(), 'Same question, two eras. Left: you write every step. Right: you write the result you want, and the optimizer (the cat) finds the route.'),
    'FIG_LAB': fig(fig_lab(), 'My Lab 1 result on PostgreSQL 16: the optimizer switched plans by itself once the index existed. Hover a bar for details.', scroll=False),
    'FIG_ORDER': fig(fig_order(), 'Read the lines: <span style="color:var(--mint)">WHERE</span> is step 2, <span style="color:var(--peach)">SELECT</span> is step 5. An alias made in SELECT doesn\'t exist yet when WHERE runs.'),
    'FIG_STAIRS': fig(fig_stairs(), 'The SQL standard grows one edition at a time. The ↳ lines show what each step added, or where I meet it in my labs. (Newer editions keep coming, like SQL:2023.)'),
    'FIG_WINDOW': fig(fig_window(), 'Window functions: from the standard (2003) to PostgreSQL (2009) to MySQL (2018).'),
    'FIG_HUB': fig(fig_hub(), 'Modern data platforms, old language. Learn SQL once, use it everywhere.'),
}
