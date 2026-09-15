#!/usr/bin/env python3
"""TALAYAN 2.0 — "QUARTET" poster, 1080x1350.

A different system again: a 2x2 block of colour panels, one artist per panel
with a captioned name bar, over a solid information block that carries the
date, venue, times and the ticket QR.
"""
import base64, pathlib, subprocess

HERE = pathlib.Path(__file__).parent
SHELL = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"
W, HT = 1080, 1350

b64 = lambda p: base64.b64encode((HERE / p).read_bytes()).decode()
FR, P3, P5, P6, P7 = (b64(f) for f in
                      ("fr900.woff2", "pop300.woff2", "pop500.woff2", "pop600.woff2", "pop700.woff2"))
QR = b64("qr_poster.png")

INK, CREAM, GOLD = "#12102A", "#F4ECDD", "#E8B65A"

PANEL_W, PANEL_H, CAP_H = 540, 470, 66
INFO_H = HT - PANEL_H * 2          # 410

# per artist: panel colour, plus how the cutout is framed inside its panel.
# `w` is the image width; `head` is roughly where the face sits across the
# cutout (0 = left edge, 1 = right edge) and `top` how far below the panel top
# the image begins — the bottom offset is derived so the face always clears the
# top edge instead of being guessed at.
ART = [
    dict(key="siemy",    n="Siemy Di",            i="Drums",  bg="#C8241F", bg2="#94120F",
         w=664, head=0.46, top=12),
    dict(key="manmohan", n="Manmohan Dogra",      i="Tabla",  bg="#E08A15", bg2="#A85D06",
         w=618, head=0.59, top=36),
    dict(key="etienne",  n="Etienne Bartholomew", i="Sitar",  bg="#12807F", bg2="#0A5654",
         w=650, head=0.32, top=14),
    dict(key="varun",    n="Varun Guru",          i="Guitar", bg="#4B2A8E", bg2="#2E1760",
         w=606, head=0.54, top=28),
]

# native cutout sizes, so the placement maths below is exact
import struct


def png_size(path):
    d = (HERE / path).read_bytes()
    return struct.unpack(">II", d[16:24])


for a in ART:
    iw, ih = png_size(a["key"] + "_solo.png")
    a["h"] = round(a["w"] * ih / iw)
    a["left"] = round(PANEL_W / 2 - a["head"] * a["w"])
    a["bottom"] = PANEL_H - a["top"] - a["h"]

