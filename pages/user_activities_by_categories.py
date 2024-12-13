import streamlit as st

st.set_page_config(
    page_title="Apptivity - Más Actividades -",
    page_icon='images/APPTIVITY3.png',
    layout='centered',
    initial_sidebar_state="expanded"
)
from menu import login, authenticated_menu
from api.city_api import city_api
import os
from streamlit_cookies_manager import EncryptedCookieManager
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime

from api.place_api import place_api
from api.user_api import user_api
import time
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

st.header(f"Más actividades", help="Estas actividades no se basan en tus categorias ni en tu distancia de notificacion")
st.write("¿Quieres conocer que más pasa en Apptivity?")

user_activities = user_api.get_more_activities(user_id=int(cookies['user_id']))

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

                if row['assistance']:
                    st.markdown(f"<h2 style='color: #82b29a'>{row['name']}</h2>", unsafe_allow_html=True)
                elif row['assistance'] is None:
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

                if st.button(f"Añadir actividad a Inicio",key=row['id']):
                    user_api.add_user_activity(user_id=cookies['user_id'], activity_id=row['id'])
                    st.rerun()

else:
    st.info("Aquí aparecerán actividades de todo Apptivity")
