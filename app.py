import streamlit as st
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
from api.category_api import category_api
from api.place_api import place_api
from api.user_api import user_api

st.set_page_config(
    page_title="Apptivity",
    page_icon='',
    layout='centered',
    initial_sidebar_state="expanded"
)

load_dotenv()
from auth import cookies
from menu import check_authenticated

check_authenticated()

if cookies['organizer_role'] == 'true':

    st.switch_page("pages/organizer_home.py")

elif cookies['user_role'] == 'true':
    st.switch_page("pages/user_home.py")