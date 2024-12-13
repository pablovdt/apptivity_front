import streamlit as st

from api.city_api import city_api
from api.organizer import organizer_api
from api.user_api import user_api

st.set_page_config(
    page_title="Apptivity - Organizadores",
    page_icon='images/APPTIVITY3.png',
    layout='centered',
    initial_sidebar_state="expanded"
)
from menu import login, authenticated_menu
from dotenv import load_dotenv
import os
import time
from streamlit_cookies_manager import EncryptedCookieManager

load_dotenv()


cookies = EncryptedCookieManager(prefix=os.getenv("APPTIVITY_COOKIES_PREFIX"),
                                 password=os.getenv("APPTIVITY_COOKIES_PASSWORD"))
while not cookies.ready():
    time.sleep(0.1)
user_id = cookies.get("session_uuid")

if user_id is None:
    login(cookies)
    st.stop()

if cookies['user_role'] != 'true':
    st.stop()

authenticated_menu(cookies)


if cookies['user_role'] != 'true':
    st.stop()


st.title("Organizadores")
st.write("Suscribete a un organizador para enterarte de todas sus actividades, independientemente de la categoría y de "
         "la distancia.")

st.subheader('Filtros:')

col1, col2, col3 = st.columns([2, 2, 2])
with col1:
    input_name = st.text_input('Nombre:')

with col3:
    cities: list = city_api.get_cities()
    cities_options = {"": ""}
    cities_options.update({city["name"]: city["id"] for city in cities})
    city_selected_name = st.selectbox("Selecciona un municipio", cities_options.keys())
    city_id = cities_options[city_selected_name]

organizers = organizer_api.get_organizers(name=input_name, city_id=city_id)
user_organizers = user_api.get_subscribe_organizers(user_id=cookies['user_id'])

for _ in range(3):
    st.write("")

if organizers:
    for organizer in organizers:
        with st.container(border=True):
            if organizer['id'] in [user_organizer['id'] for user_organizer in user_organizers]:
                st.markdown(f"<h1 style='color:#82b29a;'>{organizer['name']}</h1>", unsafe_allow_html=True)
            else:

                st.title(organizer['name'])

            municipio = city_api.get_city_by_id(organizer['city_id'])
            st.subheader(municipio['name'])
            st.write(organizer['description'])

            if st.button("Suscribirse", key=organizer['name']):
                if user_api.organizer_subscribe(organizer_id=organizer['id'], user_id=cookies['user_id']):
                    st.success(f"Genial, te has suscrito a {organizer['name']}")
                    st.rerun()
