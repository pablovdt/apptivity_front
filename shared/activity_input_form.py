import streamlit as st
from datetime import datetime
import pytz


from api.category_api import category_api
from api.place_api import place_api
from utils import add_one_year, save_image

madrid_tz = pytz.timezone('Europe/Madrid')


def activity_input_form(activity, cookies):

    places: list = place_api.get_places_by_id(cookies['organizer_city_id'])
    places_options = {place["name"]: place["id"] for place in places}

    categories: list = category_api.get_categories()
    categories_options = {category["name"]: category["id"] for category in categories}

    # Convertir los IDs prellenados a los nombres correspondientes para los selectbox
    place_selected_name = [name for name, id_ in places_options.items() if id_ == activity['place_id']]
    category_selected_name = [name for name, id_ in categories_options.items() if id_ == activity['category_id']]

    # Seleccionar el primer valor si no hay coincidencia
    place_selected_name = place_selected_name[0] if place_selected_name else list(places_options.keys())[0]
    category_selected_name = category_selected_name[0] if category_selected_name else list(categories_options.keys())[0]

    with st.form(key='event_form'):

        name = st.text_input("Nombre", value=activity['name'])
        place_selected_name = st.selectbox("Selecciona un lugar", places_options.keys(),
                                           index=list(places_options.keys()).index(place_selected_name))

        place_id = places_options[place_selected_name]

        if activity["date"]:
            date = st.date_input("Fecha", value=datetime.fromisoformat(activity['date']).date())
            time = st.time_input("Hora", value=datetime.fromisoformat(activity['date']).time())
        else:
            date = st.date_input("Fecha")
            time = st.time_input("Hora")

        price = st.number_input("Precio", min_value=0.0, format="%.2f", value=float(activity['price']))
        description = st.text_area("Descripción", value=activity['description'])

        category_selected_name = st.selectbox("Selecciona categoría", categories_options.keys(),
                                              index=list(categories_options.keys()).index(category_selected_name))
        category_id = categories_options[category_selected_name]

        cancelled = st.checkbox("Cancelado", value=activity['cancelled'])


        if activity['image_path']:
            st.image(activity['image_path'])

        uploaded_file = st.file_uploader("Selecciona una imagen. Si no la proporcionas se pondrá la de tu perfil",
                                         type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            image_path = save_image(uploaded_file)
        else:
            image_path = activity['image_path'] if activity['image_path'] else "images/logotipo_apptivity.png"

        submit_button = st.form_submit_button("Enviar")

        combined_datetime = datetime.combine(date, time)
        localized_datetime = madrid_tz.localize(combined_datetime)
        date_time = localized_datetime.isoformat()

        if submit_button:
            data = {
                "name": name,
                "place_id": place_id,
                "date": date_time,
                "price": price,
                "organizer_id": cookies['organizer_id'],
                "description": description,
                "image_path": image_path,
                "category_id": category_id,
                "cancelled": cancelled
            }

            return data
