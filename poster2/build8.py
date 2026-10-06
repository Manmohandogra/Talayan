#!/usr/bin/env python3
"""TALAYAN 2.0 — date launch poster, Instagram 1080x1350. Three layout options."""
import base64, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).parent
SCR = pathlib.Path("/tmp/claude-0/-home-user-Talayan/3051a222-024a-5ff2-9d30-ff7a483ba6a6/scratchpad")
SHELL = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"

b64 = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()
P3, P5 = (b64(HERE / f"pop{w}.woff2") for w in (300, 500))
FR = b64(HERE / "fr600.woff2")
H = {k: b64(SCR / "cut" / f"{k}_head.png") for k in ("etienne", "siemy", "manmohan", "varun")}

PAL = {
 "bombay": dict(top="#1FA3A0", top2="#12807F", strip="#E23B2E", strip2="#B8241C",
   plate="#5E0F1C", cream="#FFF3DC", hot="#F5B921", rule="#F5B921"),
 "fillmore": dict(top="#F26B21", top2="#E8156B", strip="#17B6B0", strip2="#0E8C8C",
   plate="#2B1052", cream="#FFF6E3", hot="#FFC93C", rule="#17B6B0"),
 "mod": dict(top="#F0B429", top2="#E8503A", strip="#0E8C8C", strip2="#0A6E70",
   plate="#14262E", cream="#FFF6E3", hot="#F0B429", rule="#E8503A"),
}
W, HT = 1080, 1350

LINEUP = """  <div class="lineup">
    <div class="c1"><div class="n">Etienne<br>Bartholomew</div><div class="r">Sitar</div></div>
    <div class="c2"><div class="n">Siemy Di</div><div class="r">Drums</div></div>
    <div class="c3"><div class="n">Manmohan<br>Dogra</div><div class="r">Tabla</div></div>
    <div class="c4"><div class="n">Varun Guru</div><div class="r">Guitar</div></div>
  </div>"""

HANDLES = ('<div class="web">talayanfestival.com &nbsp;&middot;&nbsp; @talayanfestival '
           '&nbsp;&middot;&nbsp; #Talayan2</div>')

# per-layout: plate height, how far to lift the figures, and the plate contents
LAYOUTS = {
 "lineup": dict(
   plate=548, lift=16,
   body=LINEUP + """
  <div class="hr"></div>
  <div class="when">Saturday 7 November 2026</div>
  <div class="venue">St John&rsquo;s Hoxton &middot; London</div>
  <div class="time">Doors 6:30pm &middot; Music 7:00pm</div>
  <div class="mast"><div class="t">TALAYAN <b>2.0</b></div></div>
  """ + HANDLES),
 "datehero": dict(
   plate=612, lift=80,
   body=LINEUP + """
  <div class="hr"></div>
  <div class="mast small"><div class="t">TALAYAN <b>2.0</b></div></div>
  <div class="bigdate">07 &middot; 11 &middot; 26</div>
  <div class="when tight">Saturday 7 November 2026</div>
  <div class="venue">St John&rsquo;s Hoxton &middot; London &nbsp;|&nbsp; Doors 6:30pm &middot; Music 7:00pm</div>
  """ + HANDLES),
 "stub": dict(
   plate=556, lift=24,
   body=LINEUP + """
  <div class="perf"></div>
  <div class="stub">
    <div><span>Date</span><b>Sat 7 Nov 2026</b></div>
    <div><span>Venue</span><b>St John&rsquo;s Hoxton</b></div>
    <div><span>Doors</span><b>6:30pm &middot; 7:00pm</b></div>
  </div>
  <div class="mast"><div class="t">TALAYAN <b>2.0</b></div></div>
  """ + HANDLES),
}


def build(layout, palname):
    v, L = PAL[palname], LAYOUTS[layout]
    P, lift = L["plate"], L["lift"]
    html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><style>
@font-face{{font-family:'Pop';font-weight:300;src:url(data:font/woff2;base64,{P3}) format('woff2');}}
@font-face{{font-family:'Pop';font-weight:500;src:url(data:font/woff2;base64,{P5}) format('woff2');}}
@font-face{{font-family:'Fraunces';font-weight:600;src:url(data:font/woff2;base64,{FR}) format('woff2');}}
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{width:{W}px;height:{HT}px;}}
body{{position:relative;overflow:hidden;font-family:'Pop',system-ui,sans-serif;
  background:linear-gradient(158deg,{v['top']} 0%,{v['top']} 42%,{v['top2']} 100%);}}
.torn{{position:absolute;inset:0;z-index:1;}} .torn svg{{width:100%;height:100%;}}

.cast{{position:absolute;inset:0;z-index:3;}}
.cast img{{position:absolute;display:block;}}
.etienne {{left:-44px; top:{64-lift}px; width:498px; filter:brightness(.95) saturate(.92);}}
.varun   {{left:624px; top:{60-lift}px; width:498px; filter:brightness(.95) saturate(.92);}}
.siemy   {{left:180px; top:{54-lift}px; width:530px; filter:brightness(1.07) contrast(1.04);}}
.manmohan{{left:432px; top:{46-lift}px; width:542px; filter:brightness(1.07) contrast(1.04);}}

.plate{{position:absolute;left:0;right:0;bottom:0;height:{P}px;z-index:6;background:{v['plate']};}}
.plateTop{{position:absolute;left:0;right:0;bottom:{P}px;height:86px;z-index:6;}}
.plateTop svg{{width:100%;height:100%;}}
.copy{{position:absolute;left:0;right:0;bottom:0;height:{P}px;z-index:7;display:flex;
  flex-direction:column;align-items:center;justify-content:center;padding:24px 40px 26px;}}

