import streamlit as st

st.set_page_config(
    page_title="Apptivity - Top Ranking -",
    page_icon='',
    layout='centered',
    initial_sidebar_state="expanded"
)
import pytz
from datetime import datetime

now = datetime.now(pytz.timezone("Europe/Madrid"))
from api.activity_api import activiti_api
from api.category_api import category_api
from api.place_api import place_api
from api.user_api import user_api
from api.city_api import city_api

from menu import check_authenticated
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime

load_dotenv()
from auth import cookies

check_authenticated()

if cookies['user_role'] != 'true':
    st.stop()


activities = activiti_api.get_activities(date_from=datetime.now().strftime("%Y-%m-%d"), cancelled=False,
                                         order_by_assistance=True, limit=10)
if activities:

    st.title('🔥 Ranking de Eventos Populares 🔥')

    st.markdown("""
    Aquí tienes las 10 Actividades más populares según las asistencias registradas.
    ¡Descubre los eventos que están atrayendo a más personas!
    """)

    st.markdown('#### Actividades más Populares por Asistencias:')

    df = pd.DataFrame(activities)

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

