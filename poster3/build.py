#!/usr/bin/env python3
"""TALAYAN 2.0 — text-only concert posters, three designs, 1080x1350.

No photographs: this series is pure typography plus the ticket QR, so the
date, venue, time and the four names carry the whole poster.
"""
import base64, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).parent
SHELL = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"
W, HT = 1080, 1350

b64 = lambda p: base64.b64encode((HERE / p).read_bytes()).decode()
FR, P3, P5, P6, P7 = (b64(f) for f in
                      ("fr900.woff2", "pop300.woff2", "pop500.woff2", "pop600.woff2", "pop700.woff2"))
QR = b64("qr_poster.png")

# ---------------------------------------------------------------- content
THEME   = "A Study of Change"
DATE_L  = "Saturday 7 November 2026"
DATE_N  = "07.11.26"
VENUE   = "St John&rsquo;s Hoxton &middot; London"
VENUE_S = "St John&rsquo;s Hoxton, London"
TIMES   = "Doors 6:30pm &middot; Music 7:00pm"
ABOUT   = ("Four players. Three traditions. One pulse. A drum kit shaped by jazz and Africa, "
           "a tabla carrying centuries of tala, a sitar and a guitar that sings in Carnatic &mdash; "
           "meeting for one night and becoming a single conversation.")
ABOUT_S = ("Four players. Three traditions. One pulse. Indian classical tala, the deep pulse of Africa "
           "and the improvising freedom of jazz, meeting for one night.")
FOOT    = "talayanfestival.com &nbsp;&middot;&nbsp; @talayanfestival"
ARTISTS = [("Siemy Di", "Drums"), ("Manmohan Dogra", "Tabla"),
           ("Etienne Bartholomew", "Sitar"), ("Varun Guru", "Guitar")]

FONTS = f"""
@font-face{{font-family:'Fr';font-weight:100 900;
  src:url(data:font/woff2;base64,{FR}) format('woff2');}}
@font-face{{font-family:'Pop';font-weight:300;src:url(data:font/woff2;base64,{P3}) format('woff2');}}
@font-face{{font-family:'Pop';font-weight:500;src:url(data:font/woff2;base64,{P5}) format('woff2');}}
@font-face{{font-family:'Pop';font-weight:600;src:url(data:font/woff2;base64,{P6}) format('woff2');}}
@font-face{{font-family:'Pop';font-weight:700;src:url(data:font/woff2;base64,{P7}) format('woff2');}}
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{width:{W}px;height:{HT}px;}}
body{{position:relative;overflow:hidden;font-family:'Pop',system-ui,sans-serif;}}
.fr{{font-family:'Fr',Georgia,serif;font-variation-settings:'opsz' 144;}}
/* an <svg> is a replaced element, so inset:0 alone leaves it at its intrinsic
   300x150 and stamps a grey box in the corner — it needs an explicit size */
.grain{{position:absolute;inset:0;width:100%;height:100%;z-index:20;opacity:.10;
  mix-blend-mode:multiply;pointer-events:none;}}
.qr{{position:relative;z-index:30;}}
.qr img{{display:block;width:100%;height:100%;}}
"""

GRAIN = ('<svg class="grain"><filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.85" '
         'numOctaves="4"/></filter><rect width="100%" height="100%" filter="url(#g)"/></svg>')


def page(css, body):
    return (f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
            f'<style>{FONTS}{css}</style></head><body>{body}{GRAIN}</body></html>')


def render(html, out):
    hp = HERE / f"_{out}.html"
    hp.write_text(html)
    subprocess.run([SHELL, "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
                    "--force-device-scale-factor=1", f"--window-size={W},{HT}",
                    "--virtual-time-budget=12000",
                    f"--screenshot={HERE / (out + '.png')}", f"file://{hp}"],
                   capture_output=True)
    hp.unlink()
    print("rendered", out + ".png")


