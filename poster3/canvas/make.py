#!/usr/bin/env python3
"""Generate Main.dc.html for the TALAYAN 2.0 poster canvas.

Values are lifted straight from poster3/build.py's `grid` design so the
artboard matches the rendered PNG exactly. The brand faces are embedded as
data: URIs rather than pulled from Google Fonts, so PNG/PDF export keeps the
real typography instead of falling back.
"""
import base64, pathlib

HERE = pathlib.Path(__file__).parent
b64 = lambda f: base64.b64encode((HERE / f).read_bytes()).decode()

FACES = "\n".join(
    f"    @font-face{{font-family:'{fam}';font-weight:{wt};font-style:normal;"
    f"font-display:block;src:url(data:font/woff2;base64,{b64(f)}) format('woff2');}}"
    for fam, wt, f in [
        ("TalayanDisplay", "300 900", "fr900.woff2"),
        ("TalayanText", "300", "pop300.woff2"),
        ("TalayanText", "500", "pop500.woff2"),
        ("TalayanText", "600", "pop600.woff2"),
        ("TalayanText", "700", "pop700.woff2"),
    ])

DISPLAY = "'TalayanDisplay', Georgia, 'Times New Roman', serif"
TEXT = "'TalayanText', system-ui, -apple-system, sans-serif"

CREAM = "#F4ECDD"
GOLD = "#C9A24B"

ARTISTS = [("Siemy Di", "Drums"), ("Manmohan Dogra", "Tabla"),
           ("Etienne Bartholomew", "Sitar"), ("Varun Guru", "Guitar")]


def cast_rows():
    out = []
    for i, (name, inst) in enumerate(ARTISTS):
        top = f"border-top: 1px solid rgba(201, 162, 75, 0.26); " if i == 0 else ""
        out.append(
            f'      <div style="display: flex; align-items: baseline; gap: 16px; padding: 14px 0; '
            f'{top}border-bottom: 1px solid rgba(201, 162, 75, 0.26);">\n'
            f'        <div style="font-family: {DISPLAY}; font-variation-settings: \'opsz\' 144; '
            f'font-weight: 900; font-size: 44px; line-height: 1; flex: 1 1 auto;">{name}</div>\n'
            f'        <div style="font-size: 12.5px; font-weight: 600; letter-spacing: 0.28em; '
            f'text-indent: 0.28em; text-transform: uppercase; color: {{{{accent}}}}; '
            f'flex: 0 0 auto;">{inst}</div>\n'
            f'      </div>')
    return "\n".join(out)


