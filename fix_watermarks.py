#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, math
OUT = r"C:\Users\Blu\Downloads\BGS Designs"
F = r"C:\Windows\Fonts"
def font(p,s): return ImageFont.truetype(os.path.join(F,p),s)
def center(draw, xy, text, f, **kw):
    bb = draw.textbbox((0,0), text, font=f, stroke_width=kw.get("stroke_width",0))
    w=bb[2]-bb[0]; h=bb[3]-bb[1]
    draw.text((xy[0]-w/2-bb[0], xy[1]-h/2-bb[1]), text, font=f, **kw)

def curved_top(base, cx, cy, radius, text, f, fill):
    d = ImageDraw.Draw(base)
    widths=[]
    for ch in text:
        bb=d.textbbox((0,0),ch,font=f); widths.append(bb[2]-bb[0]+10)
    total=sum(widths); arc=total/radius
    a=-math.pi/2-arc/2
    for ch,w in zip(text,widths):
        theta=a+(w/2)/radius
        x=cx+radius*math.cos(theta); y=cy+radius*math.sin(theta)
        rot=math.degrees(theta)+90
        bb=d.textbbox((0,0),ch,font=f); cw=bb[2]-bb[0]+30; chh=bb[3]-bb[1]+30
        tmp=Image.new("RGBA",(cw+30,chh+30),(0,0,0,0)); td=ImageDraw.Draw(tmp)
        td.text((20-bb[0],20-bb[1]),ch,font=f,fill=fill)
        tmp=tmp.rotate(-rot,resample=Image.BICUBIC,expand=True)
        base.alpha_composite(tmp,(int(x-tmp.width/2),int(y-tmp.height/2)))
        a+=w/radius
    return base

def curved_bottom(base, cx, cy, radius, text, f, fill):
    d = ImageDraw.Draw(base)
    widths=[]
    for ch in text:
        bb=d.textbbox((0,0),ch,font=f); widths.append(bb[2]-bb[0]+10)
    total=sum(widths); arc=total/radius
    a=math.pi/2+arc/2
    for ch,w in zip(text,widths):
        theta=a-(w/2)/radius
        x=cx+radius*math.cos(theta); y=cy+radius*math.sin(theta)
        rot=math.degrees(theta)-90
        bb=d.textbbox((0,0),ch,font=f); cw=bb[2]-bb[0]+30; chh=bb[3]-bb[1]+30
        tmp=Image.new("RGBA",(cw+30,chh+30),(0,0,0,0)); td=ImageDraw.Draw(tmp)
        td.text((20-bb[0],20-bb[1]),ch,font=f,fill=fill)
        tmp=tmp.rotate(-rot,resample=Image.BICUBIC,expand=True)
        base.alpha_composite(tmp,(int(x-tmp.width/2),int(y-tmp.height/2)))
        a-=w/radius
    return base

# --- 03 circular badge fixed ---
cb=Image.new("RGBA",(1200,1200),(0,0,0,0))
d=ImageDraw.Draw(cb); cx=cy=600
d.ellipse([60,60,1140,1140],outline=(255,255,255,255),width=10)
d.ellipse([110,110,1090,1090],outline=(0,229,255,255),width=4)
d.ellipse([180,180,1020,1020],outline=(255,255,255,140),width=2)
cb=curved_top(cb,cx,cy,430,"BLU GIGGITY",font("ariblk.ttf",84),(255,255,255,255))
cb=curved_bottom(cb,cx,cy,430,"SAVAGELYFE",font("ariblk.ttf",84),(0,229,255,255))
d=ImageDraw.Draw(cb)
center(d,(600,540),"BGS",font("ariblk.ttf",300),fill=(255,255,255,255),stroke_width=3,stroke_fill=(0,229,255,255))
center(d,(600,730),"- EST - ENTERTAINMENT -",font("arialbd.ttf",44),fill=(200,225,255,255))
center(d,(215,600),"o",font("arialbd.ttf",50),fill=(0,229,255,255))
center(d,(985,600),"o",font("arialbd.ttf",50),fill=(168,85,247,255))
cb.save(os.path.join(OUT,"03_circular_badge.png"))
print("03 fixed")