# ============================================================ A — THE BILL
def bill():
    """Letterpress concert bill: parchment, centred, heavy rules, huge date."""
    css = """
body{background:#F4ECDD;color:#12102A;}
.edge{position:absolute;inset:26px;border:2px solid #12102A;}
.edge::after{content:'';position:absolute;inset:9px;border:1px solid rgba(18,16,42,.4);}
.in{position:absolute;inset:26px;padding:52px 62px 44px;display:flex;flex-direction:column;
  align-items:center;text-align:center;}
.theme{font-size:17px;font-weight:600;letter-spacing:.44em;text-indent:.44em;text-transform:uppercase;
  color:#9A6B12;}
.theme i{font-style:normal;color:#12102A;}
.rule{width:100%;height:5px;background:#12102A;margin:18px 0 6px;}
.rule.thin{height:2px;margin:14px 0;}
.rule.hair{height:1px;background:rgba(18,16,42,.42);margin:16px 0;}
.mast{font-weight:900;font-size:118px;line-height:.88;letter-spacing:.005em;margin:10px 0 2px;}
.mast b{font-weight:900;color:#C2451C;}
.pres{font-size:13px;font-weight:600;letter-spacing:.42em;text-indent:.42em;text-transform:uppercase;
  color:rgba(18,16,42,.62);margin-bottom:12px;}

.datewrap{width:100%;background:#12102A;color:#F4ECDD;padding:20px 18px 24px;margin-top:4px;}
.dow{font-size:19px;font-weight:700;letter-spacing:.40em;text-indent:.40em;text-transform:uppercase;
  color:#E8963F;}
.dbig{font-weight:900;font-size:128px;line-height:.9;letter-spacing:-.01em;margin-top:2px;}
.dmon{font-weight:900;font-size:46px;line-height:1;letter-spacing:.02em;margin-top:4px;}

.where{margin-top:20px;}
.where .v{font-weight:900;font-size:40px;line-height:1.1;}
.where .t{margin-top:8px;font-size:23px;font-weight:600;letter-spacing:.05em;color:#12102A;}
.where .t b{font-weight:700;color:#C2451C;}

.cast{width:100%;margin-top:6px;}
.cast .n{font-weight:900;font-size:41px;line-height:1.16;}
.cast .i{font-size:13px;font-weight:600;letter-spacing:.34em;text-indent:.34em;text-transform:uppercase;
  color:#9A6B12;margin-top:1px;}
.cast .row+.row{margin-top:11px;}

.about{font-size:16.5px;font-weight:300;line-height:1.6;color:rgba(18,16,42,.84);max-width:46ch;
  margin-top:4px;}
.foot{margin-top:auto;width:100%;display:flex;align-items:center;gap:20px;text-align:left;}
.qr{width:192px;height:192px;flex:0 0 auto;background:#fff;border:2px solid #12102A;}
.foot .fi{flex:1 1 auto;}
.foot .sc{font-weight:900;font-size:27px;line-height:1.1;}
.foot .su{font-size:14.5px;font-weight:500;color:rgba(18,16,42,.72);margin-top:5px;line-height:1.45;}
.foot .web{font-size:13px;font-weight:600;letter-spacing:.2em;text-transform:uppercase;margin-top:9px;
  color:#9A6B12;}
"""
    cast = "".join(
        f'<div class="row"><div class="n fr">{n}</div><div class="i">{i}</div></div>'
        for n, i in ARTISTS)
    body = f"""
<div class="edge"></div>
<div class="in">
  <div class="theme"><i>Talayan</i> &middot; {THEME}</div>
  <div class="rule"></div>
  <div class="pres">One night in London</div>
  <div class="mast fr">TALAYAN <b>2.0</b></div>
  <div class="rule thin"></div>

  <div class="datewrap">
    <div class="dow">Saturday</div>
    <div class="dbig fr">7 NOV</div>
    <div class="dmon fr">2026</div>
  </div>

  <div class="where">
    <div class="v fr">{VENUE_S}</div>
    <div class="t">Doors <b>6:30pm</b> &nbsp;&middot;&nbsp; Music <b>7:00pm</b></div>
  </div>

  <div class="rule hair"></div>
  <div class="cast">{cast}</div>
  <div class="rule hair"></div>

  <div class="about">{ABOUT_S}</div>

  <div class="foot">
    <div class="qr"><img src="data:image/png;base64,{QR}" alt=""></div>
    <div class="fi">
      <div class="sc fr">Scan to book tickets</div>
      <div class="su">Point your camera at the code, or book online at talayanfestival.com</div>
      <div class="web">{FOOT}</div>
    </div>
  </div>
</div>"""
    render(page(css, body), "text-bill")


