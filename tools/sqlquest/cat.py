PAL = {'L':'#4a2f3a','O':'#f5a65b','D':'#d97f35','C':'#fff1dc','P':'#f7a1b5','K':'#2b2238','W':'#ffffff','N':'#e86a8a'}
SIT = [
"..L..........L..",
".LOL........LOL.",
".LPOLLLLLLLLOPL.",
"LOOOODODDODOOOOL",
"LOOOOOOOOOOOOOOL",
"LOOKWOOOOOOKWOOL",
"LOOKKOOOOOOKKOOL",
"LOPPOOCCNCCOPPOL",
".LOOOCCCCCCOOOL.",
"..LLOOOOOOOOLL..",
".LOOOOCCCCOOOOL.",
".LOODOCCCCCODOL.LL",
".LOOOOCCCCCOOOLLOL",
".LODOOCCCCCOODOOOL",
".LOOOOCCCCOOOOOLL.",
".LCCCLLLLLLLCCCL..",
"..LLL.......LLL...",
]
WALK = [
"...........L...L..",
"..........LOL.LOL.",
"..........LOPLLPOL",
"LL........LOOOOOOL",
"LOL.......LOOKOOKL",
".LOL.LLLLLLOOOCNCL",
"..LOLOODOODOLPCCCL",
"...LOOODOODOOLLLL.",
"...LOOOOOOOOOOOL..",
"...LOCCCCCCCCCOL..",
"...LOLLOL..LOLLOL.",
"...LL..LL..LL..LL.",
]
SLEEP = [
"..L..L.........",
".LOLLOL..LLLL..",
".LOOOOOLLOODOL.",
"LOOOOOOOOODOOOL",
"LOKKOKKOOOOODOL",
"LPOCNCOPOOOOOOL",
".LOCCCOOCCCCCOL",
".LLOOOOOOOOOOL.",
"..LLLLLLLLLLL..",
]
def rects(rows, x0=0, y0=0, eye_cls=None, leg_rows=None):
    out=[]
    for y,row in enumerate(rows):
        for x,ch in enumerate(row):
            if ch in PAL:
                cls=''
                if eye_cls and ch in 'KW': cls=f' class="{eye_cls}"'
                if leg_rows and y in leg_rows:
                    cls=' class="legA"' if x<9 else ' class="legB"'
                out.append(f'<rect x="{x0+x}" y="{y0+y}" width="1" height="1" fill="{PAL[ch]}"{cls}/>')
    return ''.join(out)
def sprite(cls, walk=False):
    rows = WALK if walk else SIT
    w=max(len(r) for r in rows); h=len(rows)
    body = rects(rows, leg_rows={10,11} if walk else None, eye_cls=None if walk else 'eye')
    return f'<svg class="{cls}" viewBox="0 0 {w} {h}" shape-rendering="crispEdges" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">{body}</svg>'
