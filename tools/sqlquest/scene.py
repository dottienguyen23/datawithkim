import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
# Builds a pixel-art study-room SVG (grid units, crisp edges)
W,H=64,36
R=[]
def r(x,y,w,h,c,cls=None):
    R.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}"{f" class=\"{cls}\"" if cls else ""}/>')
# wall
r(0,0,W,H,'#2a2440')
r(0,26,W,10,'#3a2f4f')            # desk area wall shade
# window
r(6,3,26,18,'#5b4a6e'); r(7,4,24,16,'#141030')
for (x,y) in [(9,6),(14,9),(20,5),(26,8),(11,14),(23,13),(28,16),(17,15)]:
    r(x,y,1,1,'#fff6d5','tw')
r(25,5,4,4,'#fde6a8'); r(24,6,1,2,'#fde6a8'); r(29,6,1,2,'#fde6a8'); r(26,4,2,1,'#fde6a8'); r(26,9,2,1,'#fde6a8'); r(27,5,2,2,'#f4cf7c')  # moon
r(18,4,1,16,'#5b4a6e'); r(7,11,24,1,'#5b4a6e')   # window cross
r(5,21,28,2,'#7a6690')  # sill
# rain streaks
for (x,y) in [(10,5),(16,7),(22,10),(13,12),(29,11),(20,16),(8,17)]:
    r(x,y,1,2,'#6f7fbf','rain')
# shelf + books
r(40,8,18,1,'#8a6a52')
for i,(c,h) in enumerate([('#f2a7b8',5),('#9ed8c3',6),('#c9b6f2',4),('#f6c58f',6),('#8fb8f2',5)]):
    r(41+i*2,8-h,2,h,c)
r(53,5,3,3,'#9ed8c3'); r(54,4,1,1,'#7cc1a8')  # tiny plant on shelf
# desk
r(0,27,W,2,'#9a7658'); r(0,29,W,1,'#7a5a44'); r(4,30,2,6,'#7a5a44'); r(58,30,2,6,'#7a5a44')
# laptop
r(20,17,22,10,'#3d3a52'); r(21,18,20,8,'#0f1a14')
r(23,20,7,1,'#f2a7b8'); r(31,20,6,1,'#e6e1f0')      # SELECT ...
r(23,22,5,1,'#f2a7b8'); r(29,22,5,1,'#e6e1f0')
r(23,24,6,1,'#f2a7b8'); r(30,24,3,1,'#9ed8c3'); r(34,24,1,1,'#e6e1f0','cur')
r(17,27,28,1,'#57536e')  # keyboard base (sits on desk top)
r(17,26,28,1,'#6d6888')
# mug + steam
r(47,22,5,5,'#f6c58f'); r(52,23,2,1,'#f6c58f'); r(53,24,1,1,'#f6c58f'); r(52,25,2,1,'#f6c58f')
r(48,23,3,1,'#7a4a32')
r(48,19,1,2,'#cfc6e0','st1'); r(50,18,1,2,'#cfc6e0','st2')
# notebook (right side)
r(54,25,9,2,'#e9e1c8'); r(54,25,9,1,'#fff6e0'); r(58,24,1,3,'#f2a7b8')
# sleeping orange cat (left side of desk)
import sys; sys.path.insert(0, HERE)
from cat import rects, SLEEP
R.append(rects(SLEEP, 2, 18))
# zzz
for (x,y) in [(16,15),(17,15),(18,15),(17,16),(16,17),(17,17),(18,17)]: r(x,y,1,1,'#c9b6f2','z1')
for (x,y) in [(20,11),(21,11),(22,11),(21,12),(20,13),(21,13),(22,13)]: r(x,y,1,1,'#c9b6f2','z2')
# lamp glow
svg=f'''<svg class="scene" viewBox="0 0 {W} {H}" shape-rendering="crispEdges" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Pixel art: a cozy desk at night with a laptop showing SQL, a mug of tea, a sleeping cat and rain on the window">{"".join(R)}</svg>'''
open(os.path.join(HERE, 'scene.svg'), 'w').write(svg)
print(len(svg))
