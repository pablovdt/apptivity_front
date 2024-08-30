import streamlit as st
from dotenv import load_dotenv
from shared.activity_input_form import activity_input_form

from api.activity_api import activiti_api

st.set_page_config(
    page_title="Apptivity - Crear Actividad-",
    page_icon='',
    layout='centered',
    initial_sidebar_state="expanded"
)

load_dotenv()

from menu import check_authenticated

check_authenticated()

st.title("Formulario de Actividad")

data = activity_input_form()

if data:
    response = activiti_api.create_activity(activity=data)

    if response.status_code == 201:
        st.success("Actividad creada exitosamente!")
        st.session_state['activity_to_repeat'] = None
    else:
        st.error(f"Error {response.status_code}: {response.text}")
