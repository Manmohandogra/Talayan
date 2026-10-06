#!/usr/bin/env python3
"""TALAYAN 2.0 — "STAMP" series. Solo artist posters + a group poster, 1080x1350.

A different system from the torn-paper design: flat bold colour, a giant outlined
instrument word behind the player, a rotated date stamp, and heavy Fraunces names.
Each artist carries their own accent so the solo posters read as one campaign.
"""
import base64, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).parent
SCR = pathlib.Path("/tmp/claude-0/-home-user-Talayan/3051a222-024a-5ff2-9d30-ff7a483ba6a6/scratchpad")
SHELL = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"

b64 = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()
P3, P5 = (b64(HERE / f"pop{w}.woff2") for w in (300, 500))
FR = b64(HERE / "fr600.woff2")
IMG = {k: b64(SCR / "cut" / f"{k}_solo.png") for k in ("etienne", "siemy", "manmohan", "varun")}

W, HT = 1080, 1350
INK, CREAM = "#1B0714", "#FFF3DC"

ART = {
 "siemy":    dict(name="Siemy Di",   n1="Siemy", n2="Di", inst="DRUMS",
                  bg="#C8241F", bg2="#8E1512", accent="#F5B921", w=930, left=70,  top=170),
 "manmohan": dict(name="Manmohan Dogra", n1="Manmohan", n2="Dogra", inst="TABLA",
                  bg="#E08A15", bg2="#A85D06", accent="#FFF3DC", w=960, left=60,  top=180),
 "etienne":  dict(name="Etienne Bartholomew", n1="Etienne", n2="Bartholomew", inst="SITAR",
                  bg="#12807F", bg2="#0A5654", accent="#F5B921", w=900, left=90,  top=150),
 "varun":    dict(name="Varun Guru", n1="Varun", n2="Guru", inst="GUITAR",
                  bg="#4B2A8E", bg2="#2E1760", accent="#F5B921", w=880, left=110, top=140),
}

STAMP = """<div class="stamp"><div class="ring"><div class="sd">SAT</div>
  <div class="sn">7 NOV</div><div class="sy">2026</div></div></div>"""

BAR = """<div class="bar">
  <div><span>Venue</span><b>St John&rsquo;s Hoxton &middot; London</b></div>
  <div><span>Doors</span><b>6:30pm &middot; Music 7:00pm</b></div>
  <div><span>Follow</span><b>@talayanfestival &middot; talayanfestival.com</b></div>
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

/* masthead rail */
.rail{position:absolute;left:56px;top:52px;z-index:8;font-family:'Fraunces',Georgia,serif;
  font-weight:600;font-size:34px;letter-spacing:.06em;}
.rail b{color:__ACCENT__;}
.hair{position:absolute;left:56px;right:56px;top:108px;height:2px;background:__CREAM__;opacity:.55;z-index:8;}

/* giant outlined instrument word, sitting behind the player */
.inst{position:absolute;left:0;right:0;z-index:2;text-align:center;font-family:'Fraunces',Georgia,serif;
  font-weight:600;line-height:.9;color:transparent;-webkit-text-stroke:3px rgba(255,243,220,.55);
  letter-spacing:.03em;white-space:nowrap;}

/* the player */
.who{position:absolute;z-index:4;}
.who img{width:100%;height:auto;display:block;}

/* date stamp */
.stamp{position:absolute;z-index:9;transform:rotate(-9deg);}
.ring{width:236px;height:236px;border-radius:50%;border:4px solid __ACCENT__;
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  box-shadow:0 0 0 7px transparent,0 0 0 9px __ACCENT__;background:rgba(27,7,20,.34);}
.sd{font-size:19px;font-weight:500;letter-spacing:.34em;text-indent:.34em;color:__ACCENT__;}
.sn{font-family:'Fraunces',Georgia,serif;font-weight:600;font-size:60px;line-height:1.04;color:__CREAM__;}
.sy{font-size:20px;font-weight:500;letter-spacing:.26em;text-indent:.26em;color:__ACCENT__;}

/* bottom bar */
.bar{position:absolute;left:0;right:0;bottom:0;height:118px;z-index:9;background:__INK__;
  display:flex;align-items:center;padding:0 46px;}
.bar>div{flex:1 1 0;padding-right:14px;}
.bar>div:last-child{flex:1.5 1 0;}
.bar span{display:block;font-size:10px;font-weight:500;letter-spacing:.30em;text-transform:uppercase;
  color:__ACCENT__;text-indent:.30em;}
.bar b{display:block;margin-top:5px;font-size:14px;font-weight:500;color:__CREAM__;letter-spacing:.02em;}
.grain{position:absolute;inset:0;z-index:10;opacity:.13;mix-blend-mode:multiply;pointer-events:none;}
"""


