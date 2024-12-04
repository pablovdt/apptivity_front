import streamlit as st

from api.user_api import user_api
from auth import cookies
from api.city_api import city_api
import json
from api.organizer import organizer_api

from utils import set_background_image, hash_password, save_image


def check_password(person_email: str, person_password: str):

    if organizer_api.validate_organizer(organizer_email=person_email, organizer_password=person_password):
        organizer_basic_info: dict = organizer_api.get_organizer_basic_info(person_email)

        print(organizer_basic_info)

        cookies['organizer_id'] = str(organizer_basic_info['id'])
        cookies['organizer_name'] = organizer_basic_info['name']
        cookies['organizer_email'] = person_email
        cookies['city_id'] = str(organizer_basic_info['city_id'])
        cookies['organizer_image_path'] = organizer_basic_info['image_path']
        cookies['organizer_latitude'] = str(organizer_basic_info['city_latitude'])
        cookies['organizer_longitude'] = str(organizer_basic_info['city_longitude'])

        cookies['organizer_role'] = 'true'
        cookies['user_role'] = 'false'

        cookies['apptivty_authenticated'] = 'true'

    elif user_api.validate_user(user_email=person_email, user_password=person_password):

        user_basic_info: dict = user_api.get_user_basic_info(person_email)

        print(user_basic_info)

        cookies['user_id'] = str(user_basic_info['id'])
        cookies['user_name'] = user_basic_info['name']
        cookies['user_email'] = person_email
        cookies['user_city_id'] = str(user_basic_info['city_id'])
        cookies['user_notification_distance'] = str(user_basic_info['notification_distance'])
        cookies['user_categories'] = json.dumps(user_basic_info['categories'])

        cookies['user_role'] = 'true'
        cookies['organizer_role'] = 'false'

        cookies['apptivty_authenticated'] = 'true'

    cookies.save()
    st.rerun()


def login():
    if st.button("Registrate"):
        st.switch_page("pages/registry.py")

    st.image("images/logotipo_apptivity.png")

    _, col, _ = st.columns([1, 3, 1])

    with col:
        with st.form(key="login_form"):
            st.subheader("Accede")
            person_login_email = st.text_input("Email:")
            person_login_password = st.text_input("Contraseña")

            if st.form_submit_button("Acceder"):
                if not person_login_email and not person_login_password:
                    st.warning("Campos insuficientes")
                    st.stop()
                check_password(person_email=person_login_email, person_password=person_login_password)


def authenticated_menu():

    st.sidebar.image("images/logotipo_apptivity2.png")
    for _ in range(2):
        st.sidebar.text('')

    if cookies['organizer_role'] == 'true':

        st.sidebar.page_link("app.py", label="🏠 Inicio")
        st.sidebar.page_link("pages/create_activity.py", label="📝 Crear actividad")
        st.sidebar.page_link("pages/show_next_activities.py", label="📅  Ver próximas actividades")
        st.sidebar.page_link("pages/show_activities.py", label="📄 Ver todas las actividades")
        st.sidebar.page_link("pages/organizer_activities_top_ranking.py", label="🏆 Actividades Top Ranking")
        st.sidebar.page_link("pages/organizer_map.py", label="📍Mapa de Actividades")
        st.sidebar.page_link("pages/statistics.py", label=" 📊 Estadisticas")

    elif cookies['user_role'] == 'true':

        st.sidebar.page_link("app.py", label="🏠 Inicio")
        st.sidebar.page_link("pages/user_show_activities.py", label="📄 Ver todas tus actividades")
        st.sidebar.page_link("pages/user_activities_by_categories.py", label="✚ Ver más actividades")
        st.sidebar.page_link("pages/user_activities_top_ranking.py", label="🏆 Actividades Top Ranking")
        st.sidebar.page_link("pages/user_organizers.py", label="🏛️ Organizadores")
        st.sidebar.page_link("pages/user_statistics.py", label=" 📊 Estadisticas")
        st.sidebar.page_link("pages/user_settings.py", label="⚙ ️Ajustes")

    st.sidebar.markdown('---')
    st.sidebar.page_link("pages/logout.py", label="Logout")


def check_authenticated():
    if cookies.get("apptivty_authenticated") != "true":
        login()
        st.stop()
    else:
        authenticated_menu()
