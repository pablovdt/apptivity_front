import streamlit as st
from dotenv import load_dotenv

st.set_page_config(
    page_title="Apptivity - Estadisticas -",
    page_icon='images/APPTIVITY3.png',
    layout='centered',
    initial_sidebar_state="expanded"
)
from menu import login, authenticated_menu
import os
import time
from streamlit_cookies_manager import EncryptedCookieManager

load_dotenv()

cookies = EncryptedCookieManager(prefix=os.getenv("APPTIVITY_COOKIES_PREFIX"),
                                 password=os.getenv("APPTIVITY_COOKIES_PASSWORD"))
while not cookies.ready():
    time.sleep(0.1)
user_id = cookies.get("session_uuid")

if user_id is None:
    login(cookies)
    st.stop()

if cookies['user_role'] != 'true':
    st.stop()

authenticated_menu(cookies)

if cookies['user_role'] != 'true':
    st.stop()
