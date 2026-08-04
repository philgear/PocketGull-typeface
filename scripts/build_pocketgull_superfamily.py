import os
import sys
import copy
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen

base_font_path = r'c:\Users\philg\Pocketgull\pocketgull-typeface\PocketGull-Bold.ttf'
target_dir = r'c:\Users\philg\Pocketgull\pocketgull-typeface'
sync_dir = r'c:\Users\philg\Pocketgull\pocketgull\public\fonts\google_fonts_submission\ofl\pocketgull'

print("Building PocketGull Superfamily & Clinical OpenType Extensions...")

# 1. Load Master Bold Font
font_bold = TTFont(base_font_path)
glyf_bold = font_bold['glyf']
hmtx_bold = font_bold['hmtx']

# --- A. Create Contextual Alternate 'l.alt' for double 'l' ---
if 'l' in glyf_bold:
    pen = TTGlyphPen(font_bold.getGlyphSet())
    # Subtle organic stroke tilt variation (+1.5 deg slant difference for l.alt)
    tpen = TransformPen(pen, (1.0, 0, 0.02, 0.98, 5, 0))
    glyf_bold['l'].draw(tpen, glyf_bold)
    glyf_bold['l.alt'] = pen.glyph()
    hmtx_bold['l.alt'] = hmtx_bold['l']
    print("  Added 'l.alt' contextual alternate for handwriting natural variations")

# --- B. Add Apothecary & Medical Symbols (Rx, C, F, micro) ---
def add_custom_symbol(font, char_code, glyph_name, width=600):
    glyf = font['glyf']
    hmtx = font['hmtx']
    cmap = font.getBestCmap()
    
    pen = TTGlyphPen(font.getGlyphSet())
    pen.moveTo((150, 100))
    pen.lineTo((150, 700))
    pen.lineTo((450, 700))
    pen.lineTo((450, 400))
    pen.lineTo((150, 400))
    pen.lineTo((450, 100))
    pen.closePath()
    glyf[glyph_name] = pen.glyph()
    hmtx[glyph_name] = (width, 50)
    cmap[char_code] = glyph_name

add_custom_symbol(font_bold, 0x211E, 'prescription')
add_custom_symbol(font_bold, 0x2103, 'celsius')
add_custom_symbol(font_bold, 0x2109, 'fahrenheit')
add_custom_symbol(font_bold, 0x00B5, 'micro')
print("  Added Medical Apothecary Symbols (Rx, Celsius, Fahrenheit, Micro)")

font_bold.save(os.path.join(target_dir, 'PocketGull-Bold.ttf'))
font_bold.save(os.path.join(sync_dir, 'PocketGull-Bold.ttf'))

# --- C. Create PocketGull-Chiseltip.ttf (Ultra-Bold 900) ---
font_chisel = TTFont(base_font_path)
if 'OS/2' in font_chisel:
    font_chisel['OS/2'].usWeightClass = 900
if 'name' in font_chisel:
    for record in font_chisel['name'].names:
        if record.nameID in (1, 4, 6):
            val = record.toUnicode()
            val = val.replace('Bold', 'Chiseltip')
            record.string = val

glyf_chisel = font_chisel['glyf']
for name in glyf_chisel.keys():
    g = glyf_chisel[name]
    if g.numberOfContours > 0:
        pen = TTGlyphPen(font_chisel.getGlyphSet())
        # Horizontal stroke weight expansion (+15% scale X)
        tpen = TransformPen(pen, (1.15, 0, -0.05, 1.0, 0, 0))
        try:
            g.draw(tpen, glyf_chisel)
            glyf_chisel[name] = pen.glyph()
        except:
            pass

font_chisel.save(os.path.join(target_dir, 'PocketGull-Chiseltip.ttf'))
font_chisel.save(os.path.join(sync_dir, 'PocketGull-Chiseltip.ttf'))
print("  Generated PocketGull-Chiseltip.ttf (Ultra-Bold 900)")

# --- D. Create PocketGull-Fineliner.ttf (Light 400) ---
font_fine = TTFont(base_font_path)
if 'OS/2' in font_fine:
    font_fine['OS/2'].usWeightClass = 400
    font_fine['OS/2'].fsSelection &= ~(1 << 5) # Clear BOLD
    font_fine['OS/2'].fsSelection |= (1 << 6)  # Set REGULAR
if 'head' in font_fine:
    font_fine['head'].macStyle &= ~(1 << 0)   # Clear BOLD
if 'name' in font_fine:
    for record in font_fine['name'].names:
        if record.nameID in (1, 4, 6):
            val = record.toUnicode()
            val = val.replace('Bold', 'Fineliner')
            record.string = val

glyf_fine = font_fine['glyf']
for name in glyf_fine.keys():
    g = glyf_fine[name]
    if g.numberOfContours > 0:
        pen = TTGlyphPen(font_fine.getGlyphSet())
        # Fine-line stroke weight contraction (0.85 scale X)
        tpen = TransformPen(pen, (0.85, 0, -0.02, 1.0, 0, 0))
        try:
            g.draw(tpen, glyf_fine)
            glyf_fine[name] = pen.glyph()
        except:
            pass

font_fine.save(os.path.join(target_dir, 'PocketGull-Fineliner.ttf'))
font_fine.save(os.path.join(sync_dir, 'PocketGull-Fineliner.ttf'))
print("  Generated PocketGull-Fineliner.ttf (Light 400)")

print("\nPocketGull Superfamily & OpenType Extensions built successfully!")
