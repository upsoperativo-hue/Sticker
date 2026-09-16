import streamlit as st
from io import BytesIO

st.set_page_config(page_title="Barcode Zebra ZPL", page_icon="🏷️")
st.title("Generatore Barcode ZPL per Zebra (Sticker 50×15 mm)")

st.write(
    "Inserisci il valore da codificare. "
    "Il tool genera codice ZPL compatibile con tutte le stampanti Zebra."
)

value = st.text_input("Valore barcode", "")

def generate_zpl(value):
    return f"""
^XA
^PW400
^LL120
^FO20,10
^BY2,2,40
^BCN,40,Y,N,N
^FD{value}^FS
^XZ
"""

if st.button("Genera ZPL") and value.strip():
    zpl_code = generate_zpl(value.strip())

    st.code(zpl_code, language="text")

    buffer = BytesIO(zpl_code.encode("utf-8"))

    st.download_button(
        "Scarica file ZPL",
        data=buffer.getvalue(),
        file_name=f"BARCODE_{value.strip()}.zpl",
        mime="text/plain"
    )
else:
    st.info("Inserisci un valore e premi 'Genera ZPL'.")
