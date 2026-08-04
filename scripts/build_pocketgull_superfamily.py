import os
import sys
import copy
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen

base_font_path = r'c:\Users\philg\Pocketgull\pocketgull-typeface\PocketGull-Bold.ttf'
target_dir = r'c:\Users\philg\Pocketgull\pocketgull-typeface'
sync_dir = r'c:\Users\philg\Pocketgull\pocketgull\public\fonts\google_fonts_submission\ofl\pocketgull'

print("Ensuring Precision: Setting OpenType Name Tables & Weight Classes...")

def update_name_table(font, family_name, style_name, full_name, ps_name):
    if 'name' not in font:
        return
    name_table = font['name']
    for record in name_table.names:
        if record.nameID == 1: # Family Name
            record.string = family_name
        elif record.nameID == 2: # SubFamily Name
            record.string = style_name
        elif record.nameID == 4: # Full Name
            record.string = full_name
        elif record.nameID == 6: # PostScript Name
            record.string = ps_name

# --- 1. Master Bold Font ---
font_bold = TTFont(base_font_path)
if 'OS/2' in font_bold:
    font_bold['OS/2'].usWeightClass = 700 # Standard Bold
update_name_table(font_bold, "PocketGull", "Bold", "PocketGull Bold", "PocketGull-Bold")

font_bold.save(os.path.join(target_dir, 'PocketGull-Bold.ttf'))
font_bold.save(os.path.join(sync_dir, 'PocketGull-Bold.ttf'))

# --- 2. Chiseltip Font (900 Black) ---
font_chisel = TTFont(base_font_path)
if 'OS/2' in font_chisel:
    font_chisel['OS/2'].usWeightClass = 900
update_name_table(font_chisel, "PocketGull", "Black", "PocketGull Chiseltip", "PocketGull-Chiseltip")

glyf_chisel = font_chisel['glyf']
for name in glyf_chisel.keys():
    g = glyf_chisel[name]
    if g.numberOfContours > 0:
        pen = TTGlyphPen(font_chisel.getGlyphSet())
        tpen = TransformPen(pen, (1.15, 0, -0.05, 1.0, 0, 0))
        try:
            g.draw(tpen, glyf_chisel)
            glyf_chisel[name] = pen.glyph()
        except:
            pass

font_chisel.save(os.path.join(target_dir, 'PocketGull-Chiseltip.ttf'))
font_chisel.save(os.path.join(sync_dir, 'PocketGull-Chiseltip.ttf'))

# --- 3. Fineliner Font (400 Regular) ---
font_fine = TTFont(base_font_path)
if 'OS/2' in font_fine:
    font_fine['OS/2'].usWeightClass = 400
    font_fine['OS/2'].fsSelection &= ~(1 << 5) # Clear BOLD
    font_fine['OS/2'].fsSelection |= (1 << 6)  # Set REGULAR
if 'head' in font_fine:
    font_fine['head'].macStyle &= ~(1 << 0)   # Clear BOLD
update_name_table(font_fine, "PocketGull", "Regular", "PocketGull Fineliner", "PocketGull-Fineliner")

glyf_fine = font_fine['glyf']
for name in glyf_fine.keys():
    g = glyf_fine[name]
    if g.numberOfContours > 0:
        pen = TTGlyphPen(font_fine.getGlyphSet())
        tpen = TransformPen(pen, (0.85, 0, -0.02, 1.0, 0, 0))
        try:
            g.draw(tpen, glyf_fine)
            glyf_fine[name] = pen.glyph()
        except:
            pass

font_fine.save(os.path.join(target_dir, 'PocketGull-Fineliner.ttf'))
font_fine.save(os.path.join(sync_dir, 'PocketGull-Fineliner.ttf'))

print("All OpenType name records and weight classes updated with exact precision.")
