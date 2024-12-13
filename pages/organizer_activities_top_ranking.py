import streamlit as st

st.set_page_config(
    page_title="Apptivity - Top Ranking-",
    page_icon='images/APPTIVITY3.png',
    layout='centered',
    initial_sidebar_state="expanded"
)
from menu import login, authenticated_menu
from datetime import datetime
import pytz

now = datetime.now(pytz.timezone("Europe/Madrid"))
from api.activity_api import activiti_api

from api.place_api import place_api
from api.user_api import user_api
from api.city_api import city_api

from dotenv import load_dotenv
import os
import time
from streamlit_cookies_manager import EncryptedCookieManager
import pandas as pd

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

organizer_activities = activiti_api.get_activities(organizer_id=cookies['organizer_id'],
                                                   date_from=datetime.now(pytz.timezone("Europe/Madrid")).strftime("%Y-%m-%d"), cancelled=False,
                                                   order_by_assistance=True)

general_activities = activiti_api.get_activities(date_from=datetime.now(pytz.timezone("Europe/Madrid")).strftime("%Y-%m-%d"), cancelled=False,
                                                 order_by_assistance=True, limit=10)

st.title("Actividades Destacadas")

organizer_tab, general_tab = st.tabs([f"Destacadas {cookies['organizer_name']}", "Destacadas Otros"])

with organizer_tab:
    for _ in range(3):
        st.write("")

    if organizer_activities:

        st.subheader("Tus Destacadas")

        st.markdown(f"""
        ¡Descubre las actividades creadas por {cookies['organizer_name']} que están atrayendo a más personas!
        """)

        df = pd.DataFrame(organizer_activities)

        for i, (index, row) in enumerate(df.iterrows()):

            with st.container(border=True):

                st.markdown(f"<h2>{row['name']}</h2>", unsafe_allow_html=True)

                place = place_api.get_place_by_id(row["place_id"])
                place_city_id = place["city_id"]

                city_name = city_api.get_city_by_id(place_city_id)['name']

                st.write(city_name)

                date_obj = datetime.fromisoformat(row['date'])
                st.write(f"📅 {date_obj.strftime('%d/%m/%Y')} 🕒 {date_obj.strftime('%H:%M')}")

                st.write(f"💰 {row['price']} €")

                st.metric(label=f"👥 **Asistiré:**", value=f"{row['number_of_possible_assistances']}",
                          help="Número de personas que han marcado que asistirán a la actividad")

                if row.get('image_path'):
                    st.image(row['image_path'], use_column_width=True)

with general_tab:
    for _ in range(3):
        st.write("")

    if general_activities:

        st.subheader("Destacadas de Otros Organizadores")

        st.markdown("""
        ¡Descubre las actividades  que están atrayendo a más personas en todo Apptivity!
        """)



        df = pd.DataFrame(general_activities)

        for i, (index, row) in enumerate(df.iterrows()):

            with st.container(border=True):

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
