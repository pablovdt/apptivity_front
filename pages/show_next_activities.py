import streamlit as st

st.set_page_config(
    page_title="Apptivity - Ver Proximas actividades -",
    page_icon='images/logotipo_apptivity3.png',
    layout='centered',
    initial_sidebar_state="expanded"
)
from menu import login, authenticated_menu
import pytz
import pandas as pd
from dotenv import load_dotenv
import os
import time
from streamlit_cookies_manager import EncryptedCookieManager
from shared.activity_input_form import activity_input_form
from datetime import datetime
from api.activity_api import activiti_api
from api.category_api import category_api
from api.place_api import place_api

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

st.title('Gestiona actividades futuras')

st.subheader('Filtros:')
col1, col2, col3 = st.columns([2, 2, 2])
with col1:
    input_name = st.text_input('Nombre:')
with col2:
    cancelled = st.toggle('Cancelada', value=False)
with col3:
    places: list = place_api.get_places_by_id(cookies['city_id'])
    places_options = {"": ""}
    places_options.update({place["name"]: place["id"] for place in places})
    place_selected_name = st.selectbox("Selecciona un lugar", places_options.keys())
    place_id = places_options[place_selected_name]

activities = activiti_api.get_activities(organizer_id=cookies['organizer_id'],
                                         date_from=datetime.now(pytz.timezone("Europe/Madrid")).strftime("%Y-%m-%d"), activity_name=input_name,
                                         place_id=place_id, cancelled=cancelled)

df = pd.DataFrame(activities)

if activities:

    for i, (index, row) in enumerate(df.iterrows()):

        with st.container(border=True):
            st.subheader(row['name'])
            place = place_api.get_place_by_id(row["place_id"])
            if not place['location_url']:
                st.write(f'📍 **Lugar**: {place["name"]}')
            else:
                st.write(f'📍 **Lugar:** {place["name"]}. **Ubicación:** {place["location_url"]}')
            date_obj = datetime.fromisoformat(row['date'])
            st.write(f"📅 **Fecha:** {date_obj.strftime('%A, %d de %B de %Y')}")
            st.write(f"🕒 **Hora:** {date_obj.strftime('%H:%M:%S')}")
            st.write(f"💰 **Precio:** {row['price']} €")
            st.write(f"📝 **Descripción:** {row['description']}")
            category = category_api.get_category_by_id(row['category_id'])['name']
            st.write(f"🏷️ **Categoría:** {category}")
            if row['cancelled']:
                st.write(f"🚫 **CANCELADA !!**")
            colm1, colm2, colm3 = st.columns([2, 2, 2])
            with colm1:
                st.metric(label=f"👥 **Posibles asistencias:**", value=f"{row['number_of_possible_assistances']}")
            with colm2:
                st.metric(label=f"📤 **Envios:** ", value=f"{row['number_of_shipments']}")
            with colm3:
                st.metric(label=f"🗑️ **Descartes:**", value=f" {row['number_of_discards']}")
            st.image(row['image_path'])

            col1, _, col2 = st.columns([2, 2, 2])

            with col1:
                if st.button("Editar Actividad", key=f'edit{i}'):
                    st.session_state['activity_to_repeat'] = row
                    st.switch_page('pages/update_activity.py')
            with col2:
                if st.button("Repetir Actividad", key=f'repeat{i}'):
                    st.session_state['activity_to_repeat'] = row
                    st.switch_page('pages/create_activity.py')

else:
    st.info("Cuando crees actividades, aparecerán aqui:")
