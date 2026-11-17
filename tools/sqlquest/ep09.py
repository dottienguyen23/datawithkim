"""Builds the Window Saga episodes (Ep 09a, 09b) of SQL Quest.

    python3 tools/sqlquest/ep09.py

Writes sql/ep09a-see-through-the-window/index.html and sql/ep09b-sum-it-up/index.html.
Shared head/nav/footer come from site_build-style helpers below so the pages match Episode 00.
Lab numbers come from my study sessions (SalesDB sample database, SQL Server / SSMS) on 16-17 Nov 2026.
"""
import os, re, json, html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
ASSET_V = '2'

def write(rel, text):
    p = os.path.join(ROOT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w').write(text); print('wrote', rel, len(text))

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '  <link href="https://fonts.googleapis.com/css2?family=Pixelify+Sans:wght@400;600;700&family=VT323&family=Nunito:wght@400;600;700&display=swap" rel="stylesheet">')

def head(title, desc):
    return ('<!DOCTYPE html>\n<html lang="en">\n<head>\n  <meta charset="UTF-8">\n'
            '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            f'  <title>{title}</title>\n  <meta name="description" content="{html.escape(desc)}">\n  {FONTS}\n'
            f'  <link rel="stylesheet" href="/assets/pixel-study.css?v={ASSET_V}">\n'
            f'  <script src="/assets/pixel-study.js?v={ASSET_V}" defer></script>\n</head>')

def nav(levels):
    return f'''  <nav>
    <div class="wide">
      <a class="logo" href="/">datawithkim<b>.dev</b></a>
      <div class="nav-right">
        <span class="xp" title="Levels you marked as cleared">★ <span id="xp">0/{levels}</span><span class="long"> cleared</span></span>
        <a href="/sql/">SQL Quest</a>
        <a class="hide-sm" href="/#notes">← notes</a>
      </div>
    </div>
    <div class="track" aria-hidden="true"></div>
  </nav>'''

FOOTER = '''  <footer>
    <div class="wide">
      <span>© <span id="yr">2026</span> Kim Nguyen · SQL Quest</span>
      <span>made with tea, rain &amp; a sleepy cat</span>
    </div>
  </footer>'''

# ---------------- tiny SQL highlighter ----------------
KW = ('SELECT FROM WHERE GROUP BY ORDER PARTITION OVER ROWS RANGE BETWEEN AND UNBOUNDED PRECEDING '
      'FOLLOWING CURRENT ROW AS WITH CASE WHEN THEN ELSE END IN DESC ASC DISTINCT INTERVAL HAVING').split()
FN = 'SUM AVG COUNT MIN MAX ROUND COALESCE CAST RANK ROW_NUMBER NULLIF FLOAT DECIMAL'.split()

def hl_code(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"('[^']*')", r'<span class="s">\1</span>', s)
    s = re.sub(r'\b(' + '|'.join(FN) + r')\b', r'<span class="fn">\1</span>', s)
    s = re.sub(r'\b(' + '|'.join(KW) + r')\b', r'<span class="kw">\1</span>', s)
    return s

def sql(code):
    out = []
    for line in code.strip('\n').split('\n'):
        if '--' in line:
            a, b = line.split('--', 1)
            out.append(hl_code(a) + '<span class="c">--' + html.escape(b, quote=False) + '</span>')
        else:
            out.append(hl_code(line))
    return '<pre class="sql">' + '\n'.join(out) + '</pre>'

def out(text, err=False):
    return f'<pre class="out{" err" if err else ""}">' + html.escape(text.strip('\n'), quote=False) + '</pre>'

def term(word, d):
    return f'<button class="term" data-def="{html.escape(d)}">{word}</button>'

def save(n, color, tip, terms):
    t = ''.join(term(w, d) for w, d in terms)
    return f'''      <div class="px save" style="--c: var(--{color})">
        <div>
          <div class="tag">💾 save point · the cat says</div>
          <p class="tip">{tip}</p>
          <div class="terms">{t}</div>
          <label class="clear"><input type="checkbox" data-ch="{n}"><span>cleared</span></label>
        </div>
      </div>'''

def table(headers, rows, cls='std wrap'):
    th = ''.join(f'<th>{h}</th>' for h in headers)
    tr = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<table class="{cls}"><tr>{th}</tr>{tr}</table>'

# ---------------- SVG helpers ----------------
C = dict(bg='#1e1a2e', bg2='#252038', panel='#2c2643', line='#4a4068', text='#f3ecdc', muted='#a99fbf',
         pink='#f2a7b8', mint='#9ed8c3', lav='#c9b6f2', peach='#f6c58f', sky='#8fb8f2')

