#!/usr/bin/env python3
"""Generate BGS watermark pack - Blu Giggity Savagelyfe / BGS Designs."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import os, math

OUT = r"C:\Users\Blu\Downloads\BGS Designs"
os.makedirs(OUT, exist_ok=True)
F = r"C:\Windows\Fonts"

def font(path, size):
    return ImageFont.truetype(os.path.join(F, path), size)

FONTS = {
    "black": "ariblk.ttf",        # Arial Black - bold promo
    "bold": "arialbd.ttf",
    "regular": "arial.ttf",
    "impact": "impact.ttf",       # condensed bold
    "script1": "PRISTINA.TTF",    # elegant script (signature)
    "script2": "MISTRAL.TTF",     # hand script
    "hand": "Inkfree.ttf",        # handwritten
    "print": "segoeprb.ttf",      # segoe print bold
    "elegant": "Gabriola.ttf",    # luxury serif/script
    "mono": "consolab.ttf",       # mono bold
    "treb": "trebucbd.ttf",
}

def exists(p):
    import os as _o
    return _o.path.exists(_o.path.join(F, p))

# fallback check
for k,v in list(FONTS.items()):
    if not exists(v):
        print(f"missing font {v}, fallback to arial.ttf")
        FONTS[k] = "arial.ttf"

def center_text(draw, xy, text, font, **kw):
    # xy = center
    bbox = draw.textbbox((0,0), text, font=font, stroke_width=kw.get("stroke_width",0))
    w = bbox[2]-bbox[0]; h = bbox[3]-bbox[1]
    draw.text((xy[0]-w/2-bbox[0], xy[1]-h/2-bbox[1]), text, font=font, **kw)

def glow_text(size, main_text, main_font, sub_text=None, sub_font=None,
              core=(255,255,255,255), glow1=(0,229,255,255), glow2=(168,85,247,255),
              glow_radius=25):
    """Neon glow: blurred colored copies + crisp core."""
    img = Image.new("RGBA", size, (0,0,0,0))
    # glow layers
    for color, blur, offset in [(glow2, glow_radius, 0), (glow1, glow_radius//2, 0)]:
        layer = Image.new("RGBA", size, (0,0,0,0))
        d = ImageDraw.Draw(layer)
        center_text(d, (size[0]//2, size[1]//2 - (60 if sub_text else 0)),
                    main_text, main_font, fill=color, stroke_width=6, stroke_fill=color)
        layer = layer.filter(ImageFilter.GaussianBlur(blur))
        img = Image.alpha_composite(img, layer)
    # second outer thin neon line
    layer2 = Image.new("RGBA", size, (0,0,0,0))
    d2 = ImageDraw.Draw(layer2)
    center_text(d2, (size[0]//2, size[1]//2 - (60 if sub_text else 0)),
                main_text, main_font, fill=(0,0,0,0), stroke_width=3, stroke_fill=(220,240,255,255))
    img = Image.alpha_composite(img, layer2)
    # core
    d = ImageDraw.Draw(img)
    center_text(d, (size[0]//2, size[1]//2 - (60 if sub_text else 0)),
                main_text, main_font, fill=core, stroke_width=2, stroke_fill=glow1)
    if sub_text:
        center_text(d, (size[0]//2, size[1]//2 + 130), sub_text, sub_font,
                    fill=(200,225,255,255), stroke_width=0)
    return img

def chrome_gradient(size):
    grad = Image.new("RGBA", size, (0,0,0,0))
    px = grad.load()
    # vertical gradient: deep blue -> silver -> white -> blue-purple
    stops = [(10,30,80),(70,130,200),(230,240,255),(255,255,255),(140,120,255),(20,40,120)]
    h = size[1]
    for y in range(h):
        t = y/h* (len(stops)-1)
        i = int(t); f = t-i
        if i >= len(stops)-1:
            c = stops[-1]
        else:
            c = tuple(int(stops[i][j]*(1-f)+stops[i+1][j]*f) for j in range(3))
        for x in range(size[0]):
            px[x,y] = c+(255,)
    return grad

def draw_curved_text(base, center, radius, text, font, fill, top=True, letter_spacing=0):
    d = ImageDraw.Draw(base)
    # total arc
    widths = []
    for ch in text:
        bb = d.textbbox((0,0), ch, font=font)
        widths.append(bb[2]-bb[0]+letter_spacing)
    total_w = sum(widths)
    arc = total_w / radius  # radians
    start = -arc/2 + (-math.pi/2 if top else math.pi/2)
    # for bottom, reverse direction
    ang = start
    for ch, w in zip(text, widths):
        theta = ang + (w/2)/radius
        x = center[0] + radius*math.cos(theta)
        y = center[1] + radius*math.sin(theta)
        rot = math.degrees(theta) + (90 if top else -90)
        # render char
        bb = d.textbbox((0,0), ch, font=font)
        cw, chh = bb[2]-bb[0]+20, bb[3]-bb[1]+20
        tmp = Image.new("RGBA", (cw+40, chh+40), (0,0,0,0))
        td = ImageDraw.Draw(tmp)
        td.text((20-bb[0], 20-bb[1]), ch, font=font, fill=fill)
        tmp = tmp.rotate(-rot if top else -rot+180, resample=Image.BICUBIC, expand=True)
        base.alpha_composite(tmp, (int(x-tmp.width/2), int(y-tmp.height/2)))
        ang += w/radius
    return base

print("Generating...")

# 1. NEON blue-purple
img = glow_text((1920,640), "B.G.S.", font(FONTS["black"], 300),
                "BLU GIGGITY  •  SAVAGELYFE", font(FONTS["bold"], 64))
img.save(os.path.join(OUT,"01_neon_blue_purple.png"))
print("01 ok")

# 2. SIGNATURE script - handwritten personal
s = Image.new("RGBA",(1920,640),(0,0,0,0))
d = ImageDraw.Draw(s)
# soft shadow
shadow = Image.new("RGBA",(1920,640),(0,0,0,0))
ds = ImageDraw.Draw(shadow)
center_text(ds,(962,282),"Blu BGS",font(FONTS["script1"],300),fill=(0,0,0,160))
shadow = shadow.filter(ImageFilter.GaussianBlur(12))
s = Image.alpha_composite(s, shadow)
d = ImageDraw.Draw(s)
center_text(d,(960,270),"Blu BGS",font(FONTS["script1"],300),fill=(255,255,255,255))
# gold swash underline
d.line([(420,480),(1500,470)],fill=(255,200,80,255),width=8)
d.line([(420,495),(1500,485)],fill=(255,200,80,120),width=3)
center_text(d,(960,555),"S A V A G E L Y F E",font(FONTS["regular"],44),fill=(255,215,130,255))
s.save(os.path.join(OUT,"02_signature_script.png"))
# alt signature with Mistral
s2 = Image.new("RGBA",(1920,640),(0,0,0,0))
d2 = ImageDraw.Draw(s2)
center_text(d2,(960,270),"Blu Giggity",font(FONTS["script2"],220),fill=(255,255,255,255))
center_text(d2,(960,480),"SAVAGELYFE • BGS",font(FONTS["hand"],72),fill=(150,220,255,255))
s2.save(os.path.join(OUT,"02b_signature_hand.png"))
print("02 ok")

# 3. CIRCULAR BADGE 1200x1200
cb = Image.new("RGBA",(1200,1200),(0,0,0,0))
d = ImageDraw.Draw(cb)
cx=cy=600
d.ellipse([60,60,1140,1140],outline=(255,255,255,255),width=10)
d.ellipse([110,110,1090,1090],outline=(0,229,255,255),width=4)
# inner ring
d.ellipse([180,180,1020,1020],outline=(255,255,255,160),width=2)
cb = draw_curved_text(cb,(cx,cy),430,"BLU GIGGITY",font(FONTS["black"],84),fill=(255,255,255,255),top=True,letter_spacing=8)
cb = draw_curved_text(cb,(cx,cy),430,"SAVAGELYFE",font(FONTS["black"],84),fill=(0,229,255,255),top=False,letter_spacing=8)
d = ImageDraw.Draw(cb)
center_text(d,(600,540),"BGS",font(FONTS["black"],300),fill=(255,255,255,255),stroke_width=3,stroke_fill=(0,229,255,255))
center_text(d,(600,730),"★ EST • ENTERTAINMENT ★",font(FONTS["bold"],44),fill=(200,225,255,255))
# side stars
center_text(d,(220,600),"★",font(FONTS["bold"],60),fill=(0,229,255,255))
center_text(d,(980,600),"★",font(FONTS["bold"],60),fill=(168,85,247,255))
cb.save(os.path.join(OUT,"03_circular_badge.png"))
print("03 ok")

# 4. RECTANGULAR BADGE
rb = Image.new("RGBA",(1920,640),(0,0,0,0))
d = ImageDraw.Draw(rb)
d.rounded_rectangle([20,40,1900,600],radius=60,outline=(255,255,255,255),width=8)
d.rounded_rectangle([40,60,1880,580],radius=48,outline=(0,229,255,180),width=3)
center_text(d,(960,260),"B.G.S.",font(FONTS["black"],260),fill=(255,255,255,255))
center_text(d,(960,470),"BLU GIGGITY SAVAGELYFE — ENTERTAINMENT",font(FONTS["bold"],56),fill=(0,229,255,255))
rb.save(os.path.join(OUT,"04_rectangular_badge.png"))
print("04 ok")

# 5. SOCIAL PROFILE square 1080 (Telegram / MeWe avatar safe)
sp = Image.new("RGBA",(1080,1080),(10,12,28,255))
d = ImageDraw.Draw(sp)
# subtle radial glow bg
glow = Image.new("RGBA",(1080,1080),(0,0,0,0))
dg = ImageDraw.Draw(glow)
dg.ellipse([140,140,940,940],fill=(30,60,140,255))
glow = glow.filter(ImageFilter.GaussianBlur(80))
sp = Image.alpha_composite(sp, glow)
d = ImageDraw.Draw(sp)
d.ellipse([90,90,990,990],outline=(0,229,255,255),width=10)
center_text(d,(540,470),"BGS",font(FONTS["black"],340),fill=(255,255,255,255))
center_text(d,(540,720),"BLU GIGGITY",font(FONTS["bold"],72),fill=(0,229,255,255))
center_text(d,(540,800),"SAVAGELYFE",font(FONTS["bold"],72),fill=(168,85,247,255))
sp.convert("RGB").save(os.path.join(OUT,"05_social_profile_1080.jpg"),quality=92)
sp.save(os.path.join(OUT,"05_social_profile_1080.png"))
print("05 ok")

# 6. SOCIAL BANNER 1920x480 (Telegram channel / MeWe / stream header)
bn = Image.new("RGBA",(1920,480),(8,10,24,255))
d = ImageDraw.Draw(bn)
# neon edge lines
d.rectangle([0,0,1920,10],fill=(0,229,255,255))
d.rectangle([0,470,1920,480],fill=(168,85,247,255))
center_text(d,(960,190),"B.G.S. — BLU GIGGITY SAVAGELYFE",font(FONTS["black"],130),fill=(255,255,255,255))
center_text(d,(960,330),"TELEGRAM • MEWE • STREAMING • BROADCAST",font(FONTS["bold"],52),fill=(0,229,255,255))
bn.convert("RGB").save(os.path.join(OUT,"06_social_banner_1920x480.jpg"),quality=90)
bn.save(os.path.join(OUT,"06_social_banner_1920x480.png"))
print("06 ok")

# 7. STREAM LOWER THIRD 1920x400 transparent (OBS / broadcast)
lt = Image.new("RGBA",(1920,400),(0,0,0,0))
d = ImageDraw.Draw(lt)
d.rounded_rectangle([60,80,1100,320],radius=24,fill=(0,0,0,170),outline=(0,229,255,255),width=4)
d.rectangle([60,80,90,320],fill=(0,229,255,255))
d.text((140,120),"BLU GIGGITY SAVAGELYFE",font=font(FONTS["black"],72),fill=(255,255,255,255))
d.text((140,210),"B.G.S. ENTERTAINMENT • LIVE",font=font(FONTS["bold"],48),fill=(0,229,255,255))
d.ellipse([1150,150,1250,250],outline=(168,85,247,255),width=6)
d.text((1178,168),"B",font=font(FONTS["black"],64),fill=(255,255,255,255))
lt.save(os.path.join(OUT,"07_stream_lowerthird.png"))
print("07 ok")

# 8. VIDEO WATERMARK STATIC subtle
vw = Image.new("RGBA",(800,240),(0,0,0,0))
d = ImageDraw.Draw(vw)
d.text((20,20),"B.G.S.",font=font(FONTS["black"],130),fill=(255,255,255,90),stroke_width=2,stroke_fill=(255,255,255,40))
d.text((24,160),"BLU GIGGITY SAVAGELYFE",font=font(FONTS["bold"],40),fill=(255,255,255,70))
vw.save(os.path.join(OUT,"08_video_watermark_static.png"))
print("08 ok")

# 9. ANIMATED fade in/out - APNG + GIF, white subtle
frames=[]
for i in range(30):
    # sine fade 0..1..0
    import math as _m
    a = int(110*abs(_m.sin(_m.pi*i/30)))+10
    fr = Image.new("RGBA",(800,240),(0,0,0,0))
    df = ImageDraw.Draw(fr)
    df.text((20,20),"B.G.S.",font=font(FONTS["black"],130),fill=(255,255,255,a),stroke_width=2,stroke_fill=(255,255,255,max(0,a-50)))
    df.text((24,160),"BLU GIGGITY SAVAGELYFE",font=font(FONTS["bold"],40),fill=(255,255,255,max(0,a-20)))
    frames.append(fr)
frames[0].save(os.path.join(OUT,"09_video_watermark_fade.apng"),save_all=True,append_images=frames[1:],duration=100,loop=0)
frames[0].save(os.path.join(OUT,"09_video_watermark_fade.gif"),save_all=True,append_images=frames[1:],duration=100,loop=0,disposal=2)
print("09 ok")

# 10. CORNER stacked small 600x600
co = Image.new("RGBA",(600,600),(0,0,0,0))
d = ImageDraw.Draw(co)
# dark pill behind for legibility
d.rounded_rectangle([40,40,560,560],radius=36,fill=(0,0,0,120))
# drop shadow text via blur copy
t = Image.new("RGBA",(600,600),(0,0,0,0))
dt = ImageDraw.Draw(t)
center_text(dt,(300,200),"BGS",font(FONTS["black"],170),fill=(255,255,255,255))
t2 = t.filter(ImageFilter.GaussianBlur(6))
# actually composite
co = Image.alpha_composite(co, t2)
d = ImageDraw.Draw(co)
center_text(d,(300,195),"BGS",font(FONTS["black"],170),fill=(255,255,255,255),stroke_width=2,stroke_fill=(0,229,255,255))
center_text(d,(300,340),"BLU GIGGITY",font(FONTS["bold"],52),fill=(0,229,255,255))
center_text(d,(300,400),"SAVAGELYFE",font(FONTS["bold"],52),fill=(200,180,255,255))
center_text(d,(300,470),"ENTERTAINMENT",font(FONTS["regular"],36),fill=(255,255,255,200))
co.save(os.path.join(OUT,"10_corner_stacked.png"))
# tiny 256 version
co.resize((256,256),Image.LANCZOS).save(os.path.join(OUT,"10_corner_stacked_256.png"))
print("10 ok")

# 11. CHROME metallic
ch_size=(1920,640)
grad = chrome_gradient(ch_size)
mask = Image.new("L",ch_size,0)
dm = ImageDraw.Draw(mask)
dm.text((0,0),"BGS",font=font(FONTS["impact"],480),fill=255,stroke_width=4)
# center mask: compute bbox
bb = dm.textbbox((0,0),"BGS",font=font(FONTS["impact"],480),stroke_width=4)
tw,th = bb[2]-bb[0], bb[3]-bb[1]
mask2 = Image.new("L",ch_size,0)
dm2 = ImageDraw.Draw(mask2)
dm2.text((ch_size[0]//2-tw//2-bb[0],150-bb[1]),"BGS",font=font(FONTS["impact"],480),fill=255,stroke_width=4)
grad.putalpha(mask2)
ch = Image.new("RGBA",ch_size,(0,0,0,0))
ch = Image.alpha_composite(ch, grad)
d = ImageDraw.Draw(ch)
d.text((ch_size[0]//2-tw//2-bb[0],150-bb[1]),"BGS",font=font(FONTS["impact"],480),fill=(0,0,0,0),stroke_width=2,stroke_fill=(255,255,255,200))
# subtext
d2 = ImageDraw.Draw(ch)
center_text(d2,(960,540),"BLU GIGGITY SAVAGELYFE",font(FONTS["bold"],64),fill=(220,235,255,255))
ch.save(os.path.join(OUT,"11_chrome_metallic.png"))
print("11 ok")

# 12. OUTLINE + MINIMAL
om = Image.new("RGBA",(1920,640),(0,0,0,0))
d = ImageDraw.Draw(om)
center_text(d,(960,240),"B.G.S.",font(FONTS["bold"],280),fill=(0,0,0,0),stroke_width=4,stroke_fill=(255,255,255,255))
center_text(d,(960,480),"BLU GIGGITY SAVAGELYFE • MINIMAL",font(FONTS["mono"],52),fill=(255,255,255,200))
om.save(os.path.join(OUT,"12_outline_minimal.png"))
# 12b mono on dark pill
mp = Image.new("RGBA",(1920,400),(0,0,0,0))
d = ImageDraw.Draw(mp)
d.rounded_rectangle([200,60,1720,340],radius=20,fill=(0,0,0,180),outline=(255,255,255,120),width=2)
center_text(d,(960,170),"BGS | BLU GIGGITY SAVAGELYFE",font(FONTS["mono"],64),fill=(255,255,255,255))
center_text(d,(960,260),"TELEGRAM / MEWE / STREAM OVERLAY",font(FONTS["regular"],40),fill=(160,200,220,255))
mp.save(os.path.join(OUT,"12b_mono_stream.png"))
print("12 ok")

print("DONE ->", OUT)