CSS = f"""
@font-face{{font-family:'Fr';font-weight:100 900;src:url(data:font/woff2;base64,{FR}) format('woff2');}}
@font-face{{font-family:'Pop';font-weight:300;src:url(data:font/woff2;base64,{P3}) format('woff2');}}
@font-face{{font-family:'Pop';font-weight:500;src:url(data:font/woff2;base64,{P5}) format('woff2');}}
@font-face{{font-family:'Pop';font-weight:600;src:url(data:font/woff2;base64,{P6}) format('woff2');}}
@font-face{{font-family:'Pop';font-weight:700;src:url(data:font/woff2;base64,{P7}) format('woff2');}}
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{width:{W}px;height:{HT}px;}}
body{{position:relative;overflow:hidden;background:{INK};color:{CREAM};
  font-family:'Pop',system-ui,sans-serif;}}
.fr{{font-family:'Fr',Georgia,serif;font-variation-settings:'opsz' 144;}}

/* ---- 2x2 panel block ---- */
.wall{{position:absolute;left:0;top:0;width:{W}px;height:{PANEL_H*2}px;
  display:grid;grid-template-columns:repeat(2,minmax(0,1fr));grid-auto-rows:{PANEL_H}px;gap:0;}}
.pan{{position:relative;overflow:hidden;}}
.pan .figure{{position:absolute;}}
.pan .figure img{{display:block;width:100%;height:auto;}}
/* a soft floor under each figure so the cutout melts into the panel colour */
.pan .floor{{position:absolute;left:0;right:0;bottom:{CAP_H}px;height:150px;z-index:2;}}
.cap{{position:absolute;left:0;right:0;bottom:0;height:{CAP_H}px;z-index:3;background:{INK};
  display:flex;align-items:center;justify-content:space-between;gap:12px;padding:0 22px;}}
.cap .n{{font-weight:900;font-size:27px;line-height:1.04;letter-spacing:.004em;}}
.cap .i{{font-size:10.5px;font-weight:600;letter-spacing:.26em;text-indent:.26em;
  text-transform:uppercase;color:{GOLD};flex:0 0 auto;}}
/* hairline seams between the panels */
.seam-v{{position:absolute;left:{W//2 - 1}px;top:0;width:2px;height:{PANEL_H*2}px;
  background:{INK};z-index:4;}}
.seam-h{{position:absolute;left:0;top:{PANEL_H - 1}px;width:{W}px;height:2px;
  background:{INK};z-index:4;}}

/* ---- information block ---- */
.info{{position:absolute;left:0;bottom:0;width:{W}px;height:{INFO_H}px;background:{INK};
  display:flex;align-items:center;gap:30px;padding:0 58px;}}
.info::before{{content:'';position:absolute;left:58px;right:58px;top:0;height:3px;background:{GOLD};}}
.col{{flex:1 1 auto;min-width:0;}}
.mast{{font-weight:900;font-size:50px;line-height:1;letter-spacing:.01em;}}
.mast b{{font-weight:900;color:{GOLD};}}
.date{{font-weight:900;font-size:92px;line-height:.98;letter-spacing:-.005em;margin-top:6px;
  white-space:nowrap;}}
.where{{margin-top:12px;font-weight:900;font-size:27px;line-height:1.15;}}
.times{{margin-top:7px;font-size:21px;font-weight:700;letter-spacing:-.01em;}}
.times b{{font-weight:700;color:{GOLD};}}
.web{{margin-top:12px;font-size:11.5px;font-weight:600;letter-spacing:.22em;text-indent:.22em;
  text-transform:uppercase;color:rgba(244,236,221,.66);}}
.tix{{flex:0 0 auto;display:flex;flex-direction:column;align-items:center;gap:9px;}}
.qr{{width:202px;height:202px;background:#fff;border-radius:4px;position:relative;z-index:30;}}
.qr img{{display:block;width:100%;height:100%;}}
.tix .lbl{{font-size:10.5px;font-weight:600;letter-spacing:.24em;text-indent:.24em;
  text-transform:uppercase;color:{GOLD};}}

.grain{{position:absolute;inset:0;width:100%;height:100%;z-index:20;opacity:.10;
  mix-blend-mode:multiply;pointer-events:none;}}
"""


def panels():
    out = []
    for a in ART:
        out.append(f"""
  <div class="pan" style="background:linear-gradient(170deg,{a['bg']} 0%,{a['bg2']} 100%);">
    <div class="figure" style="width:{a['w']}px;left:{a['left']}px;bottom:{a['bottom']}px;">
      <img src="data:image/png;base64,{b64(a['key'] + '_solo.png')}" alt="">
    </div>
    <div class="floor" style="background:linear-gradient(180deg,transparent,{a['bg2']});"></div>
    <div class="cap"><div class="n fr">{a['n']}</div><div class="i">{a['i']}</div></div>
  </div>""")
    return "".join(out)


HTML = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><style>{CSS}</style></head>
<body>
<div class="wall">{panels()}</div>
<div class="seam-v"></div><div class="seam-h"></div>

<div class="info">
  <div class="col">
    <div class="mast fr">TALAYAN <b>2.0</b></div>
    <div class="date fr">SAT 7 NOV 2026</div>
    <div class="where fr">St John&rsquo;s Hoxton &middot; London</div>
    <div class="times">Doors <b>6:30pm</b> &middot; Music <b>7:00pm</b></div>
    <div class="web">talayanfestival.com &nbsp;&middot;&nbsp; @talayanfestival</div>
  </div>
  <div class="tix">
    <div class="qr"><img src="data:image/png;base64,{QR}" alt=""></div>
    <div class="lbl">Scan to book</div>
  </div>
</div>

<svg class="grain"><filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.85"
 numOctaves="4"/></filter><rect width="100%" height="100%" filter="url(#g)"/></svg>
</body></html>"""


if __name__ == "__main__":
    hp = HERE / "_quartet.html"
    hp.write_text(HTML)
    subprocess.run([SHELL, "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
                    "--force-device-scale-factor=1", f"--window-size={W},{HT}",
                    "--virtual-time-budget=14000",
                    f"--screenshot={HERE / 'photo-quartet.png'}", f"file://{hp}"],
                   capture_output=True)
    hp.unlink()
    print("rendered photo-quartet.png")
