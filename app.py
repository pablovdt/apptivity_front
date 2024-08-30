import streamlit as st
from dotenv import load_dotenv

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

st.header(f"Hola {cookies['organizer_name']}")

st.image(cookies['organizer_image_path'])