/* names, aligned under each photograph */
.lineup{{position:relative;width:100%;height:96px;}}
.lineup>div{{position:absolute;top:0;transform:translateX(-50%);text-align:center;width:230px;}}
.lineup .c1{{left:124px;}} .lineup .c2{{left:334px;}}
.lineup .c3{{left:556px;}} .lineup .c4{{left:892px;}}
.lineup .n{{font-family:'Fraunces',Georgia,serif;font-weight:600;font-size:23px;color:{v['cream']};line-height:1.16;}}
.lineup .r{{margin-top:5px;font-size:11px;font-weight:500;letter-spacing:.26em;text-transform:uppercase;
  color:{v['hot']};text-indent:.26em;}}

.hr{{width:250px;height:2px;margin:8px 0 16px;background:{v['rule']};opacity:.9;}}
.when{{font-family:'Fraunces',Georgia,serif;font-weight:600;font-size:52px;color:{v['cream']};line-height:1.06;}}
.when.tight{{font-size:30px;margin-top:10px;}}
.venue{{margin-top:12px;font-size:19px;font-weight:500;letter-spacing:.10em;color:{v['hot']};}}
.time{{margin-top:8px;font-size:17px;font-weight:300;color:{v['cream']};opacity:.86;letter-spacing:.05em;}}
.bigdate{{margin-top:14px;font-family:'Fraunces',Georgia,serif;font-weight:600;font-size:132px;
  line-height:1;color:{v['hot']};letter-spacing:.01em;}}

.perf{{width:100%;height:3px;margin:14px 0 18px;
  background:repeating-linear-gradient(90deg,{v['rule']} 0 12px,transparent 12px 24px);opacity:.75;}}
.stub{{display:flex;width:100%;}}
.stub>div{{flex:1 1 0;text-align:center;padding:0 6px;}}
.stub span{{display:block;font-size:11px;font-weight:500;letter-spacing:.28em;text-transform:uppercase;
  color:{v['hot']};text-indent:.28em;}}
.stub b{{display:block;margin-top:7px;font-family:'Fraunces',Georgia,serif;font-weight:600;
  font-size:23px;color:{v['cream']};}}

.mast{{margin-top:20px;}}
.mast .t{{font-family:'Fraunces',Georgia,serif;font-weight:600;font-size:124px;line-height:1.02;
  letter-spacing:.028em;color:{v['cream']};white-space:nowrap;text-indent:.028em;}}
.mast.small .t{{font-size:76px;}}
.mast .t b{{font-weight:600;color:{v['hot']};}}
.web{{margin-top:14px;font-size:13px;font-weight:500;letter-spacing:.24em;text-transform:uppercase;
  color:{v['cream']};opacity:.84;text-indent:.24em;text-align:center;}}
.grain{{position:absolute;inset:0;z-index:9;opacity:.14;mix-blend-mode:multiply;pointer-events:none;}}
</style></head><body>

<svg class="torn" viewBox="0 0 1080 1000" preserveAspectRatio="none">
 <defs>
  <filter id="rip" x="-14%" y="-8%" width="128%" height="116%">
    <feTurbulence type="fractalNoise" baseFrequency="0.014 0.09" numOctaves="4" seed="11" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="38" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <filter id="rip2" x="-14%" y="-8%" width="128%" height="116%">
    <feTurbulence type="fractalNoise" baseFrequency="0.017 0.075" numOctaves="4" seed="23" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="42" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <linearGradient id="sg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{v['strip']}"/><stop offset="1" stop-color="{v['strip2']}"/>
  </linearGradient>
 </defs>
 <g filter="url(#rip)">
   <rect x="66"  y="-30" width="362" height="1000" fill="url(#sg)"/>
   <rect x="648" y="-30" width="347" height="1000" fill="url(#sg)"/>
 </g>
 <g filter="url(#rip2)" opacity=".62">
   <rect x="460" y="-30" width="164" height="980" fill="url(#sg)"/>
   <rect x="1000" y="-30" width="116" height="990" fill="{v['top2']}"/>
 </g>
</svg>

<div class="cast">
  <img class="etienne"  src="data:image/png;base64,{H['etienne']}"  alt="">
  <img class="siemy"    src="data:image/png;base64,{H['siemy']}"    alt="">
  <img class="manmohan" src="data:image/png;base64,{H['manmohan']}" alt="">
  <img class="varun"    src="data:image/png;base64,{H['varun']}"    alt="">
</div>

<svg class="plateTop" viewBox="0 0 1080 86" preserveAspectRatio="none">
  <filter id="rip3" x="-6%" y="-40%" width="112%" height="180%">
    <feTurbulence type="fractalNoise" baseFrequency="0.06 0.024" numOctaves="4" seed="7" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="26" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <rect x="-20" y="36" width="1120" height="90" fill="{v['plate']}" filter="url(#rip3)"/>
</svg>
<div class="plate"></div>

<div class="copy">
{L['body']}
</div>

<svg class="grain"><filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="4"/>
 </filter><rect width="100%" height="100%" filter="url(#g)"/></svg>
</body></html>"""
    hp = HERE / f"b8_{layout}_{palname}.html"; hp.write_text(html)
    out = HERE / f"date-{layout}-{palname}.png"
    subprocess.run([SHELL, "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
                    "--force-device-scale-factor=1", f"--window-size={W},{HT}",
                    "--virtual-time-budget=9000", f"--screenshot={out}", f"file://{hp}"],
                   capture_output=True)
    hp.unlink(); print("rendered", out.name)


if __name__ == "__main__":
    pal = sys.argv[1] if len(sys.argv) > 1 else "bombay"
    for lay in LAYOUTS:
        build(lay, pal)
