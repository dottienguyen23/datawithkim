import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
import os, re, sys, json, html
sys.path.insert(0, HERE)
from cat import sprite
from figs import FIGS
from episodes import WORLDS, all_eps

ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
ASSET_V = '2'

def write(rel, text):
    p = os.path.join(ROOT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w').write(text); print('wrote', rel, len(text))

def strip_cls(svg):
    return re.sub(r'^<svg class="[^"]*" ', '<svg ', svg)

# ---------------- assets ----------------
css = open(os.path.join(HERE, 'base.css')).read() + open(os.path.join(HERE, 'hub.css')).read()
css = '/* SQL Quest · shared pixel-study theme · datawithkim.dev */\n' + re.sub(r'^    ', '', css, flags=re.M)
write('assets/pixel-study.css', css)

scene = open(os.path.join(HERE, 'scene.svg')).read().replace('<svg class="scene" ', '<svg ')
js = open(os.path.join(HERE, 'base.js')).read()
js = js.replace("'{SPRITE_SIT}'", json.dumps(strip_cls(sprite('x'))))
js = js.replace("'{SPRITE_WALK}'", json.dumps(strip_cls(sprite('x', walk=True))))
js = js.replace("'{SCENE}'", json.dumps(scene))
write('assets/pixel-study.js', js)

# ---------------- shared page parts ----------------
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '  <link href="https://fonts.googleapis.com/css2?family=Pixelify+Sans:wght@400;600;700&family=VT323&family=Nunito:wght@400;600;700&display=swap" rel="stylesheet">')

def head(title, desc):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{html.escape(desc)}">
  {FONTS}
  <link rel="stylesheet" href="/assets/pixel-study.css?v={ASSET_V}">
  <script src="/assets/pixel-study.js?v={ASSET_V}" defer></script>
</head>'''

def nav(crumb, xp_total=None):
    xp = (f'<span class="xp" title="Levels you marked as cleared">★ <span id="xp">0/{xp_total}</span><span class="long"> cleared</span></span>'
          if xp_total else '')
    return f'''  <nav>
    <div class="wide">
      <a class="logo" href="/">datawithkim<b>.dev</b></a>
      <div class="nav-right">
        {xp}
        <a href="/sql/">{crumb}</a>
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

eps = all_eps()
order = [e for _, e in eps]
def neighbours(ep_id):
    i = [e[0] for e in order].index(ep_id)
    prev = order[i - 1] if i > 0 else None
    nxt = order[i + 1] if i + 1 < len(order) else None
    return prev, nxt

def ep_nav(ep_id):
    prev, nxt = neighbours(ep_id)
    def link(e, arrow_left):
        if not e: return '<a class="px" href="/sql/">← all episodes</a>' if arrow_left else '<a class="px" href="/sql/">all episodes →</a>'
        label = f'{e[0]} · {e[2]}'
        if e[5] != 'live':
            return f'<span class="px">{"← " if arrow_left else ""}{label} (soon){"" if arrow_left else " →"}</span>'
        return f'<a class="px" href="/sql/{e[1]}/">{"← " if arrow_left else ""}{label}{"" if arrow_left else " →"}</a>'
    return f'    <div class="ep-nav">{link(prev, True)}{link(nxt, False)}</div>'

# ---------------- Episode 0 ----------------
t = open(os.path.join(HERE, 'template.html')).read()
body = t[t.index('  <header class="wide hero">'):t.index('  <footer>')]
body = body.replace('{SCENE}', '<div class="scene-slot"></div>')
body = re.sub(r'\{CAT\}', '', body)
for k, v in FIGS.items():
    body = body.replace('{' + k + '}', v)
assert '{' not in re.sub(r'\{[^A-Z]', '', ''.join(re.findall(r'\{[A-Z_]+\}', body))), re.findall(r'\{[A-Z_]+\}', body)
body = body.replace('<div class="chip">study log · sql series · part 0</div>', '<div class="chip">SQL Quest · episode 00 · world 1</div>')
body = body.replace('<p class="next">next level → what really happens in the half-second after you press Enter</p>',
                    '<p class="next">next episode → ep01 · your first query</p>')
