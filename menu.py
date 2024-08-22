import streamlit as st
from auth import cookies
from api.city_api import city_api
from api.organizer import organizer_api

from utils import set_background_image, hash_password


def check_password(organizer_email: str, organizer_password: str):
    if organizer_api.validate_organizer(organizer_email=organizer_email, organizer_password=organizer_password):
        organizer_basic_info: dict = organizer_api.get_organizer_basic_info(organizer_email)

        print(organizer_basic_info)

        cookies['organizer_name'] = organizer_basic_info['name']
        cookies['organizer_id'] = str(organizer_basic_info['id'])
        cookies['apptivty_authenticated'] = 'true'

        cookies.save()
        st.rerun()


def login():
    # set_background_image()

    cities: list = city_api.get_cities()

    cities_options = {city["name"]: city["cp"] for city in cities}

    st.image("images/logotipo_apptivity.png")

    col_register, _, col_login = st.columns([3, 1, 3])

    with col_register:
        with st.form(key="register_form", clear_on_submit=True):
            st.subheader("Registrate")
            name = st.text_input("Nombre", value="")
            city_selected = st.selectbox("Municipio", cities_options.keys())
            city_cp = cities_options[city_selected]
            description = st.text_area("Descripción", value="")
            email = st.text_input("Correo Electrónico", value="")
            password = st.text_input("Contraseña", type='password')
            confirm_password = st.text_input("Repite contraseña", type='password')
            phone = st.text_input("Teléfono", value="")

            # todo validate email

            if password != confirm_password:
                st.warning("Las contraseñas no coinciden")
                st.stop()

            hashed_password = hash_password(password)

            if st.form_submit_button("Registrarse"):
                data = {
                    "name": name,
                    "city_cp": city_cp,
                    "description": description,
                    "email": email,
                    "phone": phone,
                    "password": hashed_password
                }

                response = organizer_api.create_organizer(data)

                if response.status_code == 201:
                    st.success("Te has registrado correctamente")
                else:
                    st.error("Ocurrió un error. Intentelo de nuevo mas tarde")

    with col_login:
        with st.form(key="login_form"):
            st.subheader("Accede")
            organizer_login_email = st.text_input("Email:")
            organizer_login_password = st.text_input("Contraseña")

            if st.form_submit_button("Acceder"):
                check_password(organizer_email=organizer_login_email, organizer_password=organizer_login_password)


def authenticated_menu():
    st.sidebar.image("images/logotipo_apptivity.png")
    for _ in range(2):
        st.sidebar.text('')
    st.sidebar.page_link("app.py", label="🏠 Inicio")
    st.sidebar.page_link("pages/create_activity.py", label="📝 Crear actividad")
    st.sidebar.page_link("pages/show_next_activities.py", label="📅  Ver próximas actividades")
    st.sidebar.page_link("pages/show_activities.py", label="📄 Ver todas las actividades")
    st.sidebar.markdown('---')
    st.sidebar.page_link("pages/logout.py", label="Logout")


def check_authenticated():
    if cookies.get("apptivty_authenticated") != "true":
        login()
        st.stop()
    else:
        authenticated_menu()