# --- 05 social profile fixed (no crop) ---
sp=Image.new("RGBA",(1080,1080),(10,12,28,255))
glow=Image.new("RGBA",(1080,1080),(0,0,0,0))
dg=ImageDraw.Draw(glow); dg.ellipse([140,140,940,940],fill=(30,60,140,255))
glow=glow.filter(ImageFilter.GaussianBlur(80))
sp=Image.alpha_composite(sp,glow)
d=ImageDraw.Draw(sp)
d.ellipse([90,90,990,990],outline=(0,229,255,255),width=10)
center(d,(540,450),"BGS",font("ariblk.ttf",250),fill=(255,255,255,255))
center(d,(540,680),"BLU GIGGITY",font("arialbd.ttf",66),fill=(0,229,255,255))
center(d,(540,760),"SAVAGELYFE",font("arialbd.ttf",66),fill=(168,85,247,255))
center(d,(540,850),"ENTERTAINMENT",font("arial.ttf",40),fill=(200,220,255,255))
sp.convert("RGB").save(os.path.join(OUT,"05_social_profile_1080.jpg"),quality=92)
sp.save(os.path.join(OUT,"05_social_profile_1080.png"))
print("05 fixed")

# --- 07 lower third fixed ---
lt=Image.new("RGBA",(1920,400),(0,0,0,0))
d=ImageDraw.Draw(lt)
d.rounded_rectangle([60,80,1380,320],radius=24,fill=(0,0,0,175),outline=(0,229,255,255),width=4)
d.rectangle([60,80,92,320],fill=(0,229,255,255))
d.text((140,125),"BLU GIGGITY SAVAGELYFE",font=font("ariblk.ttf",60),fill=(255,255,255,255))
d.text((140,215),"B.G.S. ENTERTAINMENT - LIVE",font=font("arialbd.ttf",42),fill=(0,229,255,255))
d.ellipse([1440,130,1580,270],outline=(168,85,247,255),width=6)
db=d.textbbox((0,0),"B",font=font("ariblk.ttf",64))
d.text((1510-(db[2]-db[0])//2,160),"B",font=font("ariblk.ttf",64),fill=(255,255,255,255))
lt.save(os.path.join(OUT,"07_stream_lowerthird.png"))
print("07 fixed")

# --- 11 chrome fixed ---
size=(1920,640)
stops=[(8,20,60),(60,120,200),(210,230,255),(255,255,255),(150,140,255),(30,50,140)]
grad=Image.new("RGBA",size,(0,0,0,0)); px=grad.load(); h=size[1]
for y in range(h):
    t=y/h*(len(stops)-1); i=int(t); fr=t-i
    c=stops[-1] if i>=len(stops)-1 else tuple(int(stops[i][j]*(1-fr)+stops[i+1][j]*fr) for j in range(3))
    for x in range(size[0]): px[x,y]=c+(255,)
fb=font("impact.ttf",400)
tmpd=ImageDraw.Draw(Image.new("RGBA",(10,10)))
bb=tmpd.textbbox((0,0),"BGS",font=fb,stroke_width=3)
tw,th=bb[2]-bb[0],bb[3]-bb[1]
tx=size[0]//2-tw//2-bb[0]; ty=60-bb[1]
mask=Image.new("L",size,0); dm=ImageDraw.Draw(mask)
dm.text((tx,ty),"BGS",font=fb,fill=255,stroke_width=3)
grad.putalpha(mask)
ch=Image.new("RGBA",size,(0,0,0,0)); ch=Image.alpha_composite(ch,grad)
d=ImageDraw.Draw(ch)
d.text((tx,ty),"BGS",font=fb,fill=(0,0,0,0),stroke_width=3,stroke_fill=(255,255,255,230))
center(d,(960,500),"BLU GIGGITY SAVAGELYFE",font("arialbd.ttf",62),fill=(220,235,255,255))
ch.save(os.path.join(OUT,"11_chrome_metallic.png"))
print("11 fixed")
