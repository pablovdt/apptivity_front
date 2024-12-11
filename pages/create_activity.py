import streamlit as st

st.set_page_config(
    page_title="Apptivity - Crear Actividad-",
    page_icon='images/logotipo_apptivity3.png',
    layout='centered',
    initial_sidebar_state="expanded"
)
from utils import create_qr_code
from menu import login, authenticated_menu
from dotenv import load_dotenv
import os
import time
from datetime import datetime
from streamlit_cookies_manager import EncryptedCookieManager
from shared.activity_input_form import activity_input_form
import pytz
from api.activity_api import activiti_api

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

madrid_tz = pytz.timezone('Europe/Madrid')

st.title("Formulario de Actividad")

activity = {
    "name": "",
    "place_id": "",
    "date": "",
    "price": 0,
    "organizer_id": "",
    "description": "",
    "image_path": "",
    "category_id": "",
    "cancelled": False
}

data = activity_input_form(activity=activity, cookies=cookies, button_text="Crear Actividad")

if data:
    response = activiti_api.create_activity(activity=data)

    if response.status_code == 201:
        st.success("Actividad creada exitosamente!")
        st.header("Descárgate el codigo QR de la actividad")
        st.write("Deberás imprimirlo y llevarlo al lugar de la activiad para que los usuarios puedan confirmar su asistencia")
        create_qr_code(activity_id=response.json()['id'], organizer_id=int(cookies['organizer_id']))

    else:
        st.error(f"Error {response.status_code}: {response.text}")
