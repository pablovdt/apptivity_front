import streamlit as st

st.set_page_config(
    page_title="Apptivity - Top Ranking-",
    page_icon='',
    layout='centered',
    initial_sidebar_state="expanded"
)

from datetime import datetime
import pytz

now = datetime.now(pytz.timezone("Europe/Madrid"))
from api.activity_api import activiti_api

from api.place_api import place_api
from api.user_api import user_api
from api.city_api import city_api

from dotenv import load_dotenv
import pandas as pd
from datetime import datetime

load_dotenv()

from menu import check_authenticated

check_authenticated()

from auth import cookies

if cookies['organizer_role'] != 'true':
    st.stop()

organizer_activities = activiti_api.get_activities(organizer_id=cookies['organizer_id'],
                                                   date_from=datetime.now().strftime("%Y-%m-%d"), cancelled=False,
                                                   order_by_assistance=True)

general_activities = activiti_api.get_activities(date_from=datetime.now().strftime("%Y-%m-%d"), cancelled=False,
                                                 order_by_assistance=True, limit=10)

st.title('🔥 Ranking de Eventos Populares 🔥')

organizer_tab, general_tab = st.tabs([f"{cookies['organizer_name']} top ranking", "General Top Ranking"])

with organizer_tab:
    for _ in range(3):
        st.write("")

    if organizer_activities:

        st.subheader("Tus Top Ranking")

        st.markdown("""
        Aquí tienes tus 10 Actividades más populares según las asistencias registradas.
        ¡Descubre las actividades que están atrayendo a más personas!
        """)

        st.markdown('#### Actividades más Populares por Asistencias:')

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

                if row.get('image_path'):
                    st.image(row['image_path'], use_column_width=True)

with general_tab:
    for _ in range(3):
        st.write("")

    if general_activities:

        st.subheader("Top Ranking de todo Apptivity")

        st.markdown("""
        Aquí tienes las 10 Actividades más populares según las asistencias registradas.
        ¡Descubre los eventos que están atrayendo a más personas!
        """)

        st.markdown('#### Actividades más Populares por Asistencias:')

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

                if st.button(f"Añadir actividad a Inicio", key=row['id']):
                    user_api.add_user_activity(user_id=cookies['user_id'], activity_id=row['id'])
                    st.rerun()
