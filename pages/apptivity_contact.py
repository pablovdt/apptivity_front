import streamlit as st

from api.place_api import place_api

st.set_page_config(
    page_title="Apptivity - Contacto -",
    page_icon='images/logotipo_apptivity3.png',
    layout='centered',
    initial_sidebar_state="expanded"
)
from menu import login, authenticated_menu

from dotenv import load_dotenv
import os
import time
from streamlit_cookies_manager import EncryptedCookieManager

import pandas as pd
import pydeck as pdk

load_dotenv()

cookies = EncryptedCookieManager(prefix=os.getenv("APPTIVITY_COOKIES_PREFIX"),
                                 password=os.getenv("APPTIVITY_COOKIES_PASSWORD"))
while not cookies.ready():
    time.sleep(0.1)
user_id = cookies.get("session_uuid")

if user_id is None:
    login(cookies)
    st.stop()


authenticated_menu(cookies)

st.image("images/logotipo_apptivity.png")

# Ficha de contacto
st.write("### Información de Contacto")

st.markdown("""
📍 **Dirección:** Calle Ejemplo 123, Ciudad, País  
📞 **Teléfono:** +34 123 456 789  
📧 **Correo Electrónico:** [apptivity@mail.com](mailto:apptivity@mail.com)  
🌐 **Página Web:** [www.apptivity.com](https://www.apptivity.com)
""")

st.write("### Envíanos un mensaje")
name = st.text_input("Nombre")
email = st.text_input("Correo Electrónico")
message = st.text_area("Mensaje")
if st.button("Enviar"):
    st.success(f"Gracias por contactarnos, {name}. Pronto responderemos a tu mensaje.")

