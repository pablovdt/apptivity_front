import streamlit as st
from auth import cookies
from datetime import datetime

from api.category_api import category_api
from api.place_api import place_api
from utils import add_one_year, save_image


def activity_input_form():
    if 'activity_to_repeat' not in st.session_state:
        st.session_state['activity_to_repeat'] = None

    if st.session_state['activity_to_repeat'] is not None:

        prefill_values = {
            "name": st.session_state['activity_to_repeat']['name'],
            "place_id": st.session_state['activity_to_repeat']['place_id'],
            "date": add_one_year(datetime.fromisoformat(st.session_state['activity_to_repeat']['date']).date()),
            "time": datetime.fromisoformat(st.session_state['activity_to_repeat']['date']).time(),
            "price": st.session_state['activity_to_repeat']['price'],
            "description": st.session_state['activity_to_repeat']['description'],
            "category_id": st.session_state['activity_to_repeat']['category_id'],
            "cancelled": False,
            "image_path": st.session_state['activity_to_repeat']['image_path']
        }
    else:
        prefill_values = {
            "name": "",
            "place_id": None,
            "date": datetime.today().date(),
            "time": datetime.now().time(),
            "price": 0.0,
            "description": "",
            "category_id": None,
            "cancelled": False,
            "image_path": ""
        }

    places: list = place_api.get_places_by_id(cookies['city_id'])
    places_options = {place["name"]: place["id"] for place in places}

    categories: list = category_api.get_categories()
    categories_options = {category["name"]: category["id"] for category in categories}

    # Convertir los IDs prellenados a los nombres correspondientes para los selectbox
    place_selected_name = [name for name, id_ in places_options.items() if id_ == prefill_values['place_id']]
    category_selected_name = [name for name, id_ in categories_options.items() if id_ == prefill_values['category_id']]

    # Seleccionar el primer valor si no hay coincidencia
    place_selected_name = place_selected_name[0] if place_selected_name else list(places_options.keys())[0]
    category_selected_name = category_selected_name[0] if category_selected_name else list(categories_options.keys())[0]

    with st.form(key='event_form'):
        name = st.text_input("Nombre", value=prefill_values['name'])
        place_selected_name = st.selectbox("Selecciona un lugar", places_options.keys(),
                                           index=list(places_options.keys()).index(place_selected_name))
        place_id = places_options[place_selected_name]

        date = st.date_input("Fecha", value=prefill_values['date'])
        time = st.time_input("Hora", value=prefill_values['time'])

        price = st.number_input("Precio", min_value=0.0, format="%.2f", value=float(prefill_values['price']))
        description = st.text_area("Descripción", value=prefill_values['description'])

        category_selected_name = st.selectbox("Selecciona categoría", categories_options.keys(),
                                              index=list(categories_options.keys()).index(category_selected_name))
        category_id = categories_options[category_selected_name]

        cancelled = st.checkbox("Cancelado", value=prefill_values['cancelled'])

        uploaded_file = st.file_uploader("Selecciona una imagen. Si no la proporcionas se pondrá la de tu perfil", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            image_path = save_image(uploaded_file)
        else:
            image_path = "images/logotipo_apptivity.png"  # todo, sustituir por la del perfil de cada organizador

        submit_button = st.form_submit_button("Enviar")

        if submit_button:
            date_time = datetime.combine(date, time).isoformat() + 'Z'

            data = {
                "name": name,
                "place_id": place_id,
                "date": date_time,
                "price": price,
                "organizer_id": cookies['organizer_id'],
                "description": description,
                "image_path": image_path,
                "category_id": category_id,
                "cancelled": cancelled,
                "number_of_possible_assistances": 0,
                "number_of_assistances": 0,
                "number_of_shipments": 0,
                "number_of_discards": 0
            }

            return data
