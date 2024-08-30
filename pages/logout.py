import streamlit as st

from auth import cookies

cookies['organizer_name'] = ''
cookies['organizer_id'] = ''
cookies['organizer_email'] = ''
cookies['organizer_cp'] = ''

cookies['apptivty_authenticated'] = 'false'

cookies.save()

st.switch_page('app.py')