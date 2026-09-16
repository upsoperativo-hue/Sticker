import streamlit as st
from io import BytesIO
from datetime import datetime

# -----------------------------
# TABELLA CODE128 (moduli)
# -----------------------------
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
    (2,1,1,4,1,2), # START A
    (2,1,1,2,1,4), # START B
    (2,1,1,2,3,2), # START C
    (2,3,3,1,1,1,2) # STOP
]

# -----------------------------
# Funzione Code128 AUTO
# -----------------------------
def encode_code128_auto(text):
    # START B (AUTO usa B come default)
    encoded = [104]

    # Converti ogni carattere
    for ch in text:
        encoded.append(ord(ch) - 32)

    # Checksum
    checksum = encoded[0]
    for i, v in enumerate(encoded[1:], 1):
        checksum += v * i
    checksum %= 103
    encoded.append(checksum)

    # STOP
    encoded.append(106)

    return encoded

# -----------------------------
# Generatore SVG
# -----------------------------
def generate_svg(text):
    encoded = encode_code128_auto(text)

    module_width_mm = 0.20
    quiet_zone_mm = 3
    height_mm = 12

    x = quiet_zone_mm
    rects = []

    for code in encoded:
        pattern = CODE128_TABLE[code]
        is_bar = True
        for width in pattern:
            w = width * module_width_mm
            if is_bar:
                rects.append(f'<rect x="{x}mm" y="0mm" width="{w}mm" height="{height_mm}mm" fill="black"/>')
            x += w
            is_bar = not is_bar

    total_width = x + quiet_zone_mm

    svg = f'''
<svg width="50mm" height="15mm" viewBox="0 0 {total_width} {height_mm+5}" xmlns="http://www.w3.org/2000/svg">
    {"".join(rects)}
    <text x="{total_width/2}" y="{height_mm+4}" font-size="4" text-anchor="middle">{text}</text>
</svg>
'''
    return svg

# -----------------------------
# STREAMLIT
# -----------------------------
st.set_page_config(page_title="Barcode SVG Professionale", page_icon="🔧")
st.title("Barcode Code128 AUTO (barre + testo)")

value = st.text_input("Valore barcode", "")

if st.button("Genera SVG") and value.strip():
    svg = generate_svg(value.strip())
    st.download_button(
        "Scarica barcode (SVG professionale)",
        data=svg.encode("utf-8"),
        file_name=f"BARCODE_{value.strip()}.svg",
        mime="image/svg+xml",
    )
else:
    st.info("Inserisci un valore e premi 'Genera SVG'.")
