# SQL Quest build tools

Generates the SQL Quest study series pages on datawithkim.dev.

```bash
python3 tools/sqlquest/scene.py       # builds the pixel study-room scene (scene.svg)
python3 tools/sqlquest/site_build.py  # writes assets/, sql/ and the redirect page
```

| File | What it is |
|---|---|
| `episodes.py` | The episode catalogue (worlds, titles, labs, status `live`/`soon`). The hub page is built from this. |
| `base.css`, `hub.css` | Shared pixel theme → `/assets/pixel-study.css` |
| `base.js` | Shared behaviour (cat, timer, glossary, quiz, progress) → `/assets/pixel-study.js` |
| `cat.py`, `scene.py` | Pixel-art cat sprites and the study-room scene |
| `figs.py` | The SVG diagrams used in Episode 00 |
| `template.html`, `chapters.html` | Source of Episode 00 |

New episode: copy `/sql/_template/`, fill it in, then set its status to `live` in `episodes.py` and rerun `site_build.py`.
