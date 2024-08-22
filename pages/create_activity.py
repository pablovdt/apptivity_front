import streamlit as st
from dotenv import load_dotenv
from datetime import datetime

from api.activity_api import activiti_api
from api.category_api import category_api
from api.place_api import place_api

st.set_page_config(
    page_title="Apptivity - Crear Actividad-",
    page_icon='',
    layout='centered',
    initial_sidebar_state="expanded"
)

load_dotenv()
from auth import cookies
from menu import check_authenticated

check_authenticated()

st.title("Formulario de Actividad")

# todo change tu organizer_cp

places: list = place_api.get_places_by_cp("26312")
places_options = {place["name"]: place["id"] for place in places}

categories: list = category_api.get_categories()
categories_options = {category["name"]: category["id"] for category in categories}

with st.form(key='event_form'):
    name = st.text_input("Nombre")
    place_selected_name = st.selectbox("Selecciona un lugar", places_options.keys())
    place_id = places_options[place_selected_name]
    date = st.date_input("Fecha", value=datetime.today())
    time = st.time_input("Hora", value=datetime.now().time())
    price = st.number_input("Precio", min_value=0.0, format="%.2f", value=0.0)
    description = st.text_area("Descripción")
    category_selected_name = st.selectbox("Selecciona categoría", categories_options.keys())
    category_id = categories_options[category_selected_name]
    cancelled = st.checkbox("Cancelado", value=False)

    submit_button = st.form_submit_button("Enviar")

if submit_button:
    date_time = datetime.combine(date, time).isoformat() + 'Z'  # Añadir 'Z' para indicar UTC

    data = {
        "name": name,
        "place_id": place_id,
        "date": date_time,
        "price": price,
        "organizer_id": cookies['organizer_id'],
        "description": description,
        "category_id": category_id,
        "cancelled": cancelled,
        "number_of_assistances": 0,
        "number_of_shipments": 0,
        "number_of_discards": 0
    }

    response = activiti_api.create_activity(activity=data)

    if response.status_code == 201:
        st.success("Actividad creada exitosamente!")
    else:
        st.error(f"Error {response.status_code}: {response.text}")
