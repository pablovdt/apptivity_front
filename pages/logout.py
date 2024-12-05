import streamlit as st
import os
import time
from streamlit_cookies_manager import EncryptedCookieManager

cookies = EncryptedCookieManager(prefix="apptivity_cookies", password=os.getenv("APPTIVITY_COOKIES_PASSWORD"))
while not cookies.ready():
    time.sleep(0.1)
cookies['session_uuid'] = ''

cookies['organizer_id'] = ''
cookies['organizer_name'] = ''
cookies['organizer_email'] = ''
cookies['organizer_city_id'] = ''
cookies['organizer_image_path'] = ''
cookies['organizer_latitude'] = ''
cookies['organizer_longitude'] = ''
cookies['organizer_role'] = 'false'

cookies['user_id'] = ''
cookies['user_name'] = ''
cookies['user_email'] = ''
cookies['user_city_id'] = ''
cookies['user_notification_distance'] = ''
cookies['user_categories'] = ''
cookies['user_role'] = 'false'

cookies['apptivty_authenticated'] = 'false'

cookies.save()

st.switch_page('app.py')
