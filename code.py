import streamlit as st
from io import BytesIO
from datetime import datetime
import barcode
from barcode.writer import ImageWriter
from PIL import Image

st.set_page_config(page_title="Barcode Zebra", page_icon="🏷️")
st.title("Generatore Barcode per Sticker Zebra (50×15 mm)")

st.write(
    "Inserisci il valore da codificare (tracking, bag ID, ecc.). "
    "Il barcode verrà generato in formato PNG, ottimizzato per etichette Zebra "
    "con area viva 50 mm × 15 mm."
)

value = st.text_input("Valore barcode", "")

# Parametri ridotti del 200%
DEFAULT_MODULE_WIDTH = 0.065
DEFAULT_MODULE_HEIGHT = 2.5

col1, col2 = st.columns(2)
with col1:
    module_width = st.number_input(
        "Spessore barre (module_width)",
        min_value=0.03,
        max_value=0.30,
        value=float(DEFAULT_MODULE_WIDTH),
        step=0.005
    )
with col2:
    module_height = st.number_input(
        "Altezza barre (module_height)",
        min_value=1.0,
        max_value=15.0,
        value=float(DEFAULT_MODULE_HEIGHT),
        step=0.5
    )

if st.button("Genera barcode") and value.strip():
    try:
        code128 = barcode.get("code128", value.strip(), writer=ImageWriter())

        buffer = BytesIO()
        code128.write(
            buffer,
            {
                "module_width": float(module_width),
                "module_height": float(module_height),
                "font_size": 3,        # ridotto del 200%
                "text_distance": 3,    # richiesto
                "quiet_zone": 1,       # minimo sicuro
            },
        )

        buffer.seek(0)
        img = Image.open(buffer).convert("RGB")

        st.image(img, caption=f"Barcode: {value.strip()}", use_container_width=False)

        today_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"BARCODE_{value.strip()}_{today_str}.png"

        st.download_button(
            "Scarica barcode (PNG)",
            data=buffer.getvalue(),
            file_name=filename,
            mime="image/png",
        )

    except Exception as e:
        st.error(f"Errore nella generazione del barcode: {e}")

else:
    st.info("Inserisci un valore e premi 'Genera barcode'.")
