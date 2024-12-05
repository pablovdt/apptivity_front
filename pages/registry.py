import streamlit as st

from api.category_api import category_api
from api.user_api import user_api

st.set_page_config(
    page_title="Apptivity - Registro -",
    page_icon='images/logotipo_apptivity3.png',
    layout='centered',
    initial_sidebar_state="expanded"
)

from api.city_api import city_api
from api.organizer import organizer_api
from utils import save_image, hash_password


st.sidebar.image("images/logotipo_apptivity2.png")
for _ in range(2):
    st.sidebar.text('')
st.sidebar.page_link("app.py", label="🏠 Inicio")

st.image("images/logotipo_apptivity.png")

cities: list = city_api.get_cities()
cities_options = {city["name"]: city["id"] for city in cities}

categories: list = category_api.get_categories()
categories_options = {category["name"]: category["id"] for category in categories}

col1, col2, col3 = st.columns([3, 1, 3])

with col1:
    st.subheader("Registro usuarios")

    with st.form(key="register_form_user", clear_on_submit=True):

        name = st.text_input("Nombre", value="")
        city_selected = st.selectbox("Municipio", cities_options.keys())
        city_id = cities_options[city_selected]

        categories_selected = st.multiselect("Categorías", list(categories_options.keys()))

        categories_ids = [categories_options[cat] for cat in categories_selected]

        email = st.text_input("Correo Electrónico", value="")
        password = st.text_input("Contraseña", type='password')
        confirm_password = st.text_input("Repite contraseña", type='password')

        # todo validate email

        if password != confirm_password:
            st.warning("Las contraseñas no coinciden")
            st.stop()

        hashed_password = hash_password(password)

        if st.form_submit_button("Registrar Usuario"):
            data = {
                "name": name,
                "city_id": city_id,
                "email": email,
                "password": hashed_password,
                "category_ids": categories_ids,
                "settings": "",
                "notification_distance": 20
            }

            response = user_api.create_user(data)

            if response.status_code == 201:
                st.success("Te has registrado correctamente")
            else:
                st.error("Ocurrió un error. Intentelo de nuevo mas tarde")

with col3:
    st.subheader("Registro organizadores")

    with st.form(key="register_form", clear_on_submit=True):

        name = st.text_input("Nombre", value="")
        city_selected = st.selectbox("Municipio", cities_options.keys())
        city_id = cities_options[city_selected]
        description = st.text_area("Descripción", value="")
        email = st.text_input("Correo Electrónico", value="")
        password = st.text_input("Contraseña", type='password')
        confirm_password = st.text_input("Repite contraseña", type='password')
        phone = st.text_input("Teléfono", value="")
        uploaded_file = st.file_uploader("Selecciona una imagen", type=["jpg", "jpeg", "png"])


        # todo validate email

        if password != confirm_password:
            st.warning("Las contraseñas no coinciden")
            st.stop()

        if uploaded_file is not None:
            image_path = save_image(uploaded_file)
        else:
            image_path= ''
        hashed_password = hash_password(password)

        if st.form_submit_button("Registrarse"):
            data = {
                "name": name,
                "city_id": city_id,
                "description": description,
                "email": email,
                "phone": phone,
                "password": hashed_password,
                "image_path": image_path
            }

            response = organizer_api.create_organizer(data)

            if response.status_code == 201:
                st.success("Te has registrado correctamente")
            else:
                st.error("Ocurrió un error. Intentelo de nuevo mas tarde")