# ============================================================ B — THE GRID
def grid():
    """Swiss modernist: indigo ground, giant date numerals, strict left column."""
    css = """
body{background:#0B0E23;color:#F4ECDD;}
.field{position:absolute;inset:0;
  background:radial-gradient(120% 80% at 84% 4%,#1A2050 0%,#0B0E23 58%);}
.in{position:absolute;inset:0;padding:64px 66px 58px;display:flex;flex-direction:column;}
.top{display:flex;justify-content:space-between;align-items:flex-start;}
.theme{font-size:14px;font-weight:600;letter-spacing:.34em;text-indent:.34em;text-transform:uppercase;
  color:#E8963F;}
.theme span{display:block;color:rgba(244,236,221,.62);margin-top:6px;letter-spacing:.24em;text-indent:.24em;}
.tag{font-size:12px;font-weight:600;letter-spacing:.26em;text-indent:.26em;text-transform:uppercase;
  color:#0B0E23;background:#E8963F;padding:8px 14px;border-radius:999px;}
.hr{height:2px;background:rgba(201,162,75,.42);margin:22px 0 0;}
.hr.gold{background:#C9A24B;height:3px;}

.mast{font-weight:900;font-size:104px;line-height:.9;letter-spacing:.004em;margin-top:26px;}
.mast b{font-weight:900;color:#E8963F;}

.dn{font-weight:900;font-size:206px;line-height:.84;letter-spacing:-.02em;margin-top:14px;color:#F4ECDD;}
.dl{font-size:31px;font-weight:700;letter-spacing:.06em;margin-top:10px;color:#E8963F;}

.grid2{display:flex;gap:34px;margin-top:22px;}
.grid2>div{flex:1 1 0;}
.k{font-size:11.5px;font-weight:600;letter-spacing:.30em;text-indent:.30em;text-transform:uppercase;
  color:#C9A24B;}
.v{font-weight:900;font-size:31px;line-height:1.2;margin-top:7px;}
/* clock times stay in the sans — the display serif's 3 reads as a 5 at this size */
.vt{font-family:'Pop';font-weight:700;font-size:30px;line-height:1.2;margin-top:8px;letter-spacing:-.01em;}
.vt small{display:block;font-weight:500;font-size:18px;letter-spacing:.01em;
  color:rgba(244,236,221,.8);margin-top:5px;}

.cast{margin-top:30px;}
.cline{display:flex;align-items:baseline;gap:16px;padding:18px 0;
  border-bottom:1px solid rgba(201,162,75,.26);}
.cline:first-child{border-top:1px solid rgba(201,162,75,.26);}
.cline .n{font-weight:900;font-size:44px;line-height:1;flex:1 1 auto;}
.cline .i{font-size:12.5px;font-weight:600;letter-spacing:.28em;text-indent:.28em;text-transform:uppercase;
  color:#E8963F;flex:0 0 auto;}

.about{margin-top:28px;font-size:17.5px;font-weight:300;line-height:1.66;
  color:rgba(244,236,221,.82);max-width:54ch;}

.foot{margin-top:auto;padding-top:26px;border-top:2px solid rgba(201,162,75,.42);
  display:flex;align-items:flex-end;gap:22px;}
.foot .fi{flex:1 1 auto;}
.sc{font-weight:900;font-size:29px;line-height:1.08;}
.su{font-size:14.5px;font-weight:500;color:rgba(244,236,221,.7);margin-top:6px;}
.web{font-size:12.5px;font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:#C9A24B;
  margin-top:10px;}
.qr{width:228px;height:228px;flex:0 0 auto;background:#fff;border-radius:4px;}
"""
    cast = "".join(
        f'<div class="cline"><div class="n fr">{n}</div><div class="i">{i}</div></div>'
        for n, i in ARTISTS)
    body = f"""
<div class="field"></div>
<div class="in">
  <div class="top">
    <div class="theme">Talayan <span>{THEME}</span></div>
    <div class="tag">One night only</div>
  </div>
  <div class="hr gold"></div>

  <div class="mast fr">TALAYAN <b>2.0</b></div>
  <div class="dn fr">{DATE_N}</div>
  <div class="dl fr">{DATE_L}</div>

  <div class="grid2">
    <div><div class="k">Venue</div><div class="v fr">{VENUE}</div></div>
    <div><div class="k">Times</div><div class="vt">Doors 6:30pm<small>Music from 7:00pm</small></div></div>
  </div>

  <div class="cast">{cast}</div>
  <div class="about">{ABOUT}</div>

  <div class="foot">
    <div class="fi">
      <div class="sc fr">Scan to book tickets</div>
      <div class="su">Or book online at talayanfestival.com</div>
      <div class="web">{FOOT}</div>
    </div>
    <div class="qr"><img src="data:image/png;base64,{QR}" alt=""></div>
  </div>
</div>"""
    render(page(css, body), "text-grid")


