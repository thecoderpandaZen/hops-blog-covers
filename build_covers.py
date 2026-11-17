"""Render Hops blog covers from the two existing blog cover templates.

Downloads the published Enterprise (plain) and RFP (ribbon) covers from the
Sanity CDN and the PP Mori font from hops.ai at build time, replaces the title,
and writes 1097x731 PNGs to covers/. Nothing licensed is stored in this repo.
"""
import io, os, urllib.request
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

PLAIN = "https://cdn.sanity.io/images/4df4uwm2/production/16228e1eb398f002aa88b0d0f41324b8d171f6f7-1097x731.webp"
RIBBON = "https://cdn.sanity.io/images/4df4uwm2/production/e2a865a0a5eeaa8aa22818502cb0111545ea7988-1097x731.png"
FONT = "https://www.hops.ai/_next/static/immutable/media/PPMori_VariableUpright-s.p.3765a5tm6-g7r.woff2"
D = (22, 36, 60)      # title ink, sampled from the templates
H = (88, 106, 136)    # highlighted phrase, sampled from the templates

COVERS = {
    "ai-teammate-vs-ai-assistant": ("plain", [[("AI Teammate", H), (" vs", D)], [("AI Assistant", D)]]),
    "ai-agent-vs-workflow-automation": ("ribbon", [[("AI Agent vs ", D), ("Workflow", H)], [("Automation", H)]]),
    "collaborative-ai": ("plain", [[("What Is ", D), ("Collaborative AI?", H)], [("Put It to Work", D)]]),
    "ai-agent-approval": ("ribbon", [[("Should an ", D), ("AI Agent", H), (" Ask", D)], [("Before It Acts?", D)]]),
    "ai-agent-cost-for-teams": ("plain", [[("How Much Does an", D)], [("AI Agent", H), (" Cost a Team?", D)]]),
    "relevance-ai-alternatives": ("ribbon", [[("8 ", D), ("Relevance AI", H)], [("Alternatives", D)]]),
}

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=60).read()

def main():
    os.makedirs("covers", exist_ok=True)
    font = TTFont(io.BytesIO(get(FONT)))
    font.flavor = None
    font.save("/tmp/mori.ttf")
    f = ImageFont.truetype("/tmp/mori.ttf", 64)
    f.set_variation_by_axes([600])
    bases = {"plain": get(PLAIN), "ribbon": get(RIBBON)}
    for slug, (kind, lines) in COVERS.items():
        im = Image.open(io.BytesIO(bases[kind])).convert("RGB")
        dr = ImageDraw.Draw(im)
        dr.rectangle((95, 280, 1000, 450 if kind == "plain" else 436), fill=im.getpixel((60, 250)))
        for i, line in enumerate(lines):
            x, y = 106, 343 + 80 * i
            for text, color in line:
                dr.text((x, y), text, font=f, fill=color, anchor="ls")
                x += dr.textlength(text, font=f)
        im.save(f"covers/{slug}.png", optimize=True)
        print("wrote", slug)

if __name__ == "__main__":
    main()
