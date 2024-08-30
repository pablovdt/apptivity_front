import streamlit as st
from dotenv import load_dotenv
from shared.activity_input_form import activity_input_form

from api.activity_api import activiti_api

st.set_page_config(
    page_title="Apptivity - Actualizar Actividad-",
    page_icon='',
    layout='centered',
    initial_sidebar_state="expanded"
)

load_dotenv()
from auth import cookies
from menu import check_authenticated

check_authenticated()

if 'activity_to_repeat' not in st.session_state:
    st.session_state['activity_to_repeat'] = None

if st.session_state['activity_to_repeat'] is not None:

    st.title("Edita la Actividad")

    # todo obtener de la sesion ala actividad e a editar y mandarsela a este metodo
    # todo o obtenrla desde alli, una vez cvon data le llamamos a update activity
    data = activity_input_form()

    if data:
        response = activiti_api.update_activity(activity=data, activity_id=st.session_state['activity_to_repeat']['id'])

        if response.status_code == 200:
            st.success("Actividad Actualizada exitosamente!")
            st.session_state['activity_to_repeat'] = None
        else:
            st.error(f"Error {response.status_code}: {response.text}")

else:
    st.warning("Selecciona una actividad para editar")
