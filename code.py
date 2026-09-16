import streamlit as st
from io import BytesIO
from datetime import datetime
import barcode
from barcode.writer import SVGWriter

st.set_page_config(page_title="Barcode SVG Perfetto", page_icon="🔧")
st.title("Barcode SVG leggibile per sticker 50×15 mm")

value = st.text_input("Valore barcode", "")

if st.button("Genera SVG") and value.strip():
    try:
        code128 = barcode.get("code128", value.strip(), writer=SVGWriter())

        buffer = BytesIO()
        code128.write(
            buffer,
            {
                "module_width": 0.20,     # modulo minimo leggibile
                "module_height": 8,       # altezza barre
                "font_size": 8,
                "text_distance": 3,
                "quiet_zone": 3,          # margine bianco corretto
            },
        )

        svg = buffer.getvalue().decode("utf-8")

        # Inseriamo dimensioni fisiche SENZA ridefinire width/height
        # Aggiungiamo viewBox e lasciamo width/height originali
        svg = svg.replace(
            "<svg ",
            '<svg viewBox="0 0 400 120" width="50mm" height="15mm" preserveAspectRatio="xMidYMid meet" '
        )

        today_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"BARCODE_{value.strip()}_{today_str}.svg"

        st.download_button(
            "Scarica barcode (SVG leggibile)",
            data=svg.encode("utf-8"),
            file_name=filename,
            mime="image/svg+xml",
        )

    except Exception as e:
        st.error(f"Errore nella generazione del barcode: {e}")

else:
    st.info("Inserisci un valore e premi 'Genera SVG'.")
