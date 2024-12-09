import streamlit as st

st.set_page_config(
    page_title="Apptivity",
    page_icon='images/logotipo_apptivity3.png',
    layout='centered',
    initial_sidebar_state="expanded"
)
import pytz
from menu import login, authenticated_menu
import os
from streamlit_cookies_manager import EncryptedCookieManager
from api.city_api import city_api

from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
from api.category_api import category_api
from api.place_api import place_api
from api.user_api import user_api

load_dotenv()
import time

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


@st.dialog("Actividad Actualizada")
def show_update_activity(activity):
    st.write(f"La actividad **{activity['name']}** ha sido actualizada.")
    if st.button("Aceptar"):
        user_api.post_activity_updated_confirmed(user_id=cookies['user_id'], activity_id=activity['activity_id'],
                                                 updated_confirmed=True)
        st.rerun()


activities_updated = user_api.get_activities_updated(user_id=cookies['user_id'])

if activities_updated:
    for activity_updated in activities_updated:
        show_update_activity(activity_updated)


def get_user_rural_level(value):
    if 0 <= value <= 20:
        return "Novato Rural"
    elif 21 <= value <= 40:
        return "Explorador Rural"
    elif 41 <= value <= 60:
        return "Productor Rural"
    elif 61 <= value <= 80:
        return "Agricultor Experto"
    elif 81 <= value <= 100:
        return "Líder Rural"
    elif 101 <= value <= 120:
        return "Maestro Rural"
    else:
        return "Valor fuera de rango"


user_rural_levels = {
    "Novato Rural": "Usuario que está comenzando su experiencia rural, explorando los aspectos más básicos.",
    "Explorador Rural": "Usuario que ha comenzado a familiarizarse con los aspectos rurales y busca más interacción.",
    "Productor Rural": "Usuario con conocimientos básicos y experiencia en la producción agrícola y actividades rurales.",
    "Agricultor Experto": "Usuario avanzado, con habilidades y conocimientos en la agricultura y la vida rural.",
    "Líder Rural": "Usuario líder en el ámbito rural, capaz de influir y organizar actividades y proyectos rurales.",
    "Maestro Rural": "Usuario con dominio total de los aspectos rurales, experto en todos los campos relacionados con el área rural."
}




user_level_value = user_api.get_user_assistances(user_id=int(cookies['user_id']))

user_level = get_user_rural_level(user_level_value)
col1, _, col2 = st.columns([4,3, 1])

with col1:
    st.subheader(f"Nivel: {user_level}")
with col2:
    st.metric("Puntos", value=user_level_value)


st.header(f"{cookies['user_name']}, tus actividades")
user_activities = user_api.get_user_activities(cookies['user_id'], all=False,
                                               date_from=datetime.now(pytz.timezone("Europe/Madrid")).strftime(
                                                   "%Y-%m-%d"))


@st.dialog("Información")
def show_activity_details(item):
    st.write(f"🎟️ **Actividad: {item['name']}**")
    place = place_api.get_place_by_id(item["place_id"])
    st.write(f'📍 **Lugar:** [{place["name"]}]({place["location_url"]})')

    st.write(f"♜ **Organizador**: {item['organizer_name']}")
    date_obj = datetime.fromisoformat(item['date'])
    st.write(f"📅 **Fecha**: {date_obj.strftime('%A, %d de %B de %Y')}")
    st.write(f"🕒 **Hora**: {date_obj.strftime('%H:%M:%S')}")
    st.write(f"💰 **Precio**: {item['price']} €")

    st.write(f"📝 **Descripción**: {item['description']}")

    category = category_api.get_category_by_id(item['category_id'])['name']
    st.write(f"🏷️ **Categoría**: {category}")

    if item['cancelled']:
        st.write(f"🚫 **CANCELADA!!**", color='red')

    st.image(item['image_path'], use_column_width=True)

    col_button_1, col_button_2, col_button_3 = st.columns([2, 2, 2])

    with col_button_1:
        if st.button("Asistiré"):
            if user_api.update_possible_assistance(user_id=cookies['user_id'], activity_id=item['id'],
                                                   possible_assistance=True):
                st.rerun()

    with col_button_2:

        if st.button("No lo sé"):
            if user_api.update_possible_assistance(user_id=cookies['user_id'], activity_id=item['id'],
                                                   possible_assistance=None):
                st.rerun()

    with col_button_3:
        if st.button("No Asistiré"):
            if user_api.update_possible_assistance(user_id=cookies['user_id'], activity_id=item['id'],
                                                   possible_assistance=False):
                st.rerun()



if user_activities:
    df = pd.DataFrame(user_activities)

    df_sorted = df.sort_values(by='date', ascending=True)

    col1, col2 = st.columns(2)

    for i, (index, row) in enumerate(df_sorted.iterrows()):
        if i % 2 == 0:
            col = col1
        else:
            col = col2

        with col:

            with st.container(border=True):

                if row['possible_assistance']:
                    st.markdown(f"<h2 style='color: #82b29a'>{row['name']}</h2>", unsafe_allow_html=True)
                elif row['possible_assistance'] is None:
                    st.markdown(f"<h2>{row['name']}</h2>", unsafe_allow_html=True)

                place = place_api.get_place_by_id(row["place_id"])
                place_city_id = place["city_id"]

                city_name = city_api.get_city_by_id(place_city_id)['name']

                st.write(city_name)

                date_obj = datetime.fromisoformat(row['date'])
                st.write(f"📅 {date_obj.strftime('%d/%m/%Y')} 🕒 {date_obj.strftime('%H:%M')}")

                st.write(f"💰 {row['price']} €")

                if row.get('image_path'):
                    st.image(row['image_path'], use_column_width=True)

                if st.button(f"Ver actividad - {row['name']}", key=index):
                    show_activity_details(row)


else:
    st.info("Aquí aparecerán tus actividades")
