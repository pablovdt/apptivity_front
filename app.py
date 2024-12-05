from dotenv import load_dotenv
import os
import time
from menu import login, authenticated_menu
from streamlit_cookies_manager import EncryptedCookieManager
import streamlit as st

load_dotenv()

cookies = EncryptedCookieManager(prefix=os.getenv("APPTIVITY_COOKIES_PREFIX"),
                                 password=os.getenv("APPTIVITY_COOKIES_PASSWORD"))
while not cookies.ready():
    time.sleep(0.1)

if not cookies.ready():
    st.stop()

user_id = cookies.get("session_uuid")
if user_id is None or user_id == '':
    login(cookies)
    st.stop()

if cookies['organizer_role'] == 'true':
    authenticated_menu(cookies)
    st.switch_page("pages/organizer_home.py")

elif cookies['user_role'] == 'true':

    st.switch_page("pages/user_home.py")
