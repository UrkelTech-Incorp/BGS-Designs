# BGS-Designs — Watermark Pack

Watermark + logo pack for **BGS / Blu Giggity Savagelyfe Entertainment**.

All transparent PNGs (plus JPG social exports, GIF/APNG animated fade) in this folder root.

## Files

| File | Use |
|---|---|
| `01_neon_blue_purple.png` | Neon style — blue/purple glow promo lettering (1920×640) |
| `02_signature_script.png` | Signature style — handwritten script, personal creator ID |
| `02b_signature_hand.png` | Alt hand style (Mistral / Ink Free) |
| `03_circular_badge.png` | Circular badge — stacked text, avatar/stamp (1200×1200) |
| `04_rectangular_badge.png` | Rectangular badge — clean bordered lockup |
| `05_social_profile_1080.png/.jpg` | Social profile — Telegram / MeWe avatar safe (1080×1080) |
| `06_social_banner_1920x480.png/.jpg` | Social banner — channel / stream header |
| `07_stream_lowerthird.png` | Streaming / broadcasting lower-third overlay (OBS, vMix, Meld) |
| `08_video_watermark_static.png` | Subtle static video watermark (~35% opacity) |
| `09_video_watermark_fade.gif/.apng` | Animated video watermark — fades in/out, loop |
| `10_corner_stacked.png` / `10_corner_stacked_256.png` | Corner watermark — small stacked logo, bottom-right |
| `11_chrome_metallic.png` | Chrome/metallic typography variant |
| `12_outline_minimal.png` | Outline/minimal variant |
| `12b_mono_stream.png` | Mono stream pill overlay |

## Usage

**OBS / Streamlabs / Meld / vMix:** add Image source → pick `07`, `08`, or `10_corner_stacked.png` → snap bottom-right, 15–25% scale, 80–90% opacity.

**Animated fade (CSS/OBS Browser source):**
```css
.watermark { animation: wmfade 6s ease-in-out infinite; }
@keyframes wmfade { 0%,100% {opacity:0} 15%,75% {opacity:.85} }
```

**ffmpeg burn-in (corner):**
```bash
ffmpeg -i input.mp4 -i 10_corner_stacked_256.png \
 -filter_complex "overlay=W-w-40:H-h-40:format=auto" -c:a copy output.mp4
```

**Telegram / MeWe:** use `05_social_profile_1080` as group avatar, `06_social_banner_1920x480` as channel header.

## Regenerate

```bash
python generate_watermarks.py
```

Requires Python + Pillow. Uses built-in Windows fonts (Arial Black, Impact, Pristina, Mistral, Ink Free, Gabriola).
