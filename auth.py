import os
import streamlit as st

from streamlit_cookies_manager import EncryptedCookieManager

cookies = None


def initialize_cookies():
    global cookies

    if cookies is None:
        cookies = EncryptedCookieManager(
            prefix="apptivity_cookies",
            password=os.getenv("APPTIVITY_COOKIES_PASSWORD")
        )

        if not cookies.ready():
            st.stop()
    return cookies


initialize_cookies()
