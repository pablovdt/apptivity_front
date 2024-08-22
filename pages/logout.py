import streamlit as st

from auth import cookies

cookies['organizer_name'] = ''
cookies['organizer_id'] = ''
cookies['apptivty_authenticated'] = ''

cookies.save()

st.switch_page('app.py')