import streamlit as st
from io import BytesIO
from datetime import datetime
import barcode
from barcode.writer import SVGWriter

st.set_page_config(page_title="Barcode SVG Clean", page_icon="🔧")
st.title("Barcode SVG leggibile")

value = st.text_input("Valore barcode", "")

if st.button("Genera SVG") and value.strip():
    try:
        code128 = barcode.get("code128", value.strip(), writer=SVGWriter())

        buffer = BytesIO()
        code128.write(
            buffer,
            {
                "module_width": 0.20,
                "module_height": 8,
                "font_size": 8,
                "text_distance": 3,
                "quiet_zone": 3,
            },
        )

        svg_data = buffer.getvalue()

        today_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"BARCODE_{value.strip()}_{today_str}.svg"

        st.download_button(
            "Scarica barcode (SVG)",
            data=svg_data,
            file_name=filename,
            mime="image/svg+xml",
        )

    except Exception as e:
        st.error(f"Errore nella generazione del barcode: {e}")

else:
    st.info("Inserisci un valore e premi 'Genera SVG'.")