def shell(css_extra, body, v):
    css = (CSS.replace("__P3__", P3).replace("__P5__", P5).replace("__FR__", FR)
              .replace("__W__", str(W)).replace("__HT__", str(HT))
              .replace("__CREAM__", CREAM).replace("__INK__", INK)
              .replace("__BG__", v["bg"]).replace("__BG2__", v["bg2"])
              .replace("__ACCENT__", v["accent"])) + css_extra
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<style>{css}</style></head><body>
<div class="field"></div>{body}
<svg class="grain"><filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="4"/>
</filter><rect width="100%" height="100%" filter="url(#g)"/></svg>
</body></html>"""


def render(html, out):
    hp = HERE / ("_t_" + out + ".html"); hp.write_text(html)
    subprocess.run([SHELL, "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
                    "--force-device-scale-factor=1", f"--window-size={W},{HT}",
                    "--virtual-time-budget=9000", f"--screenshot={HERE/(out+'.png')}", f"file://{hp}"],
                   capture_output=True)
    hp.unlink(); print("rendered", out + ".png")


def solo(key):
    v = ART[key]
    extra = f"""
.disc{{width:940px;height:940px;left:70px;top:210px;}}
.inst{{top:286px;font-size:200px;text-indent:-140px;}}
.who{{left:{v['left']}px;top:{v['top']}px;width:{v['w']}px;}}
.stamp{{right:44px;top:150px;}}
.name{{position:absolute;left:56px;bottom:186px;z-index:8;font-family:'Fraunces',Georgia,serif;
  font-weight:600;font-size:104px;line-height:.94;letter-spacing:.005em;
  text-shadow:0 6px 26px rgba(20,4,14,.5);}}
.name em{{display:block;font-style:normal;color:{v['accent']};}}
.role{{position:absolute;left:60px;bottom:140px;z-index:8;font-size:16px;font-weight:500;
  letter-spacing:.42em;text-transform:uppercase;color:{v['accent']};text-indent:.42em;}}
"""
    body = f"""
<div class="disc"></div>
<div class="rail">TALAYAN <b>2.0</b></div><div class="hair"></div>
<div class="inst">{v['inst']}</div>
<div class="who"><img src="data:image/png;base64,{IMG[key]}" alt=""></div>
{STAMP}
<div class="name">{v['n1']}<em>{v['n2']}</em></div>
<div class="role">{v['inst']} &middot; Talayan 2.0</div>
{BAR}"""
    render(shell(extra, body, v), f"solo-{key}")


def group():
    v = dict(bg="#C8241F", bg2="#7C1210", accent="#F5B921")
    extra = """
.disc{width:1000px;height:1000px;left:40px;top:150px;}
.inst{top:214px;font-size:196px;letter-spacing:.08em;}
.g{position:absolute;z-index:4;}
.g img{width:100%;height:auto;display:block;}
.g1{left:-56px; top:326px; width:520px;}
.g2{left:206px; top:352px; width:474px;}
.g3{left:470px; top:344px; width:494px;}
.g4{left:706px; top:316px; width:470px;}
.stamp{right:40px;top:126px;}
.tal{position:absolute;left:0;right:0;bottom:196px;z-index:8;text-align:center;
  font-family:'Fraunces',Georgia,serif;font-weight:600;font-size:132px;line-height:1;
  letter-spacing:.03em;text-shadow:0 6px 26px rgba(20,4,14,.45);}
.tal b{color:#F5B921;}
.names{position:absolute;left:0;right:0;bottom:146px;z-index:8;text-align:center;
  font-size:17px;font-weight:500;letter-spacing:.16em;color:#FFF3DC;opacity:.92;}
.names i{font-style:normal;color:#F5B921;padding:0 8px;}
"""
    body = f"""
<div class="disc"></div>
<div class="rail">TALAYAN <b>2.0</b></div><div class="hair"></div>
<div class="inst">LONDON</div>
<div class="g g1"><img src="data:image/png;base64,{IMG['etienne']}" alt=""></div>
<div class="g g2"><img src="data:image/png;base64,{IMG['siemy']}" alt=""></div>
<div class="g g3"><img src="data:image/png;base64,{IMG['manmohan']}" alt=""></div>
<div class="g g4"><img src="data:image/png;base64,{IMG['varun']}" alt=""></div>
{STAMP}
<div class="tal">TALAYAN <b>2.0</b></div>
<div class="names">Siemy Di <i>&middot;</i> Manmohan Dogra <i>&middot;</i> Etienne Bartholomew <i>&middot;</i> Varun Guru</div>
{BAR}"""
    render(shell(extra, body, v), "stamp-group")


if __name__ == "__main__":
    args = sys.argv[1:] or ["group"] + list(ART)
    for a in args:
        group() if a == "group" else solo(a)
