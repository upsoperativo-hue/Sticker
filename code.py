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

# Parametri ridotti del 150%
DEFAULT_MODULE_WIDTH = 0.13
DEFAULT_MODULE_HEIGHT = 5

col1, col2 = st.columns(2)
with col1:
    module_width = st.number_input(
        "Spessore barre (module_width)",
        min_value=0.05,
        max_value=0.50,
        value=DEFAULT_MODULE_WIDTH,
        step=0.01
    )
with col2:
    module_height = st.number_input(
        "Altezza barre (module_height)",
        min_value=3,
        max_value=20,
        value=DEFAULT_MODULE_HEIGHT,
        step=1
    )

if st.button("Genera barcode") and value.strip():
    try:
        code128 = barcode.get("code128", value.strip(), writer=ImageWriter())

        buffer = BytesIO()
        code128.write(
            buffer,
            {
                "module_width": module_width,
                "module_height": module_height,
                "font_size": 5,        # ridotto del 150%
                "text_distance": 4,    # richiesto
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
