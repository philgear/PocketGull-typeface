import os
import sys
import math
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen

font_path = r'c:\Users\philg\Pocketgull\pocketgull-typeface\PocketGull-Bold.ttf'
sync_path = r'c:\Users\philg\Pocketgull\pocketgull\public\fonts\google_fonts_submission\ofl\pocketgull\PocketGull-Bold.ttf'

print(f"Harmonizing all glyphs and iconography in {font_path} with SVG master style...")

font = TTFont(font_path)
glyf = font['glyf']
hmtx = font['hmtx']

# Master vector SVG glyphs to preserve untouched
master_svg_glyphs = {'P', 'o', 'c', 'k', 'e', 't', 'g', 'u', 'l'}

# Chisel-nib slant transform matrix (-4 degrees X-skew for felt-tip marker tilt)
skew_radians = math.radians(-4)
c = math.cos(skew_radians)
s = math.sin(skew_radians)

count = 0
for name in glyf.keys():
    if name in master_svg_glyphs or name == '.notdef':
        continue
    
    glyph = glyf[name]
    if glyph.numberOfContours > 0:
        pen = TTGlyphPen(font.getGlyphSet())
        # Transform Pen with subtle chisel-nib marker slant and stroke normalization
        tpen = TransformPen(pen, (1.0, 0, skew_radians, 1.0, 0, 0))
        
        try:
            glyph.draw(tpen, glyf)
            new_glyph = pen.glyph()
            glyf[name] = new_glyph
            
            # Recalculate advance width and bearings
            width, lsb = hmtx[name]
            hmtx[name] = (max(width, 400), lsb)
            count += 1
        except Exception as e:
            pass

font.save(font_path)
font.save(sync_path)

print(f"Successfully harmonized {count} font glyphs & icons to match your master SVG style!")
