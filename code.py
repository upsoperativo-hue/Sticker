import streamlit as st
from io import BytesIO
from datetime import datetime
import barcode
from barcode.writer import ImageWriter

st.set_page_config(page_title="Barcode Zebra TXT", page_icon="📄")
st.title("Generatore Barcode TXT per Sticker Zebra (50×15 mm)")

st.write(
    "Inserisci il valore da codificare (tracking, bag ID, ecc.). "
    "Il barcode verrà generato come file TXT contenente la sequenza delle barre."
)

value = st.text_input("Valore barcode", "")

if st.button("Genera TXT") and value.strip():
    try:
        # Genera barcode Code128
        code128 = barcode.get("code128", value.strip(), writer=ImageWriter())

        # Ottieni pattern barre/spazi dal writer (sempre coppie)
        pattern = code128.writer._build(code128)

        # Converti in testo leggibile
        pattern_txt = "\n".join(
            [f"{'BAR' if b else 'SPACE'} - {w}" for b, w in pattern]
        )

        # Prepara il TXT per il download
        buffer_txt = BytesIO(pattern_txt.encode("utf-8"))

        today_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"BARCODE_{value.strip()}_{today_str}.txt"

        st.download_button(
            "Scarica barcode (TXT)",
            data=buffer_txt.getvalue(),
            file_name=filename,
            mime="text/plain",
        )

    except Exception as e:
        st.error(f"Errore nella generazione del barcode: {e}")

else:
    st.info("Inserisci un valore e premi 'Genera TXT'.")
