#!/usr/bin/env python3
"""TALAYAN 2.0 — final STAMP series. Solo posters + group, 1080x1350.

Group hierarchy: Siemy and Manmohan centre and larger (equal to each other);
Etienne and Varun outside and equal to each other. Names are set large and
legible under every face, on a scrim so they read against any photograph.
"""
import base64, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).parent
SCR = pathlib.Path("/tmp/claude-0/-home-user-Talayan/3051a222-024a-5ff2-9d30-ff7a483ba6a6/scratchpad")
# cutouts live beside this script so the posters survive a fresh checkout;
# the scratchpad copy is only a fallback while a session is still warm.
CUT = HERE / "cut" if (HERE / "cut").is_dir() else SCR / "cut"
SHELL = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"

b64 = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()
P3, P5 = (b64(HERE / f"pop{w}.woff2") for w in (300, 500))
FR = b64(HERE / "fr600.woff2")
IMG = {k: b64(CUT / f"{k}_solo.png") for k in ("etienne", "siemy", "manmohan", "varun")}

W, HT = 1080, 1350
INK, CREAM, GOLD = "#1B0714", "#FFF3DC", "#F5B921"

ART = {
 "siemy":    dict(n1="Siemy", n2="Di", inst="DRUMS",
                  bg="#C8241F", bg2="#8E1512", accent="#F5B921", w=930, left=70,  top=170),
 "manmohan": dict(n1="Manmohan", n2="Dogra", inst="TABLA",
                  bg="#E08A15", bg2="#A85D06", accent="#3A0A0A", naccent="#F5B921",
                  w=820, left=10, top=168),
 "etienne":  dict(n1="Etienne", n2="Bartholomew", inst="SITAR",
                  bg="#12807F", bg2="#0A5654", accent="#F5B921", w=900, left=90,  top=150),
 "varun":    dict(n1="Varun", n2="Guru", inst="GUITAR",
                  bg="#4B2A8E", bg2="#2E1760", accent="#F5B921", w=880, left=110, top=140),
}

STAMP = """<div class="stamp"><div class="ring"><div class="sd">SAT</div>
  <div class="sn">7 NOV</div><div class="sy">2026</div></div></div>"""

BAR = """<div class="bar">
  <div><span>Venue</span><b>St John&rsquo;s Hoxton &middot; London</b></div>
  <div><span>Doors</span><b>6:30pm &middot; Music 7:00pm</b></div>
  <div class="last"><span>Follow</span><b>@talayanfestival &middot; talayanfestival.com</b></div>
</div>"""