# quiz data from the inline script
qsrc = t[t.index('var Q = ['):t.index('];', t.index('var Q = ['))+2]
quiz_js = 'window.QUIZ = ' + qsrc[len('var Q = '):]
nlevels = len(re.findall(r'class="clear"><input type="checkbox"', body))
body = body.replace('  </article>', ep_nav('ep00') + '\n  </article>')
ep00 = (head('Ep 00 · A Short Story of SQL · SQL Quest', 'SQL Quest episode 0: how a 1970 research paper became the language every data platform still speaks. A cozy pixel study page with a cat.') +
        '\n<body data-ep="ep00">\n\n' + nav('SQL Quest', nlevels) + '\n\n' + body + FOOTER +
        f'\n\n  <script>\n    {quiz_js}\n  </script>\n</body>\n</html>\n')
write('sql/ep00-story-of-sql/index.html', ep00)

# old URL → redirect
write('notes/sql-story/index.html', '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Moved · A Short Story of SQL</title>
  <link rel="canonical" href="https://datawithkim.dev/sql/ep00-story-of-sql/">
  <meta http-equiv="refresh" content="0; url=/sql/ep00-story-of-sql/">
</head>
<body style="background:#1e1a2e;color:#f3ecdc;font-family:monospace;padding:40px">
  <p>This page moved to <a style="color:#9ed8c3" href="/sql/ep00-story-of-sql/">SQL Quest · Episode 00</a>.</p>
</body>
</html>
''')

# ---------------- Hub ----------------
def ep_card(w, e):
    ep_id, slug, title, desc, lab, status, src = e
    boss = ' boss' if ep_id == 'boss' else ''
    num = 'BOSS' if ep_id == 'boss' else ep_id.replace('ep', 'ep ')
    src_html = f'<span class="src">↳ {src}</span>' if src else ''
    st = 'play ▸' if status == 'live' else 'soon'
    inner = (f'<div class="num">{num}<span class="st">{st}</span></div><h3>{title}</h3><p>{desc}</p>'
             f'{src_html}<span class="lab">{lab}</span>')
    style = f'style="--c: {w["color"]}"'
    if status == 'live':
        return f'<a class="px ep live{boss}" data-ep="{ep_id}" href="/sql/{slug}/" {style}>{inner}</a>'
    return f'<div class="px ep soon{boss}" data-ep="{ep_id}" {style}>{inner}</div>'

worlds_html = ''
for w in WORLDS:
    cards = '\n        '.join(ep_card(w, e) for e in w['eps'])
    worlds_html += f'''
    <section class="world reveal" id="{w['id']}" style="--c: {w['color']}">
      <div class="world-head"><span class="wn">{w['tag']}</span><h2 class="section-title" style="margin:0">{w['name']}</h2></div>
      <p class="world-sub">{w['sub']}</p>
      <div class="eps">
        {cards}
      </div>
    </section>
'''

total_eps = len(order)
hub = head('SQL Quest · learn SQL from zero to data engineer · Data with Kim',
           f"Kim's SQL study series: {len(order)} episodes from your first SELECT to building a SQL data warehouse, with labs, diagrams, quizzes and a cat.") + f'''
<body data-dock="on">

{nav('SQL Quest')}

  <header class="wide hero">
    <div>
      <div class="chip">a study series by Kim · beginner → data engineer</div>
      <h1>SQL <span class="hl">Quest</span></h1>
      <p class="lead">I'm learning SQL in public, from my first <code>SELECT</code> to building a data warehouse. Every episode is one study session: a story, a hands-on lab, diagrams, a quiz, and a cat who sleeps through all of it.</p>
      <div class="meta"><span>{total_eps} episodes</span><span>·</span><span>3 worlds</span><span>·</span><span class="t">PostgreSQL</span></div>
      <div class="px progress-big" id="progress">
        <div class="cat-slot" data-cls="cat"></div>
        <div class="bar-outer"><div class="bar-inner" id="pbar"></div></div>
        <span class="lbl" id="plbl">0/{total_eps} episodes</span>
      </div>
    </div>
    <div>
      <div class="px scene-box"><div class="scene-slot"></div></div>
      <p class="scene-cap">the study room · open 24/7 · cat not included in the price</p>
    </div>
  </header>

  <div class="wide">
    <h2 class="section-title" style="--c: var(--mint)">How every episode works</h2>
    <p class="section-sub">Same shape every time, so you always know where you are.</p>
    <div class="anatomy">
      <div class="px" style="--c: var(--mint)"><b>📖 story</b>Each topic starts with the problem it solves, told like a game level, with a cliffhanger at the end.</div>
      <div class="px" style="--c: var(--sky)"><b>🧪 lab</b>Real commands on PostgreSQL with real output from my terminal, mistakes included.</div>
      <div class="px" style="--c: var(--lav)"><b>📊 diagrams</b>One picture per big idea: execution plans, joins, windows, before vs after.</div>
      <div class="px" style="--c: var(--peach)"><b>⚖️ compare</b>Side by side: RANK vs DENSE_RANK, Seq Scan vs Index Scan, PostgreSQL vs MySQL.</div>
      <div class="px" style="--c: var(--pink)"><b>🛠 DE angle</b>Where this shows up in real data pipelines and dashboards at work.</div>
      <div class="px" style="--c: var(--mint)"><b>💾 save points</b>Cat tips, hover-to-learn keywords, a glossary and a quiz to lock it in.</div>
    </div>
  </div>

  <div class="wide">
{worlds_html}
  </div>

  <div class="wide">
    <h2 class="section-title" style="--c: var(--sky)">My study loop</h2>
    <p class="section-sub">How one study session becomes one episode.</p>
    <div class="journey">
      <div class="px"><b>1 · study</b>Lesson + lab with my AI study buddy. Every question and error gets written down.</div>
      <div class="px"><b>2 · report</b>"taki taki" → a bilingual task report in my Notion learning hub.</div>
      <div class="px"><b>3 · build</b>The report becomes an episode page: story, lab, diagrams, quiz.</div>
      <div class="px"><b>4 · ship</b><code>git push</code> → live on datawithkim.dev via GitHub Pages.</div>
      <div class="px"><b>5 · share</b>A short post linking the episode, so others can learn along.</div>
    </div>

    <h2 class="section-title" style="--c: var(--peach)">Watch-along</h2>
    <p class="section-sub">Prefer video? This free course covers most of the same ground and pairs well with the labs here.</p>
    <a class="px lab" style="display:block; --b: var(--peach)" href="https://youtu.be/SSKVgrwhzus" target="_blank" rel="noopener">
      <span class="k" style="color:var(--peach)">// video · Data with Baraa</span>
      <p><strong>SQL Full Course for Beginners (30 Hours): From Zero to Hero</strong>. Basics, joins, functions, window functions, CTEs, procedures, performance, EDA and a data warehouse project. Different database engine than mine in places, so expect small syntax differences.</p>
    </a>
  </div>

{FOOTER}

  <script>
    document.addEventListener('DOMContentLoaded', function () {{
      var done = 0, cards = document.querySelectorAll('.ep[data-ep]');
      cards.forEach(function (c) {{
        if (window.SQLQuest && SQLQuest.isDone(c.dataset.ep)) {{
          done++; c.classList.add('done'); var st = c.querySelector('.st'); if (st) st.textContent = 'cleared ✓';
        }}
      }});
      document.getElementById('pbar').style.width = (done / {total_eps} * 100) + '%';
      document.getElementById('plbl').textContent = done + '/{total_eps} episodes';
    }});
  </script>
</body>
</html>
'''
write('sql/index.html', hub)

# ---------------- Episode template ----------------
tpl = head('Ep XX · TITLE · SQL Quest', 'SQL Quest episode XX: ONE-LINE SUMMARY.') + '''
<!--
  HOW TO MAKE A NEW EPISODE
  1. Copy this folder to /sql/epXX-short-name/ and set data-ep="epXX" on <body>.
  2. Fill each level: story → (lab) → (diagram) → hook → save point.
  3. Every save point needs: a one-line tip, 2-4 <button class="term" data-def="..."> keywords,
     and a checkbox <input type="checkbox" data-ch="N"> with a unique N.
     The cat, glossary, progress bar, timer and quiz are added automatically by /assets/pixel-study.js.
  4. Write the quiz in window.QUIZ at the bottom (a = index of the right option, w = explanation).
  5. In /tmp/gen/episodes.py (or the hub HTML) set the episode status to "live".
-->
<body data-ep="epXX">

''' + nav('SQL Quest', 3) + '''

  <header class="wide hero">
    <div>
      <div class="chip">SQL Quest · episode XX · world N</div>
      <h1>EPISODE<br><span class="hl">TITLE</span></h1>
      <p class="lead">The hook: what problem does this topic solve? Why should anyone care?</p>
      <div class="meta"><span>YYYY-MM-DD</span><span>·</span><span>N min read</span><span>·</span><span class="t">#sql #topic</span></div>
    </div>
    <div>
      <div class="px scene-box"><div class="scene-slot"></div></div>
      <p class="scene-cap">study cat on duty (asleep)</p>
    </div>
  </header>

  <article class="read">

    <section class="coldopen reveal">
      <p>Open with a real situation: "Your boss asks…", "The pipeline failed at 3 a.m. because…"</p>
      <p class="big-idea">One sentence that sums up the whole episode.</p>
    </section>

    <section class="chapter reveal" id="ch1" style="--c: var(--mint)">
      <div class="ch-head"><span class="ch-num">level 01</span><span class="ch-year">concept</span></div>
      <h2>Level title</h2>
      <p>Explain the idea in simple words, with one everyday comparison.</p>
      <div class="px lab">
        <span class="k">// lab</span>
        <p>What I ran and what I saw. Put real output in a &lt;pre&gt; or as a diagram.</p>
      </div>
      <p class="hook">Cliffhanger into the next level →</p>
      <div class="px save" style="--c: var(--mint)">
        <div>
          <div class="tag">💾 save point · the cat says</div>
          <p class="tip">One-line takeaway.</p>
          <div class="terms"><button class="term" data-def="Simple definition.">keyword</button></div>
          <label class="clear"><input type="checkbox" data-ch="1"><span>cleared</span></label>
        </div>
      </div>
    </section>

    <section class="chapter reveal" id="ch2" style="--c: var(--sky)">
      <div class="ch-head"><span class="ch-num">level 02</span><span class="ch-year">compare</span></div>
      <h2>A vs B</h2>
      <p>Side-by-side comparison of two options, and when to use each.</p>
      <div class="px save" style="--c: var(--sky)">
        <div>
          <div class="tag">💾 save point · the cat says</div>
          <p class="tip">One-line takeaway.</p>
          <div class="terms"><button class="term" data-def="Simple definition.">keyword</button></div>
          <label class="clear"><input type="checkbox" data-ch="2"><span>cleared</span></label>
        </div>
      </div>
    </section>

    <section class="chapter reveal" id="ch3" style="--c: var(--peach)">
      <div class="ch-head"><span class="ch-num">level 03</span><span class="ch-year">DE angle</span></div>
      <h2>In real data engineering</h2>
      <p>Where this shows up in pipelines, warehouses and dashboards.</p>
      <div class="px save" style="--c: var(--peach)">
        <div>
          <div class="tag">💾 save point · the cat says</div>
          <p class="tip">One-line takeaway.</p>
          <div class="terms"><button class="term" data-def="Simple definition.">keyword</button></div>
          <label class="clear"><input type="checkbox" data-ch="3"><span>cleared</span></label>
        </div>
      </div>
    </section>

    <h2 class="section-title" id="glossary" style="--c: var(--lav)">Glossary</h2>
    <p class="section-sub">All the new words from this episode.</p>
    <dl class="gloss" id="gloss"></dl>

    <h2 class="section-title" id="quiz" style="--c: var(--peach)">Boss level: quick quiz</h2>
    <p class="section-sub">No pressure, the cat isn't grading.</p>
    <div class="px quiz" id="quizbox"></div>

    <section class="sources" id="sources">
      <h3>// sources</h3>
      <ol>
        <li><a href="https://www.postgresql.org/docs/current/" target="_blank" rel="noopener">PostgreSQL documentation</a></li>
      </ol>
    </section>

    <div class="ep-nav"><a class="px" href="/sql/">← all episodes</a><span></span></div>
  </article>

''' + FOOTER + '''

  <script>
    window.QUIZ = [
      { q: 'Question?', o: ['Option A', 'Option B (right)', 'Option C'], a: 1, w: 'Why B is right.' }
    ];
  </script>
</body>
</html>
'''
write('sql/_template/index.html', tpl)
