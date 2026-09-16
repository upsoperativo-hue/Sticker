import streamlit as st
from io import BytesIO
from datetime import datetime
import barcode
from barcode.writer import ImageWriter

st.set_page_config(page_title="Barcode Zebra TXT (bits)", page_icon="📄")
st.title("Generatore Barcode TXT (sequenza di barre 1/0)")

st.write(
    "Inserisci il valore da codificare (tracking, bag ID, ecc.). "
    "Il barcode verrà generato come file TXT contenente la sequenza di bit "
    "(1 = barra, 0 = spazio)."
)

value = st.text_input("Valore barcode", "")

if st.button("Genera TXT") and value.strip():
    try:
        # Genera barcode Code128
        code128 = barcode.get("code128", value.strip(), writer=ImageWriter())

        # Pattern interno del barcode
        pattern = code128.build()

        bits = []

        # Converti pattern in sequenza di 1/0
        for item in pattern:
            # item può essere una tupla o struttura più complessa:
            # prendiamo i primi due elementi come (is_bar, width)
            try:
                is_bar = bool(item[0])
                width = int(item[1])
                bits.append(("1" if is_bar else "0") * width)
            except Exception:
                # Se non è nel formato atteso, lo ignoriamo
                continue

        bit_string = "".join(bits)

        buffer_txt = BytesIO(bit_string.encode("utf-8"))

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
