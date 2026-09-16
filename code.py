import streamlit as st
from io import BytesIO
from datetime import datetime

CODE128_TABLE = [
    (2,1,2,2,2,2), (2,2,2,1,2,2), (2,2,2,2,2,1), (1,2,1,2,2,3),
    (1,2,1,3,2,2), (1,3,1,2,2,2), (1,2,2,2,1,3), (1,2,2,3,1,2),
    (1,3,2,2,1,2), (2,2,1,2,1,3), (2,2,1,3,1,2), (2,3,1,2,1,2),
    (1,1,2,2,3,2), (1,2,2,1,3,2), (1,2,2,2,3,1), (1,1,3,2,2,2),
    (1,2,3,1,2,2), (1,2,3,2,2,1), (2,2,3,2,1,1), (2,2,1,1,3,2),
    (2,2,1,2,3,1), (2,1,3,2,1,2), (2,2,3,1,1,2), (3,1,2,1,3,1),
    (3,1,1,2,2,2), (3,2,1,1,2,2), (3,2,1,2,2,1), (3,1,2,2,1,2),
    (3,2,2,1,1,2), (3,2,2,2,1,1), (2,1,2,1,2,3), (2,1,2,3,2,1),
    (2,3,2,1,2,1), (1,1,1,3,2,3), (1,3,1,1,2,3), (1,3,1,3,2,1),
    (1,1,2,3,1,3), (1,3,2,1,1,3), (1,3,2,3,1,1), (2,1,1,3,1,3),
    (2,3,1,1,1,3), (2,3,1,3,1,1), (1,1,2,1,3,3), (1,1,2,3,3,1),
    (1,3,2,1,3,1), (1,1,3,1,2,3), (1,1,3,3,2,1), (1,3,3,1,2,1),
    (3,1,3,1,2,1), (2,1,1,3,3,1), (2,3,1,1,3,1), (2,1,3,1,1,3),
    (2,1,3,3,1,1), (2,1,3,1,3,1), (3,1,1,1,2,3), (3,1,1,3,2,1),
    (3,3,1,1,2,1), (3,1,2,1,1,3), (3,1,2,3,1,1), (3,3,2,1,1,1),
    (3,1,4,1,1,1), (2,2,1,4,1,1), (4,3,1,1,1,1), (1,1,1,2,2,4),
    (1,1,1,4,2,2), (1,2,1,1,2,4), (1,2,1,4,2,1), (1,4,1,1,2,2),
    (1,4,1,2,2,1), (1,1,2,2,1,4), (1,1,2,4,1,2), (1,2,2,1,1,4),
    (1,2,2,4,1,1), (1,4,2,1,1,2), (1,4,2,2,1,1), (2,4,1,2,1,1),
    (2,2,1,1,1,4), (4,1,3,1,1,1), (2,4,1,1,1,2), (1,3,4,1,1,1),
    (1,1,1,2,4,2), (1,2,1,1,4,2), (1,2,1,2,4,1), (1,1,4,2,1,2),
    (1,2,4,1,1,2), (1,2,4,2,1,1), (4,1,1,2,1,2), (4,2,1,1,1,2),
    (4,2,1,2,1,1), (2,1,2,1,4,1), (2,1,4,1,2,1), (4,1,2,1,2,1),
    (1,1,1,1,4,3), (1,1,1,3,4,1), (1,3,1,1,4,1), (1,1,4,1,1,3),
    (1,1,4,3,1,1), (4,1,1,1,1,3), (4,1,1,3,1,1), (1,1,3,1,4,1),
    (1,1,4,1,3,1), (3,1,1,1,4,1), (4,1,1,1,3,1),
    (2,1,1,4,1,2), # 103 START A
    (2,1,1,2,1,4), # 104 START B
    (2,1,1,2,3,2), # 105 START C
    (2,3,3,1,1,1,2) # 106 STOP
]

def encode_code128_auto(text):
    encoded = [104]  # START B
    for ch in text:
        encoded.append(ord(ch) - 32)
    checksum = encoded[0]
    for i, v in enumerate(encoded[1:], 1):
        checksum += v * i
    checksum %= 103
    encoded.append(checksum)
    encoded.append(106)  # STOP
    return encoded

def generate_svg(text):
    encoded = encode_code128_auto(text)

    quiet_zone_mm = 3.0
    height_mm = 10.0  # barre
    sticker_width_mm = 50.0
    sticker_height_mm = 15.0

    # prima calcolo la larghezza totale in "moduli"
    total_modules = 0
    for code in encoded:
        pattern = CODE128_TABLE[code]
        total_modules += sum(pattern)
    # STOP ha 13 moduli, ma l’abbiamo già incluso nella tabella

    # spazio utile per barre (senza quiet zone)
    usable_width_mm = sticker_width_mm - 2 * quiet_zone_mm
    module_width_mm = usable_width_mm / total_modules

    x = quiet_zone_mm
    rects = []

    for code in encoded:
        pattern = CODE128_TABLE[code]
        is_bar = True
        for width in pattern:
            w = width * module_width_mm
            if is_bar:
                rects.append(
                    f'<rect x="{x}mm" y="2mm" width="{w}mm" height="{height_mm}mm" fill="black"/>'
                )
            x += w
            is_bar = not is_bar

    svg = f'''
<svg width="{sticker_width_mm}mm" height="{sticker_height_mm}mm"
     viewBox="0 0 {sticker_width_mm} {sticker_height_mm}"
     xmlns="http://www.w3.org/2000/svg">
    {"".join(rects)}
    <text x="{sticker_width_mm/2}" y="{height_mm+4}" font-size="4"
          text-anchor="middle">{text}</text>
</svg>
'''
    return svg

# STREAMLIT
st.set_page_config(page_title="Barcode SVG 50x15", page_icon="🔧")
st.title("Barcode Code128 AUTO (barre + testo, 50×15 mm)")

value = st.text_input("Valore barcode", "")

if st.button("Genera SVG") and value.strip():
    svg = generate_svg(value.strip())
    st.download_button(
        "Scarica barcode (SVG 50×15)",
        data=svg.encode("utf-8"),
        file_name=f"BARCODE_{value.strip()}.svg",
        mime="image/svg+xml",
    )
else:
    st.info("Inserisci un valore e premi 'Genera SVG'.")
