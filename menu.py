import streamlit as st
import uuid
from api.user_api import user_api
import json
from api.organizer import organizer_api

def clear_previous_cookies(cookies):
    keys_to_clear = [
        'organizer_id', 'organizer_name', 'organizer_email', 'organizer_city_id',
        'organizer_image_path', 'organizer_latitude', 'organizer_longitude',
        'organizer_role', 'user_id', 'user_name', 'user_email', 'user_city_id',
        'user_notification_distance', 'user_categories', 'user_role',
        'apptivty_authenticated', 'session_uuid'
    ]
    for key in keys_to_clear:
        cookies.pop(key, None)

def check_password(cookies, person_email: str, person_password: str):

    clear_previous_cookies(cookies)

    if organizer_api.validate_organizer(organizer_email=person_email, organizer_password=person_password):
        organizer_basic_info = organizer_api.get_organizer_basic_info(person_email)

        cookies['organizer_id'] = str(organizer_basic_info['id'])
        cookies['organizer_name'] = organizer_basic_info['name']
        cookies['organizer_email'] = person_email
        cookies['organizer_city_id'] = str(organizer_basic_info['city_id'])
        cookies['organizer_image_path'] = organizer_basic_info['image_path']
        cookies['organizer_latitude'] = str(organizer_basic_info['city_latitude'])
        cookies['organizer_longitude'] = str(organizer_basic_info['city_longitude'])

        cookies['organizer_role'] = 'true'
        cookies['user_role'] = 'false'

    elif user_api.validate_user(user_email=person_email, user_password=person_password):
        user_basic_info = user_api.get_user_basic_info(person_email)

        cookies['user_id'] = str(user_basic_info['id'])
        cookies['user_name'] = user_basic_info['name']
        cookies['user_email'] = person_email
        cookies['user_city_id'] = str(user_basic_info['city_id'])
        cookies['user_notification_distance'] = str(user_basic_info['notification_distance'])
        cookies['user_categories'] = json.dumps(user_basic_info['categories'])
        cookies['user_points'] = str(user_basic_info['points'])
        cookies['user_level_name'] = str(user_basic_info['level_name'])

        cookies['user_role'] = 'true'
        cookies['organizer_role'] = 'false'

    else:
        st.error("Credenciales inválidas.")
        return

    cookies['session_uuid'] = str(uuid.uuid4())

    cookies['apptivty_authenticated'] = 'true'
    cookies.save()
    st.rerun()


def login(cookies):
    if st.button("Registrate"):
        st.switch_page("pages/registry.py")

    st.image("images/logotipo_apptivity.png")

    _, col, _ = st.columns([1, 3, 1])

    with col:
        with st.form(key="login_form"):
            st.subheader("Accede")
            person_login_email = st.text_input("Email:")
            person_login_password = st.text_input("Contraseña", type='password')

            if st.form_submit_button("Acceder"):
                if not person_login_email and not person_login_password:
                    st.warning("Campos insuficientes")
                    st.stop()
                check_password(cookies=cookies, person_email=person_login_email, person_password=person_login_password)


def authenticated_menu(cookies):

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
        st.sidebar.page_link("pages/organizer_settings.py", label=" ⚙  Configuración")

    elif cookies['user_role'] == 'true':

        st.sidebar.page_link("app.py", label="🏠 Inicio")
        st.sidebar.page_link("pages/user_show_activities.py", label="📄 Ver todas tus actividades")
        st.sidebar.page_link("pages/user_activities_by_categories.py", label="✚ Ver más actividades")
        st.sidebar.page_link("pages/user_activities_top_ranking.py", label="🏆 Actividades Top Ranking")
        st.sidebar.page_link("pages/user_organizers.py", label="🏛️ Organizadores")
        st.sidebar.page_link("pages/user_statistics.py", label=" 📊 Estadisticas")
        st.sidebar.page_link("pages/user_settings.py", label="⚙ Configuración")

    st.sidebar.markdown('---')
    st.sidebar.page_link("pages/logout.py", label="↩️  Logout")
    st.sidebar.markdown('---')
    st.sidebar.page_link("pages/apptivity_contact.py", label="💬 Apptiviy Contacto")

