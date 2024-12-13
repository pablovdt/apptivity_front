import streamlit as st
st.set_page_config(
    page_title="Apptivity - Repetir Actividad-",
    page_icon='images/APPTIVITY3.png',
    layout='centered',
    initial_sidebar_state="expanded"
)
from datetime import datetime
from menu import login, authenticated_menu
from dotenv import load_dotenv
import os
import time
from streamlit_cookies_manager import EncryptedCookieManager
from shared.activity_input_form import activity_input_form
from utils import add_one_year
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
st.write('Repite la actividad sin tener que rellenar la información')
st.write('Por defecto se pone la misma fecha pero un año mas tarde')

if 'year_added' not in st.session_state:
    st.session_state['year_added'] = False

if not st.session_state['year_added']:
    st.session_state['activity_to_repeat']['date'] = str(add_one_year(datetime.fromisoformat(st.session_state['activity_to_repeat']['date'])))
    st.session_state['year_added'] = True


data = activity_input_form(activity=st.session_state['activity_to_repeat'], cookies=cookies, button_text="Repetir Actividad")

if data:
    response = activiti_api.create_activity(activity=data)

    if response.status_code == 201:
        st.success("Actividad repetida exitosamente!")
    else:
        st.error(f"Error {response.status_code}: {response.text}")

    st.session_state['year_added'] = True
    st.session_state['activity_to_repeat'] = None