def box(x, y, w, h, stroke, fill=None, sw=3):
    fill = fill or C['bg']
    return (f'<path d="M{x+4} {y} H{x+w-4} V{y+4} H{x+w} V{y+h-4} H{x+w-4} V{y+h} H{x+4} V{y+h-4} H{x} V{y+4} H{x+4} Z" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

def text(x, y, s, cls='n', anchor='start'):
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{html.escape(str(s))}</text>'

def svg_table(x, y, cols, widths, rows, stroke, row_h=30, fills=None):
    w = sum(widths)
    parts = [box(x, y, w, row_h * (len(rows) + 1) + 6, stroke)]
    cx = x
    for c, cw in zip(cols, widths):
        parts.append(text(cx + 10, y + 22, c, 'h')); cx += cw
    parts.append(f'<line x1="{x}" y1="{y+row_h+2}" x2="{x+w}" y2="{y+row_h+2}" stroke="{C["line"]}" stroke-width="2"/>')
    for i, r in enumerate(rows):
        ry = y + row_h * (i + 1) + 4
        if fills and fills[i]:
            parts.append(f'<rect x="{x+3}" y="{ry}" width="{w-6}" height="{row_h-2}" fill="{fills[i]}"/>')
        cx = x
        for v, cw in zip(r, widths):
            parts.append(text(cx + 10, ry + 21, v, 'n')); cx += cw
    return ''.join(parts)

def arrow_defs(id_, color):
    return (f'<defs><marker id="{id_}" viewBox="0 0 8 8" refX="6" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0 0 L8 4 L0 8 Z" fill="{color}"/></marker></defs>')

def figure(svg_inner, w, h, label, caption):
    return (f'<figure class="px fig reveal"><div class="fig-scroll"><svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'role="img" aria-label="{html.escape(label)}">{svg_inner}</svg></div><figcaption>{caption}</figcaption></figure>')

CAPS = 'rgba(158,216,195,.13)'; GLOV = 'rgba(246,197,143,.13)'

def fig_group_vs_window():
    p = [arrow_defs('a9-m', C['mint']), arrow_defs('a9-p', C['peach'])]
    p.append(text(20, 26, 'orders · 4 rows', 'h2'))
    p.append(svg_table(20, 40, ['id', 'product', 'sales'], [46, 104, 84],
                       [['1', 'Caps', '10'], ['2', 'Caps', '30'], ['3', 'Gloves', '5'], ['4', 'Gloves', '20']],
                       C['muted'], fills=[CAPS, CAPS, GLOV, GLOV]))
    # GROUP BY result
    p.append(text(330, 26, 'GROUP BY product', 'h2'))
    p.append(svg_table(330, 40, ['product', 'total'], [110, 74], [['Caps', '40'], ['Gloves', '25']], C['peach'], fills=[CAPS, GLOV]))
    p.append(text(330, 160, '4 rows → 2 · id is gone', 'hl'))
    # window result
    p.append(text(330, 206, 'window · PARTITION BY product', 'h2'))
    p.append(svg_table(330, 218, ['id', 'product', 'sales', 'total'], [46, 104, 84, 74],
                       [['1', 'Caps', '10', '40'], ['2', 'Caps', '30', '40'], ['3', 'Gloves', '5', '25'], ['4', 'Gloves', '20', '25']],
                       C['mint'], fills=[CAPS, CAPS, GLOV, GLOV]))
    p.append(text(330, 400, '4 rows → 4 · every detail kept', 'h'))
    p.append(f'<path d="M258 90 H296 V95 H318" fill="none" stroke="{C["peach"]}" stroke-width="3" stroke-dasharray="6 5" class="flow" marker-end="url(#a9-p)"/>')
    p.append(f'<path d="M258 130 H296 V290 H318" fill="none" stroke="{C["mint"]}" stroke-width="3" stroke-dasharray="6 5" class="flow" marker-end="url(#a9-m)"/>')
    return figure(''.join(p), 720, 412,
                  'Four order rows. GROUP BY product returns two rows and loses the id. A window SUM partitioned by product returns all four rows with the product total next to each one.',
                  'Same data, same SUM. GROUP BY squashes each group into one row (the id disappears). The window function writes the group total next to every row, so detail and total sit side by side.')

MONTHS = [('Jan', 20), ('Feb', 10), ('Mar', 30), ('Apr', 5), ('Jun', 70), ('Jul', 40)]

def fig_frames():
    p = []
    x0, y0, rh = 40, 50, 34
    p.append(text(40, 30, 'ORDER BY month · current row = Apr', 'h2'))
    p.append(box(x0, y0, 180, rh * 6 + 8, C['muted']))
    for i, (m, s) in enumerate(MONTHS):
        y = y0 + 4 + i * rh
        if m == 'Apr':
            p.append(f'<rect x="{x0+3}" y="{y}" width="174" height="{rh-2}" fill="rgba(242,167,184,.22)"/>')
        p.append(text(x0 + 14, y + 23, m, 'n')); p.append(text(x0 + 120, y + 23, s, 'n'))
    def bracket(x, i0, i1, color, label, res):
        ya, yb = y0 + 4 + i0 * rh + 3, y0 + 4 + (i1 + 1) * rh - 5
        p.append(f'<path d="M{x} {ya} H{x+12} V{yb} H{x}" fill="none" stroke="{color}" stroke-width="4"/>')
        p.append(f'<text x="{x+22}" y="{(ya+yb)//2 - 4}" class="h" text-anchor="start" fill="{color}" style="fill:{color}">{html.escape(res)}</text>')
        p.append(text(x + 22, (ya + yb) // 2 + 18, label, 's'))
    bracket(236, 0, 3, C['mint'], 'UNBOUNDED PRECEDING', '65 running')
    bracket(442, 1, 3, C['peach'], '2 PRECEDING', '45 rolling')
    bracket(582, 0, 5, C['lav'], 'whole window', '175 total')
    p.append(text(40, 286, 'rolling frame at Jul = 5 + 70 + 40 = 115', 's'))
    return figure(''.join(p), 720, 296,
                  'Six months of sales. For the current row April, the running frame covers January to April and sums to 65, the 2-preceding frame covers February to April and sums to 45, and the whole window sums to 175.',
                  'One current row, three frames. The frame decides which rows the function sees for <em>this</em> row, then it slides down with the current row.')

def fig_running_rolling():
    run = [20, 30, 60, 65, 135, 175]; roll = [20, 30, 60, 45, 105, 115]
    p = [text(30, 28, 'running total vs rolling total (2 preceding)', 'h2')]
    base, top = 260, 70; scale = (base - top) / 180
    p.append(f'<line x1="40" y1="{base}" x2="700" y2="{base}" stroke="{C["line"]}" stroke-width="2"/>')
    for i, ((m, _), a, b) in enumerate(zip(MONTHS, run, roll)):
        x = 70 + i * 105
        ha, hb = a * scale, b * scale
        p.append(f'<rect x="{x}" y="{base-ha:.0f}" width="34" height="{ha:.0f}" fill="{C["mint"]}"/>')
        p.append(f'<rect x="{x+40}" y="{base-hb:.0f}" width="34" height="{hb:.0f}" fill="{C["peach"]}"/>')
        p.append(text(x + 17, base - ha - 6, a, 'nsm', 'middle')); p.append(text(x + 57, base - hb - 6, b, 'nsm', 'middle'))
        p.append(text(x + 37, base + 22, m, 'n', 'middle'))
    p.append(f'<rect x="30" y="42" width="14" height="14" fill="{C["mint"]}"/>' + text(52, 55, 'running · keeps everything', 's'))
    p.append(f'<rect x="30" y="64" width="14" height="14" fill="{C["peach"]}"/>' + text(52, 77, 'rolling · drops the oldest', 's'))
    return figure(''.join(p), 720, 300,
                  'Bar chart for six months. The running total grows every month up to 175. The rolling total over three months goes 20, 30, 60, 45, 105, 115, rising and falling.',
                  'Running totals only grow: good for tracking progress against a target. Rolling totals go up and down: good for spotting the recent trend.')

# ---------------- Episode 09a ----------------
def ep09a():
    L = 5
    body = f'''
  <header class="wide hero">
    <div>
      <div class="chip">SQL Quest · episode 09a · world 2 · window saga 1/4</div>
      <h1>SEE THROUGH<br><span class="hl">THE WINDOW</span></h1>
      <p class="lead">Keep every row, and still see the big picture. Window functions add totals, ranks and comparisons next to your data instead of squashing it.</p>
      <div class="meta"><span>2026-11-16</span><span>·</span><span>15 min read</span><span>·</span><span class="t">#sql #window-functions #over #partition-by</span></div>
    </div>
    <div>
      <div class="px scene-box"><div class="scene-slot"></div></div>
      <p class="scene-cap">study cat on duty (asleep, as usual)</p>
    </div>
  </header>

  <article class="read">

    <section class="coldopen reveal">
      <p>Monday, 9:02. A message from sales: <em>"Can you send me every order, with its product's total sales next to it? And the grand total too, so I can see each order's share."</em></p>
      <p>Easy, I thought. <code>GROUP BY</code>. Five minutes later I had a red error, then a query that ran but gave the wrong numbers. This episode is how I got out of that hole.</p>
      <p class="big-idea">GROUP BY summarizes and changes the grain. A window function enriches and keeps it.</p>
    </section>

    <section class="chapter reveal" id="ch1" style="--c: var(--mint)">
      <div class="ch-head"><span class="ch-num">level 01</span><span class="ch-year">the problem</span></div>
      <h2>Why GROUP BY couldn't do it</h2>
      <p>The lab table is <code>Sales.Orders</code>: 10 orders, 4 products, 380 in total sales. Product 101 has four orders (10, 20, 90, 20), so its total is 140.</p>
      <div class="px lab">
        <span class="k">// lab · attempt 1: details + GROUP BY</span>
        {sql("""
SELECT OrderID, OrderDate, ProductID, SUM(Sales) AS TotalSales
FROM Sales.Orders
GROUP BY ProductID;""")}
        {out("""Msg 8120, Level 16, State 1, Line 4
Column 'Sales.Orders.OrderID' is invalid in the select list because it is not
contained in either an aggregate function or the GROUP BY clause.""", err=True)}
        <p class="note">After grouping, one product row stands for many orders. SQL can't pick which OrderID to show.</p>
      </div>
      <div class="px lab">
        <span class="k">// lab · attempt 2: put the details in GROUP BY too</span>
        {sql("""
SELECT OrderID, OrderDate, ProductID, SUM(Sales) AS TotalSales
FROM Sales.Orders
GROUP BY OrderID, OrderDate, ProductID;""")}
        {out("""OrderID  ProductID  TotalSales
1        101        10      <- product 101 should be 140
3        101        20      <- different "total" for the same product?""")}
        <p class="note">No error, wrong answer. OrderID is unique, so every order became its own group and SUM of one value is that value. The grain never changed.</p>
      </div>
      <p>That's the real limit: <code>GROUP BY</code> uses <strong>one grain for the whole query</strong>. My task needed two at once: rows at order level, total at product level.</p>
      {fig_group_vs_window()}
      <p class="hook">So how do you get a total without losing the rows? →</p>
{save(1, 'mint', 'No error ≠ correct result. Ask "what does one row mean?" before and after every GROUP BY.', [
    ('granularity', 'What one row represents in a table, also called the grain: one order, one product, one customer per month.'),
    ('GROUP BY', 'Collapses rows that share the same values into one row per group, changing the grain of the result.'),
    ('Msg 8120', 'SQL Server error: a column in SELECT is neither in GROUP BY nor inside an aggregate function.')])}
    </section>

    <section class="chapter reveal" id="ch2" style="--c: var(--sky)">
      <div class="ch-head"><span class="ch-num">level 02</span><span class="ch-year">the syntax</span></div>
      <h2>OVER: split, sort, crop</h2>
      <p>A window function is a normal function plus <code>OVER (...)</code>. The word OVER is what tells SQL: keep the rows. Inside the parentheses you describe the <strong>window</strong>, the set of rows the function looks at for the current row.</p>
      {sql("""
AVG(Sales)                        -- f(x): what to calculate
OVER (
    PARTITION BY ProductID        -- split the rows into windows
    ORDER BY OrderDate            -- sort inside each window
    ROWS UNBOUNDED PRECEDING      -- crop a frame around the current row
)""")}
      {table(['part', 'job', 'required?'], [
          ['PARTITION BY', 'split rows into groups; the calculation restarts in each one', 'optional (default: everything is one window)'],
          ['ORDER BY', 'sort rows inside each window', 'required for rank and value functions'],
          ['frame', 'which rows around the current row are used', 'optional, needs ORDER BY'],
      ])}
      <div class="px lab">
        <span class="k">// lab · the three-level report</span>
        {sql("""
SELECT OrderID, ProductID, OrderStatus, Sales,
       SUM(Sales) OVER ()                                    AS TotalSales,
       SUM(Sales) OVER (PARTITION BY ProductID)              AS SalesByProduct,
       SUM(Sales) OVER (PARTITION BY ProductID, OrderStatus) AS SalesByProductStatus
FROM Sales.Orders
ORDER BY OrderID;""")}
        {out("""OrderID ProductID OrderStatus Sales TotalSales SalesByProduct SalesByProductStatus
1       101       Delivered   10    380        140            30
2       102       Shipped     15    380        105            75
3       101       Delivered   20    380        140            30
4       105       Shipped     60    380        60             60
5       104       Delivered   25    380        75             75
6       104       Delivered   50    380        75             75
7       102       Delivered   30    380        105            30
8       101       Shipped     90    380        140            110
9       101       Shipped     20    380        140            110
10      102       Shipped     60    380        105            75""")}
        <p class="note">Checks I ran: 140 + 105 + 75 + 60 = 380 · 101: 30 + 110 = 140 · still 10 rows. Four granularities in one query, the thing GROUP BY can't do.</p>
      </div>
      <p>Two things that surprised me:</p>
      <p><strong>Same value ≠ same window.</strong> 30 shows up for 101-Delivered and 102-Delivered. Different windows, same total by coincidence. Always read the partition columns.</p>
      <p><strong>The output order is a side effect.</strong> Without the final <code>ORDER BY OrderID</code>, SQL Server returned rows grouped by product (product 102 came out as 10, 2, 7) because it sorted internally to compute the partitions. If order matters, say so with an outer <code>ORDER BY</code>.</p>
      <p class="hook">And what happens when I add ORDER BY inside OVER? The total turns into something else →</p>
{save(2, 'sky', 'OVER keeps the rows. PARTITION BY says "for each". Several windows can live in one SELECT.', [
    ('OVER', 'Turns a function into a window function and defines the window it runs on. OVER () means the whole result set.'),
    ('PARTITION BY', 'Splits rows into windows inside OVER. Unlike GROUP BY, rows are not collapsed.'),
    ('window', 'The set of rows a window function looks at for the current row.')])}
    </section>

    <section class="chapter reveal" id="ch3" style="--c: var(--lav)">
      <div class="ch-head"><span class="ch-num">level 03</span><span class="ch-year">frames</span></div>
      <h2>The frame slides with you</h2>
      <p>Add <code>ORDER BY</code> inside OVER and the window gets a direction. Now a <strong>frame</strong> can crop it: "from the first row to me", "the two rows before me", "me and the next one".</p>
      {fig_frames()}
      {table(['frame', 'Jan', 'Feb', 'Mar', 'Apr', 'Jun', 'Jul'], [
          ['UNBOUNDED PRECEDING AND CURRENT ROW', 20, 30, 60, 65, 135, 175],
          ['CURRENT ROW AND UNBOUNDED FOLLOWING', 175, 155, 145, 115, 110, 40],
          ['1 PRECEDING AND CURRENT ROW', 20, 30, 40, 35, 75, 110],
          ['CURRENT ROW AND 2 FOLLOWING', 60, 45, 105, 115, 110, 40],
          ['1 PRECEDING AND 1 FOLLOWING', 30, 60, 45, 105, 115, 110],
          ['UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING', 175, 175, 175, 175, 175, 175],
      ], 'std num wrap')}
      <p>Rule of thumb: an <code>UNBOUNDED</code> end is fixed, a <code>CURRENT ROW</code> or <code>N</code> end moves. Near the edges a frame just gets smaller, it never crosses into another partition.</p>
      <div class="px lab">
        <span class="k">// lab · the short form only works backwards</span>
        {sql("""
SUM(Sales) OVER (PARTITION BY OrderStatus ORDER BY OrderDate
                 ROWS UNBOUNDED FOLLOWING)""")}
        {out("Msg 102, Level 15, State 1, Line 7\nIncorrect syntax near 'FOLLOWING'.", err=True)}
        <p class="note">The short form <code>ROWS x</code> means <code>BETWEEN x AND CURRENT ROW</code>. With FOLLOWING the start would come after the end. Fix: write the full <code>BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING</code>. (The course slide used <code>ROWS 2 FOLLOWING</code> as its example: same error.)</p>
      </div>
      <div class="px cmp">
        <span class="k">// trap · the default frame</span>
        <p><code>SUM(Sales) OVER (ORDER BY x)</code> with no frame quietly uses <code>RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW</code>: a running total, not a total. And it's <code>RANGE</code>, not <code>ROWS</code>: rows with the same sort value are peers and get the same result.</p>
        {table(['Sales (sorted)', 'default RANGE', 'explicit ROWS'], [
            ['10', 10, 10], ['15', 25, 25], ['20', '<span class="bad">65</span>', 45], ['20', '<span class="bad">65</span>', 65],
            ['…', '…', '…'], ['60', '<span class="bad">290</span>', 230], ['60', '<span class="bad">290</span>', 290], ['90', 380, 380]], 'std num wrap')}
        <p>For a real row-by-row running total: write <code>ROWS</code> explicitly and add a tiebreaker to the sort.</p>
      </div>
      <p class="hook">Frames are flexible. But there are four rules you can't bend →</p>
{save(3, 'lav', 'ORDER BY inside OVER always means a frame. If you just wanted sorted output, use the outer ORDER BY.', [
    ('frame', 'The subset of the window used for the current row, set with ROWS or RANGE BETWEEN start AND end.'),
    ('UNBOUNDED PRECEDING', 'The first row of the partition.'),
    ('RANGE vs ROWS', 'ROWS counts physical rows. RANGE treats rows with the same ORDER BY value as one group of peers.')])}
    </section>

    <section class="chapter reveal" id="ch4" style="--c: var(--pink)">
      <div class="ch-head"><span class="ch-num">level 04</span><span class="ch-year">rules</span></div>
      <h2>Four rules, four error messages</h2>
      <p>All four rules come from one fact: window functions run <strong>late</strong>.</p>
      {sql("FROM → WHERE → GROUP BY → HAVING → window functions → SELECT → ORDER BY")}
      {table(['rule', 'what I hit', 'fix'], [
          ['1 · only in SELECT and ORDER BY', 'Msg 4108: windowed functions can only appear in the SELECT or ORDER BY clauses', 'compute in a subquery or CTE, filter outside'],
          ['2 · no nesting', 'Msg 4109: window function inside another window or aggregate', 'one layer per CTE step'],
          ['3 · WHERE runs first', 'no error: totals change (135 / 245 became 60 / 185)', 'filter in the outer query if you need full-data totals'],
          ['4 · with GROUP BY, use grouped columns or aggregates', 'Msg 8120 for ORDER BY Sales after GROUP BY CustomerID', 'RANK() OVER (ORDER BY SUM(Sales) DESC)'],
      ])}
      <div class="px lab">
        <span class="k">// lab · rule 1 workaround and rule 4 pattern</span>
        {sql("""
-- keep rows whose status total is above 100
SELECT *
FROM (
    SELECT OrderID, OrderStatus, Sales,
           SUM(Sales) OVER (PARTITION BY OrderStatus) AS TotalSales
    FROM Sales.Orders
) t                                -- the derived table needs an alias
WHERE TotalSales > 100;

-- aggregate first, then rank
SELECT CustomerID,
       SUM(Sales) AS TotalSales,
       RANK() OVER (ORDER BY SUM(Sales) DESC) AS RankCustomers
FROM Sales.Orders
GROUP BY CustomerID;""")}
        {out("""CustomerID  TotalSales  RankCustomers
3           125         1
1           110         2
4           90          3
2           55          4""")}
        <p class="note">Ranking by <code>CustomerID</code> instead also ran without errors, and put customer 4 first. Valid syntax, wrong business answer.</p>
      </div>
      <div class="px cmp">
        <span class="k">// compare · SQL Server (course) vs PostgreSQL (this series)</span>
        {table(['', 'SQL Server', 'PostgreSQL'], [
            ['window in WHERE', 'Msg 4108', 'ERROR: window functions are not allowed in WHERE'],
            ['RANGE with offsets', 'only UNBOUNDED / CURRENT ROW', "RANGE BETWEEN INTERVAL '7 days' PRECEDING …"],
            ['reuse a window', '—', 'named windows: WINDOW w AS (...)'],
            ['extra frame mode', '—', 'GROUPS (counts peer groups)'],
        ])}
      </div>
      <p class="hook">Last level: where all this shows up at work →</p>
{save(4, 'pink', 'Window functions run after WHERE and GROUP BY, so filter on them one level up.', [
    ('derived table', 'A subquery in FROM. SQL Server requires an alias for it, like ) t.'),
    ('CTE', 'WITH name AS (...): a named step you can query like a table. Easier to read than nested subqueries.'),
    ('execution order', 'The order SQL evaluates clauses: FROM, WHERE, GROUP BY, HAVING, window, SELECT, ORDER BY.')])}
    </section>

    <section class="chapter reveal" id="ch5" style="--c: var(--peach)">
      <div class="ch-head"><span class="ch-num">level 05</span><span class="ch-year">DE angle</span></div>
      <h2>In real data engineering</h2>
      <p><strong>Report tables with several levels.</strong> A sales export for Power BI often needs order line + product subtotal + business-line total + grand total on one row. Before window functions this meant one GROUP BY subquery per level and a join back for each. Now it's one pass over the table.</p>
      <p><strong>Grain discipline.</strong> The first question for any fact table (like a <code>fact_SalesLine</code>) is "what does one row mean?" Window results repeat on every row of the window, so never <code>SUM</code> a window-total column again: 4 rows × 140 = 560, not 140. That's the double-counting bug that makes dashboard totals look too big.</p>
      <p><strong>Decide where the filter goes.</strong> "Show product 101 with its share of all sales" needs the window over all rows and the filter outside. Put the filter in WHERE and the share is computed on the wrong denominator. Many "the % in my report doesn't match" tickets start here.</p>
{save(5, 'peach', 'Detail + subtotal + total in one row, one pass: that is the everyday job of a window function.', [
    ('fact table', 'A table of events with measures (sales, quantity) at a declared grain, at the center of a star schema.'),
    ('double counting', 'Summing a value that is already repeated on several rows, which inflates totals.')])}
    </section>

    <div class="px epilogue">
      <div class="tag">// episode cleared</div>
      <p>I started with a red error and ended with four levels of totals in one query. Next episode: what each aggregate function does inside a window, and the NULL traps hiding in them.</p>
      <p class="next">next → ep09b · sum it up</p>
    </div>

    <h2 class="section-title" id="glossary" style="--c: var(--lav)">Glossary</h2>
    <p class="section-sub">All the new words from this episode.</p>
    <dl class="gloss" id="gloss"></dl>

    <h2 class="section-title" id="quiz" style="--c: var(--peach)">Boss level: quick quiz</h2>
    <p class="section-sub">No pressure, the cat isn't grading.</p>
    <div class="px quiz" id="quizbox"></div>

    <section class="sources" id="sources">
      <h3>// sources</h3>
      <ol>
        <li><a href="https://www.postgresql.org/docs/current/tutorial-window.html" target="_blank" rel="noopener">PostgreSQL tutorial: Window Functions</a></li>
        <li><a href="https://www.postgresql.org/docs/current/sql-expressions.html#SYNTAX-WINDOW-FUNCTIONS" target="_blank" rel="noopener">PostgreSQL docs: window function calls (frames, RANGE, GROUPS)</a></li>
        <li><a href="https://learn.microsoft.com/en-us/sql/t-sql/queries/select-over-clause-transact-sql" target="_blank" rel="noopener">Microsoft Learn: SELECT - OVER clause (Transact-SQL)</a></li>
        <li>Lab data: the SalesDB sample database from the course I followed, run in SQL Server Management Studio.</li>
      </ol>
    </section>

    <div class="ep-nav"><span class="px">← ep08 · Queries inside queries (soon)</span><a class="px" href="/sql/ep09b-sum-it-up/">ep09b · Sum It Up →</a></div>
  </article>

'''
    quiz = [
        dict(q='You add OrderID to SELECT next to SUM(Sales) ... GROUP BY ProductID. What happens?',
             o=['SQL picks the first OrderID', 'Error: OrderID is not in GROUP BY or an aggregate', 'OrderID shows as NULL'], a=1,
             w='Every SELECT column must be grouped or aggregated. SQL Server reports Msg 8120.'),
        dict(q='Which query keeps all 10 order rows and shows each product total?',
             o=['SUM(Sales) ... GROUP BY ProductID', 'SUM(Sales) OVER (PARTITION BY ProductID)', 'SUM(Sales) OVER ()'], a=1,
             w='PARTITION BY ProductID makes one window per product and the rows are not collapsed. OVER () would give 380 on every row.'),
        dict(q='SUM(Sales) OVER (PARTITION BY ProductID ORDER BY OrderDate). For product 101 (10, 20, 90, 20) you get:',
             o=['140, 140, 140, 140', '10, 30, 120, 140', '10, 20, 90, 20'], a=1,
             w='ORDER BY switches on the default frame (start to current row), so it becomes a running total.'),
        dict(q='Why does ROWS 2 FOLLOWING fail?',
             o=['FOLLOWING needs RANGE', 'The short form means BETWEEN 2 FOLLOWING AND CURRENT ROW, so start comes after end', 'You can only look 1 row ahead'], a=1,
             w='The short form always ends at CURRENT ROW. Use BETWEEN CURRENT ROW AND 2 FOLLOWING.'),
        dict(q='How do you keep only rows where a window total is above 100?',
             o=['WHERE SUM(Sales) OVER (...) > 100', 'HAVING SUM(Sales) OVER (...) > 100', 'Compute it in a subquery or CTE, then filter outside'], a=2,
             w='Window functions run after WHERE and HAVING, so they can only be filtered one level up.'),
        dict(q='The default frame when you write ORDER BY without a frame is:',
             o=['ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW', 'RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW', 'the whole partition'], a=1,
             w='It is RANGE, so rows with the same sort value get the same result. Write ROWS explicitly for a row-by-row running total.'),
    ]
    page = (head('Ep 09a · See Through the Window · SQL Quest',
                 'SQL Quest episode 09a: window functions vs GROUP BY, the OVER clause, PARTITION BY, ORDER BY, frames and the four window rules, with real lab output and mistakes.')
            + '\n<body data-ep="ep09a">\n\n' + nav(L) + '\n' + body + FOOTER
            + '\n\n  <script>\n    window.QUIZ = ' + json.dumps(quiz, ensure_ascii=False, indent=6) + ';\n  </script>\n</body>\n</html>\n')
    write('sql/ep09a-see-through-the-window/index.html', page)

# ---------------- Episode 09b ----------------
def ep09b():
    L = 5
    body = f'''
  <header class="wide hero">
    <div>
      <div class="chip">SQL Quest · episode 09b · world 2 · window saga 2/4</div>
      <h1>SUM IT<br><span class="hl">UP</span></h1>
      <p class="lead">Totals that never forget the details. COUNT, SUM, AVG, MIN and MAX over windows: health checks, shares, comparisons, and running totals.</p>
      <div class="meta"><span>2026-11-17</span><span>·</span><span>15 min read</span><span>·</span><span class="t">#sql #window-functions #aggregates #data-quality</span></div>
    </div>
    <div>
      <div class="px scene-box"><div class="scene-slot"></div></div>
      <p class="scene-cap">the cat counted the rows. twice. (duplicate detected)</p>
    </div>
  </header>

  <article class="read">

    <section class="coldopen reveal">
      <p>A pipeline finished at 6 a.m. The dashboard says sales went up 30% overnight. Good news? Or did the same orders get loaded twice?</p>
      <p>Before anyone celebrates, two questions: <em>is anything missing?</em> and <em>is anything counted twice?</em> Both are answered by the same five functions you already know, plus <code>OVER</code>.</p>
      <p class="big-idea">Aggregate window functions answer "how much?" while every row stays where it is.</p>
    </section>

    <section class="chapter reveal" id="ch1" style="--c: var(--mint)">
      <div class="ch-head"><span class="ch-num">level 01</span><span class="ch-year">COUNT</span></div>
      <h2>The data health check</h2>
      {table(['expression', 'counts', 'Customers table (5 rows)'], [
          ['COUNT(*)', 'rows', '5'], ['COUNT(1)', 'rows (a constant is never NULL)', '5'],
          ['COUNT(Score)', 'non-NULL values', '4: Anna has no score'], ['COUNT(Country)', 'non-NULL values, duplicates included', '5, but only 2 distinct countries'],
      ])}
      <p><strong>Missing values:</strong> <code>COUNT(*) - COUNT(col)</code> is the number of NULLs. <strong>Duplicates:</strong> partition by the column that should be unique and count.</p>
      <div class="px lab">
        <span class="k">// lab · duplicates in the archive table</span>
        {sql("""
SELECT *
FROM (
    SELECT OrderID,
           COUNT(*) OVER (PARTITION BY OrderID) AS CheckPK
    FROM Sales.OrdersArchive
) t
WHERE CheckPK > 1;""")}
        {out("""OrderID  CheckPK
4        2
4        2
6        3
6        3
6        3""")}
        <p class="note">Same query on Sales.Orders: CheckPK = 1 everywhere (OrderID is a real primary key). The archive has no constraint: 5 rows returned, but only 3 are extra copies. Deleting all 5 would delete the orders. Keeping one per ID is the job of ROW_NUMBER in the next episode.</p>
      </div>
      <div class="px cmp">
        <span class="k">// gotcha · COUNT(DISTINCT) and windows</span>
        <p><code>COUNT(DISTINCT x) OVER (...)</code> is not allowed in SQL Server (Msg 10759) and not in PostgreSQL either. Use a GROUP BY subquery for distinct counts.</p>
      </div>
      <p class="hook">Rows are complete and unique. Now: whose share is biggest? →</p>
{save(1, 'mint', 'Completeness (NULLs) and uniqueness (duplicates): two COUNTs that decide whether any total can be trusted.', [
    ('COUNT(*) vs COUNT(col)', 'COUNT(*) counts rows. COUNT(col) counts only rows where col is not NULL.'),
    ('primary key', 'A column that uniquely identifies each row: no duplicates and no NULLs.'),
    ('data quality check', 'A test run after a load, for example no NULLs in key columns and no duplicate keys.')])}
    </section>

    <section class="chapter reveal" id="ch2" style="--c: var(--sky)">
      <div class="ch-head"><span class="ch-num">level 02</span><span class="ch-year">SUM</span></div>
      <h2>Part-to-whole, and the zero that lied</h2>
      <div class="px lab">
        <span class="k">// lab · each order's % of total sales</span>
        {sql("""
SELECT OrderID, Sales,
       Sales / SUM(Sales) OVER () * 100 AS PctOfTotal
FROM Sales.Orders;""")}
        {out("""OrderID  Sales  PctOfTotal
1        10     0
8        90     0      <- should be 23.68""", err=True)}
        <p class="note">Sales is INT. INT / INT is integer division: 10 / 380 = 0, and 0 × 100 = 0. Multiplying by 100 comes too late.</p>
        {sql("""
ROUND(CAST(Sales AS FLOAT) / SUM(Sales) OVER () * 100, 2) AS PctOfTotal
-- or: Sales * 100.0 / SUM(Sales) OVER ()""")}
        {out("""OrderID  Sales  PctOfTotal
1        10     2.63
4        60     15.79
8        90     23.68
...      ...    sum = 99.99 (rounding drift, not a bug)""")}
      </div>
      <p>The top 3 orders (8, 4, 10) make up 55% of sales; the smallest 3 make up 12%. That uneven split is what part-to-whole analysis is for, and it's the start of a Pareto / ABC analysis.</p>
      <p class="hook">Totals and shares done. But averages hide a NULL trap →</p>
{save(2, 'sky', 'Divide decimals, not integers: CAST or * 100.0 before the division.', [
    ('part-to-whole', 'Comparing a value with the total it belongs to, usually as a percentage.'),
    ('integer division', 'Dividing two integers drops the decimals: 10 / 380 = 0 in SQL Server.'),
    ('ROUND(x, 2)', 'Rounds x to 2 decimal places. Rounded percentages may add to 99.99 or 100.01.')])}
    </section>

    <section class="chapter reveal" id="ch3" style="--c: var(--lav)">
      <div class="ch-head"><span class="ch-num">level 03</span><span class="ch-year">AVG · MIN · MAX</span></div>
      <h2>What does a NULL mean?</h2>
      <p>Aggregates skip NULLs. Replacing NULL with 0 (<code>COALESCE(Sales, 0)</code>) is a business decision, and it moves some functions but not others:</p>
      {table(['Gloves sales 30, 70, ?', 'AVG', 'MIN', 'MAX'], [
          ['? = NULL (skipped)', '50', '30', '70'], ['? = 0 (COALESCE)', '<span class="bad">33</span>', '<span class="bad">0</span>', '70'],
      ], 'std num wrap')}
      <p>Same on customers: <code>AVG(Score)</code> = 2500 / 4 = 625, <code>AVG(COALESCE(Score, 0))</code> = 2500 / 5 = 500. A customer who was never scored and a customer who scored 0 are not the same thing. Decide once, write it down, use it everywhere in the report.</p>
      <div class="px lab">
        <span class="k">// lab · compare each order with its product</span>
        {sql("""
SELECT OrderID, ProductID, Sales,
       AVG(Sales) OVER (PARTITION BY ProductID)               AS AvgProduct,
       MAX(Sales) OVER (PARTITION BY ProductID)               AS MaxProduct,
       Sales - MIN(Sales) OVER ()                              AS DeviationFromMin
FROM Sales.Orders;""")}
        {out("""ProductID  orders  AvgProduct  Min  Max   range
101        4       35          10   90    80   <- biggest total, most uneven
102        3       35          15   60    45
104        2       37 (37.5!)  25   50    25
105        1       60          60   60    0    <- 1 order: average isn't reliable""")}
        <p class="note">104 shows 37 because AVG on an INT column returns INT in SQL Server. PostgreSQL returns 37.5. Orders above the overall average (38): 4, 6, 8, 10, found with a subquery and <code>WHERE Sales &gt; AvgSales</code>.</p>
      </div>
      <p class="hook">One more family of questions: how are we doing <em>over time</em>? →</p>
{save(3, 'lav', 'COALESCE before AVG changes the denominator. Before MIN, it can make a missing value the minimum.', [
    ('COALESCE', 'Returns the first non-NULL argument: COALESCE(Sales, 0) turns NULL into 0. Standard SQL, works in PostgreSQL too (ISNULL does not).'),
    ('compare to extremes', 'Distance from the best or worst value: MAX(x) OVER () - x or x - MIN(x) OVER ().'),
    ('outlier', 'A value far from the rest, like one 90 order when the average is 38.')])}
    </section>

    <section class="chapter reveal" id="ch4" style="--c: var(--pink)">
      <div class="ch-head"><span class="ch-num">level 04</span><span class="ch-year">over time</span></div>
      <h2>Running, rolling, moving</h2>
      {fig_running_rolling()}
      {table(['', 'frame', 'question'], [
          ['running total', 'ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW', 'how much so far? (YTD vs target)'],
          ['rolling total', 'ROWS BETWEEN 2 PRECEDING AND CURRENT ROW', 'how are the last 3 periods doing?'],
          ['moving average', 'AVG + ORDER BY date (+ frame)', 'what is the smoothed trend?'],
      ])}
      <div class="px lab">
        <span class="k">// lab · moving average per product over time</span>
        {sql("""
SELECT OrderID, ProductID, OrderDate, Sales,
       AVG(Sales) OVER (PARTITION BY ProductID)                      AS AvgByProduct,
       AVG(Sales) OVER (PARTITION BY ProductID ORDER BY OrderDate)   AS MovingAvg,
       AVG(Sales) OVER (PARTITION BY ProductID ORDER BY OrderDate
                        ROWS BETWEEN CURRENT ROW AND 1 FOLLOWING)    AS RollingAvg
FROM Sales.Orders;""")}
        {out("""ProductID  OrderDate   Sales  AvgByProduct  MovingAvg  RollingAvg
101        2025-01-01  10     35            10         15
101        2025-01-10  20     35            15         55
101        2025-02-18  90     35            40         55
101        2025-03-10  20     35            35         20   <- no next order: frame shrinks
102        2025-01-05  15     35            15         22   <- 22.5 truncated
102        2025-02-15  30     35            22         45
102        2025-03-15  60     35            35         60""")}
        <p class="note">My mistakes on the way: a trailing comma before FROM (Msg 156) and the same alias used twice. The last MovingAvg of each product equals AvgByProduct: a free correctness check.</p>
      </div>
      <div class="px cmp">
        <span class="k">// trap · "last 30 days" is not ROWS 29 PRECEDING</span>
        <p><code>ROWS</code> counts rows, not days. If May is missing, "2 preceding" from June reaches back to March.</p>
        {table(['', 'how to get a true time window'], [
            ['PostgreSQL', "SUM(sales) OVER (ORDER BY order_date RANGE BETWEEN INTERVAL '29 days' PRECEDING AND CURRENT ROW)"],
            ['SQL Server', 'aggregate to one row per day, fill gaps from a calendar table, then ROWS 29 PRECEDING'],
        ])}
      </div>
      <p class="hook">Last level: putting the checks into a pipeline →</p>
{save(4, 'pink', 'Running totals only grow; rolling totals rise and fall. Sort by a real date, make it unique, mind the gaps.', [
    ('running total', 'A cumulative sum from the first row to the current row; keeps all older data.'),
    ('rolling total', 'A sum over a fixed number of recent rows; the oldest row drops out as a new one comes in.'),
    ('moving average', 'An average over a sliding window, used to smooth spikes and show a trend.')])}
    </section>

    <section class="chapter reveal" id="ch5" style="--c: var(--peach)">
      <div class="ch-head"><span class="ch-num">level 05</span><span class="ch-year">DE angle</span></div>
      <h2>In real data engineering</h2>
      <p><strong>Post-load tests.</strong> Every load should prove two things: key columns are complete (<code>COUNT(*) - COUNT(key) = 0</code>) and keys are unique (<code>MAX(COUNT(*) OVER (PARTITION BY key)) = 1</code>, via a subquery). dbt ships these as <code>not_null</code> and <code>unique</code> tests. The duplicates in OrdersArchive are exactly what a staging table looks like when a source re-sends changed rows.</p>
      <p><strong>Reconciliation.</strong> <code>COUNT(*)</code> in the target vs the source file is the cheapest check there is. Log it on every run.</p>
      <p><strong>Dashboards.</strong> YTD lines are running totals per business line; trend lines are moving averages; "% of total" cards are part-to-whole. Computing them in SQL, at the right grain, keeps the Power BI model simple, and the NULL rule documented in one place.</p>
{save(5, 'peach', 'Before you publish a number: no NULL keys, no duplicate keys, row counts match.', [
    ('reconciliation', 'Comparing counts or totals between source and target to prove nothing was lost or duplicated.'),
    ('staging table', 'A landing table for raw loaded data, usually without constraints, cleaned before reporting.'),
    ('YTD', 'Year to date: a running total that restarts every January 1st, PARTITION BY YEAR(date).')])}
    </section>

    <div class="px epilogue">
      <div class="tag">// episode cleared</div>
      <p>Found the duplicates, fixed a division that always returned 0, and learned that a NULL needs a decision, not a default. Next: removing those duplicates and crowning the best, on the podium.</p>
      <p class="next">next → ep09c · stand on the podium (soon)</p>
    </div>

    <h2 class="section-title" id="glossary" style="--c: var(--lav)">Glossary</h2>
    <p class="section-sub">All the new words from this episode.</p>
    <dl class="gloss" id="gloss"></dl>

    <h2 class="section-title" id="quiz" style="--c: var(--peach)">Boss level: quick quiz</h2>
    <p class="section-sub">No pressure, the cat isn't grading.</p>
    <div class="px quiz" id="quizbox"></div>

    <section class="sources" id="sources">
      <h3>// sources</h3>
      <ol>
        <li><a href="https://www.postgresql.org/docs/current/functions-aggregate.html" target="_blank" rel="noopener">PostgreSQL docs: Aggregate Functions</a></li>
        <li><a href="https://www.postgresql.org/docs/current/functions-window.html" target="_blank" rel="noopener">PostgreSQL docs: Window Functions</a></li>
        <li><a href="https://learn.microsoft.com/en-us/sql/t-sql/queries/select-over-clause-transact-sql" target="_blank" rel="noopener">Microsoft Learn: SELECT - OVER clause (Transact-SQL)</a></li>
        <li>Lab data: the SalesDB sample database from the course I followed, run in SQL Server Management Studio.</li>
      </ol>
    </section>

    <div class="ep-nav"><a class="px" href="/sql/ep09a-see-through-the-window/">← ep09a · See Through the Window</a><span class="px">ep09c · Stand on the Podium (soon) →</span></div>
  </article>

'''
    quiz = [
        dict(q='Customers has 5 rows and one NULL Score. COUNT(Score) returns:',
             o=['5', '4', 'NULL'], a=1, w='COUNT(column) skips NULLs. COUNT(*) would return 5.'),
        dict(q='How do you find duplicate OrderIDs while keeping every column of the duplicate rows?',
             o=['COUNT(*) OVER (PARTITION BY OrderID) > 1, filtered in an outer query', 'COUNT(DISTINCT OrderID) OVER ()', 'SELECT DISTINCT *'], a=0,
             w='The window count shows the number of copies on every copy. GROUP BY ... HAVING only lists the keys.'),
        dict(q='Sales is INT. Sales / SUM(Sales) OVER () * 100 returns 0 for every row because:',
             o=['SUM is wrong without PARTITION BY', 'INT / INT is integer division, so 10 / 380 = 0', 'ROUND is missing'], a=1,
             w='Cast to FLOAT or DECIMAL, or multiply by 100.0 before dividing.'),
        dict(q='Gloves sales are 30, 70 and NULL. AVG(COALESCE(Sales, 0)) is:',
             o=['50', '33', '100'], a=1, w='The NULL becomes 0 and counts in the denominator: 100 / 3 = 33 (truncated on INT).'),
        dict(q='Which frame gives a 3-month rolling total?',
             o=['ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW', 'ROWS BETWEEN 2 PRECEDING AND CURRENT ROW', 'ROWS BETWEEN 3 PRECEDING AND CURRENT ROW'], a=1,
             w='2 preceding + the current row = 3 rows. 3 PRECEDING would cover 4.'),
        dict(q='ROWS BETWEEN 29 PRECEDING AND CURRENT ROW on order rows means:',
             o=['the last 30 days', 'the last 30 rows, whatever their dates', 'the last 30 days, but only in SQL Server'], a=1,
             w='ROWS counts rows. For a true time window use RANGE with an INTERVAL in PostgreSQL, or one row per day from a calendar table.'),
    ]
    page = (head('Ep 09b · Sum It Up · SQL Quest',
                 'SQL Quest episode 09b: COUNT, SUM, AVG, MIN and MAX as window functions: NULL and duplicate checks, part-to-whole, integer division, running and rolling totals, moving averages.')
            + '\n<body data-ep="ep09b">\n\n' + nav(L) + '\n' + body + FOOTER
            + '\n\n  <script>\n    window.QUIZ = ' + json.dumps(quiz, ensure_ascii=False, indent=6) + ';\n  </script>\n</body>\n</html>\n')
    write('sql/ep09b-sum-it-up/index.html', page)

if __name__ == '__main__':
    ep09a(); ep09b()