HTML = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
  <style>
{FACES}
    body {{ margin: 0; background: #0B0E23; }}
    a {{ color: #E8963F; }}
    a:hover {{ color: #F3B368; }}
  </style>
</helmet>
<div style="position: relative; width: 1080px; height: 1350px; overflow: hidden;
  background: radial-gradient(120% 80% at 84% 4%, #1A2050 0%, #0B0E23 58%);
  font-family: {TEXT}; color: {CREAM};">

  <div style="position: absolute; inset: 0; display: flex; flex-direction: column;
    padding: 64px 66px 58px;">

    <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 24px;">
      <div style="font-size: 14px; font-weight: 600; letter-spacing: 0.34em; text-indent: 0.34em;
        text-transform: uppercase; color: {{{{accent}}}};">Talayan
        <span style="display: block; color: rgba(244, 236, 221, 0.62); margin-top: 6px;
          letter-spacing: 0.24em; text-indent: 0.24em;">A Study of Change</span>
      </div>
      <div style="font-size: 12px; font-weight: 600; letter-spacing: 0.26em; text-indent: 0.26em;
        text-transform: uppercase; color: #0B0E23; background: {{{{accent}}}}; padding: 8px 14px;
        border-radius: 999px; flex: 0 0 auto;">One night only</div>
    </div>

    <div style="height: 3px; background: {GOLD}; margin-top: 22px;"></div>

    <div style="font-family: {DISPLAY}; font-variation-settings: 'opsz' 144; font-weight: 900;
      font-size: 104px; line-height: 0.9; letter-spacing: 0.004em; margin-top: 26px;">TALAYAN
      <b style="font-weight: 900; color: {{{{accent}}}};">2.0</b></div>

    <div style="font-family: {DISPLAY}; font-variation-settings: 'opsz' 144; font-weight: 900;
      font-size: 206px; line-height: 0.84; letter-spacing: -0.02em; margin-top: 14px;
      color: {CREAM};">07.11.26</div>

    <div style="font-family: {DISPLAY}; font-variation-settings: 'opsz' 144; font-size: 31px;
      font-weight: 700; letter-spacing: 0.06em; margin-top: 10px;
      color: {{{{accent}}}};">Saturday 7 November 2026</div>

    <div style="display: flex; gap: 34px; margin-top: 18px;">
      <div style="flex: 1 1 0;">
        <div style="font-size: 11.5px; font-weight: 600; letter-spacing: 0.30em; text-indent: 0.30em;
          text-transform: uppercase; color: {GOLD};">Venue</div>
        <div style="font-family: {DISPLAY}; font-variation-settings: 'opsz' 144; font-weight: 900;
          font-size: 31px; line-height: 1.2; margin-top: 7px;">St John&rsquo;s Hoxton &middot; London</div>
      </div>
      <div style="flex: 1 1 0;">
        <div style="font-size: 11.5px; font-weight: 600; letter-spacing: 0.30em; text-indent: 0.30em;
          text-transform: uppercase; color: {GOLD};">Times</div>
        <div style="font-weight: 700; font-size: 30px; line-height: 1.2; margin-top: 8px;
          letter-spacing: -0.01em;">Doors 6:30pm
          <small style="display: block; font-weight: 500; font-size: 18px; letter-spacing: 0.01em;
            color: rgba(244, 236, 221, 0.8); margin-top: 5px;">Music from 7:00pm</small>
        </div>
      </div>
    </div>

    <div style="display: flex; flex-direction: column; margin-top: 24px;">
{cast_rows()}
    </div>

    <div style="margin-top: 20px; font-size: 17.5px; font-weight: 300; line-height: 1.62;
      color: rgba(244, 236, 221, 0.82); max-width: 54ch; text-wrap: pretty;">Four players. Three
      traditions. One pulse. A drum kit shaped by jazz and Africa, a tabla carrying centuries of
      tala, a sitar and a guitar that sings in Carnatic &mdash; meeting for one night and becoming
      a single conversation.</div>

    <div style="margin-top: auto; padding-top: 20px; border-top: 2px solid rgba(201, 162, 75, 0.42);
      display: flex; align-items: flex-end; gap: 22px;">
      <div style="flex: 1 1 auto;">
        <div style="font-family: {DISPLAY}; font-variation-settings: 'opsz' 144; font-weight: 900;
          font-size: 29px; line-height: 1.08;">Scan to book tickets</div>
        <div style="font-size: 14.5px; font-weight: 500; color: rgba(244, 236, 221, 0.7);
          margin-top: 6px;">Or book online at talayanfestival.com</div>
        <div style="font-size: 12.5px; font-weight: 600; letter-spacing: 0.2em; text-indent: 0.2em;
          text-transform: uppercase; color: {GOLD}; margin-top: 10px;">talayanfestival.com
          &nbsp;&middot;&nbsp; @talayanfestival</div>
      </div>
      <div style="width: 210px; height: 210px; flex: 0 0 auto; background: #ffffff;
        border-radius: 4px;"><img src="qr-tickets.png" alt="Scan to book tickets"
        style="display: block; width: 100%; height: 100%;"></div>
    </div>
  </div>

  <svg style="position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0.10;
    mix-blend-mode: multiply; pointer-events: none;" aria-hidden="true">
    <filter id="talayan-grain"><feTurbulence type="fractalNoise" baseFrequency="0.85"
      numOctaves="4"></feTurbulence></filter>
    <rect width="100%" height="100%" filter="url(#talayan-grain)"></rect>
  </svg>
</div>
</x-dc>
<script data-dc-script data-props='{{"accent":{{"editor":"color","default":"#E8963F","options":["#E8963F","#C9A24B","#4AA295","#C8447E"],"section":"Theme"}},"$preview":{{"width":1080,"height":1350}}}}'>
class Component extends DCLogic {{
  renderVals() {{
    return {{ accent: this.props.accent ?? '#E8963F' }};
  }}
}}
</script>
</body>
</html>
"""

(HERE / "Main.dc.html").write_text(HTML)
print("wrote Main.dc.html", (HERE / "Main.dc.html").stat().st_size, "bytes")
