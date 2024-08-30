import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime
from api.activity_api import activiti_api
from api.category_api import category_api
from api.place_api import place_api

st.set_page_config(
    page_title="Apptivity - Ver Actividades-",
    page_icon='',
    layout='centered',
    initial_sidebar_state="expanded"
)

load_dotenv()
from auth import cookies
from menu import check_authenticated

check_authenticated()

if 'activity_to_repeat' not in st.session_state:
    st.session_state['activity_to_repeat'] = None


import locale

locale.setlocale(locale.LC_TIME, 'es_ES')

st.subheader('Filtros:')
col1, col2, col3 = st.columns([2, 2, 2])
with col1:
    input_name = st.text_input('Nombre:')
with col2:
    cancelled = st.toggle('Cancelada', value=False)
with col3:
    places: list = place_api.get_places_by_cp("26312")
    places_options = {"": ""}
    places_options.update({place["name"]: place["id"] for place in places})
    place_selected_name = st.selectbox("Selecciona un lugar", places_options.keys())
    place_id = places_options[place_selected_name]

activities = activiti_api.get_activities(is_date_order_asc=False, activity_name=input_name, place_id=place_id,
                                         cancelled=cancelled)

df = pd.DataFrame(activities)

for i, (index, row) in enumerate(df.iterrows()):

    with st.container(border=True):
        st.subheader(row['name'])
        place = place_api.get_place_by_id(row["place_id"])['name']
        st.write(f'📍 **Lugar**: {place}')
        date_obj = datetime.fromisoformat(row['date'])
        st.write(f"📅 **Fecha:** {date_obj.strftime('%A, %d de %B de %Y')}")
        st.write(f"🕒 **Hora:** {date_obj.strftime('%H:%M:%S')}")
        st.write(f"💰 **Precio:** {row['price']} €")
        st.write(f"📝 **Descripción:**{row['description']}")
        category = category_api.get_category_by_id(row['category_id'])['name']
        st.write(f"🏷️ **Categoría:** {category}")
        if row['cancelled']:
            st.write(f"🚫 **CANCELADA !!**")
        st.write(f"👥 **Número de asistencias:** {row['number_of_assistances']}")
        st.write(f"📤 **Número de envios:** {row['number_of_shipments']}")
        st.write(f"🗑️ **Número de descartes:** {row['number_of_discards']}")

        col1, _, col2 = st.columns([2, 2, 2])

        with col1:
            if st.button("Editar Actividad", key=f'edit{i}'):
                st.session_state['activity_to_repeat'] = row
                st.switch_page('pages/update_activity.py')
        with col2:
            if st.button("Repetir Actividad", key=f'repeat{i}'):
                st.session_state['activity_to_repeat'] = row
                st.switch_page('pages/create_activity.py')