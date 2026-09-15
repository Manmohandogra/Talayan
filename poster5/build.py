#!/usr/bin/env python3
"""TALAYAN 2.0 — "ARCH" poster, 1080x1350.

Replaces the square panel grid with one tall arched window — a nod to both the
church the concert is in and the Mughal arch on the website — with the four
players standing inside it and their names set on the picture rather than in
separate bars. The information block below is unchanged.
"""
import base64, pathlib, struct, subprocess

HERE = pathlib.Path(__file__).parent
SHELL = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"
W, HT = 1080, 1350

b64 = lambda p: base64.b64encode((HERE / p).read_bytes()).decode()
FR, P3, P5, P6, P7 = (b64(f) for f in
                      ("fr900.woff2", "pop300.woff2", "pop500.woff2", "pop600.woff2", "pop700.woff2"))
QR = b64("qr_poster.png")

INK, CREAM, GOLD = "#12102A", "#F4ECDD", "#E8B65A"

INFO_H = 410                       # unchanged from the quartet poster
ARCH_X, ARCH_W = 50, 980           # the window sits 50px in from each edge
ARCH_TOP, ARCH_BOT = 34, 922       # vertical extent of the window
ARCH_H = ARCH_BOT - ARCH_TOP       # 888
RADIUS = ARCH_W // 2               # semicircular head to the arch
NAME_BAND = 128                    # height of the name row inside the window


def png_size(path):
    return struct.unpack(">II", (HERE / path).read_bytes()[16:24])


# Siemy and Manmohan centre and larger; Etienne and Varun outside and equal.
# Figures are sized by HEIGHT (`fh`), not width: the four cutouts are framed
# differently, so matching widths made whoever had the tallest crop tower over
# the rest. `head` is where the face sits across the cutout, `cx` where that
# face should land in the window. All four stand on the window's floor.
ART = [
    dict(key="etienne",  n="Etienne<br>Bartholomew", i="Sitar",
         fh=596, head=0.30, cx=116, z=2),
    dict(key="siemy",    n="Siemy Di",               i="Drums",
         fh=666, head=0.46, cx=356, z=4),
    dict(key="manmohan", n="Manmohan<br>Dogra",      i="Tabla",
         fh=678, head=0.52, cx=632, z=4),
    dict(key="varun",    n="Varun Guru",             i="Guitar",
         fh=596, head=0.54, cx=868, z=2),
]
for a in ART:
    iw, ih = png_size(a["key"] + "_solo.png")
    a["h"] = a["fh"]
    a["w"] = round(a["fh"] * iw / ih)
    a["left"] = round(a["cx"] - a["head"] * a["w"])
    a["bottom"] = 0

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

/* ---- the arched window ---- */
.arch{{position:absolute;left:{ARCH_X}px;top:{ARCH_TOP}px;width:{ARCH_W}px;height:{ARCH_H}px;
  border-radius:{RADIUS}px {RADIUS}px 0 0;overflow:hidden;
  background:radial-gradient(120% 78% at 50% 8%,#37306B 0%,#1C1A46 46%,#12102A 100%);}}
/* a thin brass keyline traces the window */
.rim{{position:absolute;left:{ARCH_X - 9}px;top:{ARCH_TOP - 9}px;width:{ARCH_W + 18}px;
  height:{ARCH_H + 9}px;border:2px solid {GOLD};border-bottom:0;
  border-radius:{RADIUS + 9}px {RADIUS + 9}px 0 0;z-index:6;opacity:.85;}}
/* faint tala rings behind the players, following the arch */
.crown{{position:absolute;left:0;right:0;top:96px;z-index:5;text-align:center;}}
.crown .t{{font-size:15px;font-weight:600;letter-spacing:.44em;text-indent:.44em;
  text-transform:uppercase;color:{GOLD};}}
.crown .orn{{display:flex;align-items:center;justify-content:center;gap:14px;margin-top:14px;
  color:{GOLD};opacity:.8;}}
.crown .orn i{{display:block;width:66px;height:1px;background:{GOLD};}}
.crown .orn b{{font-size:13px;font-weight:400;}}
.rings{{position:absolute;left:50%;top:44px;width:760px;height:760px;transform:translateX(-50%);
  border-radius:50%;z-index:1;opacity:.16;
  background:repeating-radial-gradient(circle,transparent 0 46px,{GOLD} 46px 47px);}}

.who{{position:absolute;}}
.who img{{display:block;width:100%;height:100%;}}

/* names sit on the picture, on a scrim that rises out of the window's foot */
.scrim{{position:absolute;left:0;right:0;bottom:0;height:300px;z-index:7;
  background:linear-gradient(180deg,transparent 0%,rgba(12,10,32,.58) 42%,rgba(12,10,32,.93) 82%,
    rgba(12,10,32,.97) 100%);}}
.names{{position:absolute;left:0;right:0;bottom:22px;height:{NAME_BAND}px;z-index:8;
  display:grid;grid-template-columns:repeat(4,minmax(0,1fr));align-items:end;}}
.nm{{text-align:center;padding:0 6px;}}
.nm .n{{font-weight:900;font-size:26px;line-height:1.1;}}
.nm .n.big{{font-size:31px;}}
.nm .i{{margin-top:6px;font-size:10px;font-weight:600;letter-spacing:.26em;text-indent:.26em;
  text-transform:uppercase;color:{GOLD};}}
.nm .tick{{width:20px;height:2px;background:{GOLD};margin:9px auto 0;opacity:.75;}}

/* ---- information block (unchanged) ---- */
.info{{position:absolute;left:0;bottom:0;width:{W}px;height:{INFO_H}px;background:{INK};
  display:flex;align-items:center;gap:30px;padding:0 58px;z-index:9;}}
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

FIGURES = "".join(
    f'<div class="who" style="width:{a["w"]}px;left:{a["left"]}px;bottom:{a["bottom"]}px;'
    f'z-index:{a["z"]};"><img src="data:image/png;base64,{b64(a["key"] + "_solo.png")}" alt="">'
    f'</div>' for a in ART)

NAMES = "".join(
    f'<div class="nm"><div class="n fr{" big" if a["key"] in ("siemy", "manmohan") else ""}">'
    f'{a["n"]}</div><div class="tick"></div><div class="i">{a["i"]}</div></div>' for a in ART)

HTML = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><style>{CSS}</style></head>
<body>
<div class="arch">
  <div class="rings"></div>
  <div class="crown"><div class="t">A Study of Change</div>
    <div class="orn"><i></i><b>&#10022;</b><i></i></div></div>
  {FIGURES}
  <div class="scrim"></div>
  <div class="names">{NAMES}</div>
</div>
<div class="rim"></div>

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
    hp = HERE / "_arch.html"
    hp.write_text(HTML)
    subprocess.run([SHELL, "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
                    "--force-device-scale-factor=1", f"--window-size={W},{HT}",
                    "--virtual-time-budget=14000",
                    f"--screenshot={HERE / 'photo-arch.png'}", f"file://{hp}"],
                   capture_output=True)
    hp.unlink()
    print("rendered photo-arch.png")
