import streamlit as st

from api.place_api import place_api

st.set_page_config(
    page_title="Apptivity - Configuración-",
    page_icon='images/logotipo_apptivity3.png',
    layout='centered',
    initial_sidebar_state="expanded"
)
from menu import login, authenticated_menu
from collections import Counter
from api.organizer import organizer_api

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

if cookies['organizer_role'] != 'true':
    st.stop()

authenticated_menu(cookies)

st.title("Configuración")

st.subheader("Lugares en tu ciudad")

places_by_city = place_api.get_places_by_id(cookies['organizer_city_id'])

for place in places_by_city:
    st.write(place['name'])


st.subheader("¿Quieres añadir un nuevo lugar en tu ciudad?")

new_place_name = st.text_input("Nombre")
coordinates = st.text_input("Coordenadas- Latitud, Longitud- ", help="Buscala en google maps. Copia y pega")
st.info("Para obtener la latitud y longitud de un lugar, en google maps, haz click derecho en el lugar en cuestión "
        "y verás algo similar a 42.55113680411345, -2.961769755589488")

new_place_ubication = f"https://www.google.com/maps?q={coordinates}"

if st.button("Añadir lugar"):

    if new_place_name and new_place_ubication:
        if place_api.insert_place(name=new_place_name, location=new_place_ubication, city_id=cookies['organizer_city_id']):
            st.success("Lugar añadido correctamente")
        else:
            st.error("Error. Intentelo de nuevo mas tarde.")
    else:
        st.warning("Debes rellenar todos los campos")