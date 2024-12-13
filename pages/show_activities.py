import streamlit as st

st.set_page_config(
    page_title="Apptivity - Ver Actividades-",
    page_icon='images/APPTIVITY3.png',
    layout='centered',
    initial_sidebar_state="expanded"
)
from utils import create_qr_code
from menu import login, authenticated_menu
import pandas as pd
from dotenv import load_dotenv
import os
import time
from streamlit_cookies_manager import EncryptedCookieManager
from datetime import datetime
from api.activity_api import activiti_api
from api.category_api import category_api
from api.place_api import place_api

import pytz

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

now = datetime.now(pytz.timezone("Europe/Madrid"))

if 'activity_to_repeat' not in st.session_state:
    st.session_state['activity_to_repeat'] = None

import locale

# locale.setlocale(locale.LC_TIME, 'es_ES')

st.title('Gestiona actividades realizadas')

st.subheader('Filtros:')

col1, col2, col3 = st.columns([2, 2, 2])
with col1:
    input_name = st.text_input('Nombre:')
with col2:
    cancelled = st.toggle('Cancelada', value=False)
with col3:
    places: list = place_api.get_places_by_id(cookies['organizer_city_id'])
    places_options = {"Todos": ""}
    places_options.update({place["name"]: place["id"] for place in places})
    place_selected_name = st.selectbox("Selecciona un lugar", places_options.keys())
    place_id = places_options[place_selected_name]

activities = activiti_api.get_activities(organizer_id=cookies['organizer_id'], is_date_order_asc=False,
                                         activity_name=input_name, place_id=place_id,
                                         cancelled=cancelled, date_to=datetime.now(pytz.timezone("Europe/Madrid")).strftime("%Y-%m-%d"))

df = pd.DataFrame(activities)

for _ in range(3):
    st.write("")

if len(activities) >= 1:

    for i, (index, row) in enumerate(df.iterrows()):

        date_obj = datetime.fromisoformat(row['date'])

        with st.popover(f"{row['name']} -- {date_obj.strftime('%A, %d de %B de %Y')}"):

            st.subheader(row['name'])
            place = place_api.get_place_by_id(row["place_id"])
            st.write(f'📍 **Lugar:** [{place["name"]}]({place["location_url"]})')

            st.write(f"📅 **Fecha:** {date_obj.strftime('%A, %d de %B de %Y')}")
            st.write(f"🕒 **Hora:** {date_obj.strftime('%H:%M:%S')}")
            st.write(f"💰 **Precio:** {row['price']} €")
            if float(row['price']) > 0:
                st.write(f"💰 **Valor esperado**: {row['price'] * row['number_of_possible_assistances']} €" if row[
                                                                                                                  'number_of_possible_assistances'] > 0 else "💰 **Valor esperado**: 0 €")
                st.write(f"💰 **Valor real**: {row['price'] * row['number_of_assistances']} €")
            st.write(f"📝 **Descripción:** {row['description']}")
            category = category_api.get_category_by_id(row['category_id'])['name']
            st.write(f"🏷️ **Categoría:** {category}")
            if row['cancelled']:
                st.write(f"🚫 **CANCELADA !!**")

            if row['number_of_shipments'] > 0:
                st.write(
                    f"%  **Porcentaje de asistencia:** {(row['number_of_assistances'] / row['number_of_shipments']) * 100} %")
            else:
                st.write(f"%  **Porcentaje de asistencia:** 0.0 %")

            if row['number_of_possible_assistances'] > 0:
                porcentaje = (row['number_of_assistances'] / row['number_of_possible_assistances']) * 100
                st.write(f"% **Porcentaje de cumplimiento:** {porcentaje:.2f}%")
            else:
                st.write(f"% **Porcentaje de cumplimiento:** 0.0 %")

            colm1, colm2, colm3, colm4 = st.columns([2, 2, 2, 2])

            with colm1:
                st.metric(label=f"📤 **Alcance:** ", value=f"{row['number_of_shipments']}",
                          help="Número de personas a las que se le ha notificado con esta actividad")
            with colm2:
                st.metric(label=f"👥 **Asistiré:**", value=f"{row['number_of_possible_assistances']}",
                          help="Número de personas que han marcado que asistirán a la actividad")
            with colm3:
                st.metric(label=f"🗑️ **No asistiré:**", value=f" {row['number_of_discards']}",
                          help="Número de personas que han descartado la actividad")
            with colm4:
                st.metric(label=f"👥 ✅ **Asistencias:**", value=f"{row['number_of_assistances']}",
                          help="Número de personas que asistieron a la actividad")



            st.image(row['image_path'])

            col1, col2, col3 = st.columns([2, 2, 2])

            with col2:
                if st.button("Repetir Actividad", key=f'repeat{i}'):
                    st.session_state['activity_to_repeat'] = row
                    st.switch_page('pages/repeat_activity.py')


else:
    st.info("Ninguna actividad coincide con los filtros de búsqueda")