# ============================================================ C — THE STUB
def stub():
    """Ticket stub: deep crimson, gold deco frame, boxed date, perforated QR stub."""
    css = """
body{background:#7C1210;color:#FFF3DC;}
.field{position:absolute;inset:0;
  background:linear-gradient(168deg,#9A1A15 0%,#7C1210 46%,#590C0C 100%);}
.frame{position:absolute;left:30px;right:30px;top:30px;bottom:30px;border:3px solid #E8B65A;}
.frame::after{content:'';position:absolute;inset:8px;border:1px solid rgba(232,182,90,.5);}
.corner{position:absolute;width:26px;height:26px;border:3px solid #E8B65A;}
.c1{left:52px;top:52px;border-right:0;border-bottom:0;}
.c2{right:52px;top:52px;border-left:0;border-bottom:0;}
.c3{left:52px;bottom:52px;border-right:0;border-top:0;}
.c4{right:52px;bottom:52px;border-left:0;border-top:0;}

.in{position:absolute;inset:30px;padding:50px 58px 0;display:flex;flex-direction:column;
  align-items:center;text-align:center;}
.theme{font-size:15px;font-weight:600;letter-spacing:.40em;text-indent:.40em;text-transform:uppercase;
  color:#E8B65A;}
.orn{display:flex;align-items:center;gap:12px;margin:14px 0 8px;color:#E8B65A;}
.orn i{display:block;width:72px;height:1px;background:#E8B65A;}
.orn b{font-size:15px;}
.mast{font-weight:900;font-size:110px;line-height:.9;}
.mast b{font-weight:900;color:#E8B65A;}
.sub{font-size:15px;font-weight:600;letter-spacing:.34em;text-indent:.34em;text-transform:uppercase;
  color:rgba(255,243,220,.78);margin-top:10px;}

.tick{margin-top:20px;width:100%;border:3px solid #E8B65A;background:rgba(0,0,0,.2);padding:16px 14px 20px;}
.tick .dow{font-size:18px;font-weight:700;letter-spacing:.42em;text-indent:.42em;text-transform:uppercase;
  color:#E8B65A;}
.tick .big{font-weight:900;font-size:116px;line-height:.9;margin-top:4px;}
.tick .yr{font-weight:900;font-size:40px;line-height:1;letter-spacing:.06em;margin-top:2px;}
.tick .ln{height:1px;background:rgba(232,182,90,.5);margin:15px 34px;}
.tick .v{font-weight:900;font-size:35px;line-height:1.15;}
.tick .t{font-size:21px;font-weight:600;letter-spacing:.04em;margin-top:7px;color:#FFF3DC;}
.tick .t b{font-weight:700;color:#E8B65A;}

.cast{margin-top:20px;width:100%;}
.cast .n{font-weight:900;font-size:39px;line-height:1.14;}
.cast .i{font-size:12px;font-weight:600;letter-spacing:.32em;text-indent:.32em;text-transform:uppercase;
  color:#E8B65A;margin-top:2px;}
.cast .row+.row{margin-top:10px;}
.about{margin-top:16px;font-size:15.5px;font-weight:300;line-height:1.58;
  color:rgba(255,243,220,.84);max-width:46ch;}

.perf{position:absolute;left:30px;right:30px;bottom:212px;height:2px;
  background:repeating-linear-gradient(90deg,#E8B65A 0 11px,transparent 11px 22px);opacity:.8;}
/* punched holes either side of the perforation — deep shadow, not a foreign colour */
.notch{position:absolute;width:30px;height:30px;border-radius:50%;background:#43070A;bottom:198px;
  box-shadow:inset 0 2px 5px rgba(0,0,0,.55);}
.notch.l{left:15px;} .notch.r{right:15px;}
.stubarea{position:absolute;left:30px;right:30px;bottom:30px;height:182px;
  display:flex;align-items:center;gap:24px;padding:0 62px;}
.qr{width:172px;height:172px;flex:0 0 auto;background:#fff;}
.stubarea .fi{flex:1 1 auto;text-align:left;}
.sc{font-weight:900;font-size:27px;line-height:1.08;}
.su{font-size:14px;font-weight:500;color:rgba(255,243,220,.76);margin-top:5px;}
.web{font-size:12.5px;font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:#E8B65A;
  margin-top:9px;}
"""
    cast = "".join(
        f'<div class="row"><div class="n fr">{n}</div><div class="i">{i}</div></div>'
        for n, i in ARTISTS)
    body = f"""
<div class="field"></div>
<div class="frame"></div>
<div class="corner c1"></div><div class="corner c2"></div>
<div class="corner c3"></div><div class="corner c4"></div>

<div class="in">
  <div class="theme">{THEME}</div>
  <div class="orn"><i></i><b>&#10022;</b><i></i></div>
  <div class="mast fr">TALAYAN <b>2.0</b></div>
  <div class="sub">One night in London</div>

  <div class="tick">
    <div class="dow">Saturday</div>
    <div class="big fr">7 NOVEMBER</div>
    <div class="yr fr">2026</div>
    <div class="ln"></div>
    <div class="v fr">{VENUE_S}</div>
    <div class="t">Doors <b>6:30pm</b> &nbsp;&middot;&nbsp; Music <b>7:00pm</b></div>
  </div>

  <div class="cast">{cast}</div>
  <div class="about">{ABOUT_S}</div>
</div>

<div class="perf"></div>
<div class="notch l"></div><div class="notch r"></div>
<div class="stubarea">
  <div class="qr"><img src="data:image/png;base64,{QR}" alt=""></div>
  <div class="fi">
    <div class="sc fr">Scan to book tickets</div>
    <div class="su">Point your camera at the code to book online</div>
    <div class="web">{FOOT}</div>
  </div>
</div>"""
    render(page(css, body), "text-stub")


BUILD = {"bill": bill, "grid": grid, "stub": stub}

if __name__ == "__main__":
    for a in (sys.argv[1:] or list(BUILD)):
        BUILD[a]()
