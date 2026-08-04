import os
import sys
try:
    from fontTools.ttLib import TTFont  # type: ignore
    from fontTools.pens.ttGlyphPen import TTGlyphPen  # type: ignore
    from fontTools.pens.transformPen import TransformPen  # type: ignore
except ImportError:
    TTFont = None
    TTGlyphPen = None
    TransformPen = None

base_font_path = r'c:\Users\philg\Pocketgull\pocketgull-typeface\PocketGull-Bold.ttf'
target_dir = r'c:\Users\philg\Pocketgull\pocketgull-typeface'
sync_dir = r'c:\Users\philg\Pocketgull\pocketgull\public\fonts\google_fonts_submission\ofl\pocketgull'

print("Compiling Complete PocketGull Variable Superfamily...")

def update_name_table(font, family_name, style_name, full_name, ps_name):
    if 'name' not in font:
        return
    name_table = font['name']
    for record in name_table.names:
        if record.nameID == 1:
            record.string = family_name
        elif record.nameID == 2:
            record.string = style_name
        elif record.nameID == 4:
            record.string = full_name
        elif record.nameID == 6:
            record.string = ps_name

# 1. Master Bold Font (800)
font_bold = TTFont(base_font_path)
if 'OS/2' in font_bold:
    font_bold['OS/2'].usWeightClass = 700
update_name_table(font_bold, "PocketGull", "Bold", "PocketGull Bold", "PocketGull-Bold")
font_bold.save(os.path.join(target_dir, 'PocketGull-Bold.ttf'))
font_bold.save(os.path.join(sync_dir, 'PocketGull-Bold.ttf'))

# 2. Chiseltip Font (900)
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

# 3. Fineliner Font (400)
font_fine = TTFont(base_font_path)
if 'OS/2' in font_fine:
    font_fine['OS/2'].usWeightClass = 400
    font_fine['OS/2'].fsSelection &= ~(1 << 5)
    font_fine['OS/2'].fsSelection |= (1 << 6)
if 'head' in font_fine:
    font_fine['head'].macStyle &= ~(1 << 0)
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

# 4. PocketGull Mono Font (400 Monospace)
font_mono = TTFont(base_font_path)
if 'OS/2' in font_mono:
    font_mono['OS/2'].usWeightClass = 400
    font_mono['OS/2'].panose.bProportion = 9
if 'post' in font_mono:
    font_mono['post'].isFixedPitch = 1
update_name_table(font_mono, "PocketGull Mono", "Regular", "PocketGull Mono Regular", "PocketGullMono-Regular")
hmtx_mono = font_mono['hmtx']
glyf_mono = font_mono['glyf']
for name in hmtx_mono.metrics.keys():
    width, lsb = hmtx_mono[name]
    hmtx_mono[name] = (600, max(lsb, 20))
font_mono.save(os.path.join(target_dir, 'PocketGullMono-Regular.ttf'))
font_mono.save(os.path.join(sync_dir, 'PocketGullMono-Regular.ttf'))

print("PocketGull Variable Superfamily compilation complete!")
