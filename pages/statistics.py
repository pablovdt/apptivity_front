import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from api.activity_api import activiti_api


st.set_page_config(
    page_title="Apptivity - Estadisticas -",
    page_icon='',
    layout='centered',
    initial_sidebar_state="expanded"
)

load_dotenv()
from auth import cookies
from menu import check_authenticated

check_authenticated()

from auth import cookies
if cookies['organizer_role'] != 'true':
    st.stop()