CSS = """
@font-face{font-family:'Pop';font-weight:300;src:url(data:font/woff2;base64,__P3__) format('woff2');}
@font-face{font-family:'Pop';font-weight:500;src:url(data:font/woff2;base64,__P5__) format('woff2');}
@font-face{font-family:'Fraunces';font-weight:600;src:url(data:font/woff2;base64,__FR__) format('woff2');}
*{margin:0;padding:0;box-sizing:border-box;}
html,body{width:__W__px;height:__HT__px;}
body{position:relative;overflow:hidden;font-family:'Pop',system-ui,sans-serif;color:__CREAM__;}
.field{position:absolute;inset:0;background:linear-gradient(168deg,__BG__ 0%,__BG__ 52%,__BG2__ 100%);}
.disc{position:absolute;border-radius:50%;background:rgba(255,243,220,.10);}
.rail{position:absolute;left:56px;top:50px;z-index:8;font-family:'Fraunces',Georgia,serif;
  font-weight:600;font-size:34px;letter-spacing:.06em;}
.rail b{color:__ACCENT__;}
.hair{position:absolute;left:56px;right:56px;top:106px;height:2px;background:__CREAM__;opacity:.55;z-index:8;}
.inst{position:absolute;left:0;right:0;z-index:2;text-align:center;font-family:'Fraunces',Georgia,serif;
  font-weight:600;line-height:.9;color:transparent;-webkit-text-stroke:3px rgba(255,243,220,.55);
  letter-spacing:.03em;white-space:nowrap;}
.who{position:absolute;z-index:4;} .who img{width:100%;height:auto;display:block;}
.stamp{position:absolute;z-index:9;transform:rotate(-9deg);}
.ring{width:236px;height:236px;border-radius:50%;border:4px solid __ACCENT__;
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  box-shadow:0 0 0 7px transparent,0 0 0 9px __ACCENT__;background:rgba(27,7,20,.42);}
.sd{font-size:19px;font-weight:500;letter-spacing:.34em;text-indent:.34em;color:__ACCENT__;}
.sn{font-family:'Fraunces',Georgia,serif;font-weight:600;font-size:60px;line-height:1.04;color:__CREAM__;}
.sy{font-size:20px;font-weight:500;letter-spacing:.26em;text-indent:.26em;color:__ACCENT__;}
.bar{position:absolute;left:0;right:0;bottom:0;height:118px;z-index:9;background:__INK__;
  display:flex;align-items:center;padding:0 46px;}
.bar>div{flex:1 1 0;padding-right:14px;} .bar>div.last{flex:1.5 1 0;}
.bar span{display:block;font-size:10px;font-weight:500;letter-spacing:.30em;text-transform:uppercase;
  color:__GOLD__;text-indent:.30em;}
.bar b{display:block;margin-top:5px;font-size:14px;font-weight:500;color:__CREAM__;letter-spacing:.02em;}
.grain{position:absolute;inset:0;z-index:10;opacity:.13;mix-blend-mode:multiply;pointer-events:none;}
"""


def shell(extra, body, v):
    css = (CSS.replace("__P3__", P3).replace("__P5__", P5).replace("__FR__", FR)
              .replace("__W__", str(W)).replace("__HT__", str(HT))
              .replace("__CREAM__", CREAM).replace("__INK__", INK).replace("__GOLD__", GOLD)
              .replace("__BG__", v["bg"]).replace("__BG2__", v["bg2"])
              .replace("__ACCENT__", v["accent"])) + extra
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><style>{css}</style></head>
<body><div class="field"></div>{body}
<svg class="grain"><filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="4"/>
</filter><rect width="100%" height="100%" filter="url(#g)"/></svg></body></html>"""


def render(html, out):
    hp = HERE / ("_t_" + out + ".html"); hp.write_text(html)
    subprocess.run([SHELL, "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
                    "--force-device-scale-factor=1", f"--window-size={W},{HT}",
                    "--virtual-time-budget=9000", f"--screenshot={HERE/(out+'.png')}", f"file://{hp}"],
                   capture_output=True)
    hp.unlink(); print("rendered", out + ".png")


def solo(key):
    v = ART[key]
    # surname + role can carry their own accent so they stay legible on the field
    na = v.get("naccent", v["accent"])
    extra = f"""
.disc{{width:940px;height:940px;left:70px;top:210px;}}
.inst{{top:286px;font-size:200px;text-indent:-140px;}}
.who{{left:{v['left']}px;top:{v['top']}px;width:{v['w']}px;}}
.stamp{{right:44px;top:150px;}}
/* scrim so the name always reads over the photograph */
.nscrim{{position:absolute;left:0;right:0;bottom:118px;height:430px;z-index:6;
  background:linear-gradient(180deg,transparent 0%,rgba(20,4,14,.30) 42%,rgba(20,4,14,.72) 100%);}}
.name{{position:absolute;left:56px;right:56px;bottom:196px;z-index:8;font-family:'Fraunces',Georgia,serif;
  font-weight:600;font-size:112px;line-height:.92;letter-spacing:.004em;}}
.name em{{display:block;font-style:normal;color:{na};}}
.role{{position:absolute;left:60px;bottom:150px;z-index:8;font-size:17px;font-weight:500;
  letter-spacing:.40em;text-transform:uppercase;color:{na};text-indent:.40em;}}
"""
    body = f"""
