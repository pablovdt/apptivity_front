import streamlit as st
st.set_page_config(
    page_title="Apptivity - Crear Actividad-",
    page_icon='images/logotipo_apptivity3.png',
    layout='centered',
    initial_sidebar_state="expanded"
)
from menu import login, authenticated_menu
from dotenv import load_dotenv
import os
import time
from streamlit_cookies_manager import EncryptedCookieManager
from shared.activity_input_form import activity_input_form

from api.activity_api import activiti_api


load_dotenv()

cookies = EncryptedCookieManager(prefix=os.getenv("APPTIVITY_COOKIES_PREFIX"), password=os.getenv("APPTIVITY_COOKIES_PASSWORD"))
while not cookies.ready():
    time.sleep(0.1)
user_id = cookies.get("session_uuid")

if user_id is None:
    login(cookies)
    st.stop()

if cookies['organizer_role'] != 'true':
    st.stop()

authenticated_menu(cookies)

st.title("Formulario de Actividad")
# st.session_state['activity_to_repeat'] = None

data = activity_input_form(cookies)

if data:
    response = activiti_api.create_activity(activity=data)

    if response.status_code == 201:
        st.success("Actividad creada exitosamente!")
        st.session_state['activity_to_repeat'] = None
    else:
        st.error(f"Error {response.status_code}: {response.text}")
