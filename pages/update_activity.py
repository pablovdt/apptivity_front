import streamlit as st
from menu import login, authenticated_menu
from dotenv import load_dotenv
import os
import time
from streamlit_cookies_manager import EncryptedCookieManager
from shared.activity_input_form import activity_input_form

from api.activity_api import activiti_api

st.set_page_config(
    page_title="Apptivity - Actualizar Actividad-",
    page_icon='images/logotipo_apptivity3.png',
    layout='centered',
    initial_sidebar_state="expanded"
)

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

if 'activity_to_repeat' not in st.session_state:
    st.session_state['activity_to_repeat'] = None

if st.session_state['activity_to_repeat'] is not None:

    st.title("Edita la Actividad")

    data = activity_input_form(cookies)

    if data:
        response = activiti_api.update_activity(activity=data, activity_id=st.session_state['activity_to_repeat']['id'])

        if response.status_code == 200:
            st.success("Actividad Actualizada exitosamente!")
            st.session_state['activity_to_repeat'] = None
        else:
            st.error(f"Error {response.status_code}: {response.text}")

else:
    st.warning("Selecciona una actividad para editar")