<div class="disc"></div>
<div class="rail">TALAYAN <b>2.0</b></div><div class="hair"></div>
<div class="inst">{v['inst']}</div>
<div class="who"><img src="data:image/png;base64,{IMG[key]}" alt=""></div>
<div class="nscrim"></div>
{STAMP}
<div class="name">{v['n1']}<em>{v['n2']}</em></div>
<div class="role">{v['inst']} &middot; Talayan 2.0</div>
{BAR}"""
    render(shell(extra, body, v), f"solo-{key}")


def group():
    v = dict(bg="#C8241F", bg2="#7C1210", accent=GOLD)
    # leads centre + larger; guests outside + equal
    extra = """
.disc{width:1010px;height:1010px;left:36px;top:150px;}
.inst{top:196px;font-size:186px;letter-spacing:.08em;text-indent:-96px;}
.g{position:absolute;z-index:4;} .g img{width:100%;height:auto;display:block;}
.g-et{left:-26px; top:322px; width:468px;}
.g-si{left:170px; top:288px; width:566px;}
.g-mm{left:452px; top:316px; width:566px;}
.g-va{left:742px; top:306px; width:452px;}
.stamp{right:38px;top:120px;}
.gscrim{position:absolute;left:0;right:0;bottom:118px;height:470px;z-index:6;
  background:linear-gradient(180deg,transparent 0%,rgba(20,4,14,.34) 40%,rgba(20,4,14,.80) 100%);}
.gn{position:absolute;z-index:8;transform:translateX(-50%);text-align:center;width:270px;}
.gn .n{font-family:'Fraunces',Georgia,serif;font-weight:600;font-size:27px;line-height:1.14;color:#FFF3DC;}
.gn .r{margin-top:6px;font-size:12px;font-weight:500;letter-spacing:.26em;text-transform:uppercase;
  color:#F5B921;text-indent:.26em;}
.n-et{left:126px; bottom:388px;} .n-si{left:394px; bottom:388px;}
.n-mm{left:672px; bottom:388px;} .n-va{left:968px; bottom:388px;}
.tal{position:absolute;left:0;right:0;bottom:180px;z-index:8;text-align:center;
  font-family:'Fraunces',Georgia,serif;font-weight:600;font-size:136px;line-height:1;letter-spacing:.03em;}
.tal b{color:#F5B921;}
.sub{position:absolute;left:0;right:0;bottom:140px;z-index:8;text-align:center;font-size:16px;
  font-weight:500;letter-spacing:.34em;text-transform:uppercase;color:#FFF3DC;opacity:.88;text-indent:.34em;}
"""
    body = f"""
<div class="disc"></div>
<div class="rail">TALAYAN <b>2.0</b></div><div class="hair"></div>
<div class="inst">LONDON</div>
<div class="g g-et"><img src="data:image/png;base64,{IMG['etienne']}" alt=""></div>
<div class="g g-si"><img src="data:image/png;base64,{IMG['siemy']}" alt=""></div>
<div class="g g-mm"><img src="data:image/png;base64,{IMG['manmohan']}" alt=""></div>
<div class="g g-va"><img src="data:image/png;base64,{IMG['varun']}" alt=""></div>
<div class="gscrim"></div>
{STAMP}
<div class="gn n-et"><div class="n">Etienne<br>Bartholomew</div><div class="r">Sitar</div></div>
<div class="gn n-si"><div class="n">Siemy Di</div><div class="r">Drums</div></div>
<div class="gn n-mm"><div class="n">Manmohan<br>Dogra</div><div class="r">Tabla</div></div>
<div class="gn n-va"><div class="n">Varun Guru</div><div class="r">Guitar</div></div>
<div class="tal">TALAYAN <b>2.0</b></div>
<div class="sub">Saturday 7 November 2026 &middot; London</div>
{BAR}"""
    render(shell(extra, body, v), "group-final")


if __name__ == "__main__":
    for a in (sys.argv[1:] or ["group"] + list(ART)):
        group() if a == "group" else solo(a)
