import streamlit as st

st.set_page_config(
    page_title="Apptivity - Configuración-",
    page_icon='images/APPTIVITY3.png',
    layout='centered',
    initial_sidebar_state="expanded"
)
from api.place_api import place_api
import pandas as pd
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

st.title("Añade nuevos lugares a tu municipio")

st.subheader("Lugares en tu municipio")

places_by_city = place_api.get_places_by_id(cookies['organizer_city_id'])

# Convertir a DataFrame
df_places = pd.DataFrame(places_by_city)

# Seleccionar columnas específicas
df_places = df_places[["name", "location_url"]]

# Cambiar nombres de las columnas
df_places = df_places.rename(columns={"name": "Nombre", "location_url": "URL de la ubicación"})

# Mostrar tabla sin índice
st.dataframe(df_places, hide_index=True, use_container_width=True)

for _ in range(3):
    st.write("")

st.subheader("¿Quieres añadir un nuevo lugar en tu municipio?")

new_place_name = st.text_input("Nombre")
coordinates = st.text_input("Coordenadas- Latitud, Longitud- ", help="Buscala en google maps. Copia y pega")
st.info("Para obtener la latitud y longitud de un lugar, en google maps, haz click derecho en el lugar en cuestión "
        "y verás algo similar a 42.55113680411345, -2.961769755589488")

coordinates = coordinates.replace(", ", ",")

new_place_ubication = f"https://www.google.com/maps?q={coordinates}"

if coordinates:
    st.subheader("Comprueba si es correcto y haz click en 'Añadir lugar'")
    st.write(new_place_ubication)

    if st.button("Añadir lugar"):

        if new_place_name and new_place_ubication:
            if place_api.insert_place(name=new_place_name, location=new_place_ubication,
                                      city_id=cookies['organizer_city_id']):
                st.success("Lugar añadido correctamente")
            else:
                st.error("Error. Intentelo de nuevo mas tarde.")
        else:
            st.warning("Debes rellenar todos los campos")
