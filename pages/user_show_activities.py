import streamlit as st
from dotenv import load_dotenv

st.set_page_config(
    page_title="Apptivity - Ver Todas las Actividades -",
    page_icon='',
    layout='centered',
    initial_sidebar_state="expanded"
)

load_dotenv()

from menu import check_authenticated

check_authenticated()

from auth import cookies

if cookies['user_role'] != 'true':
    st.stop()

