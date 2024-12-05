# import os
# import uuid
# from streamlit_cookies_manager import EncryptedCookieManager
# import streamlit as st
#
# def initialize_cookies():
#     # Verificar si ya existe un session_id en el session_state
#     if 'session_id' not in st.session_state:
#         # Si no existe, generamos un session_id único
#         st.session_state['session_id'] = str(uuid.uuid4())
#         print(f"New session created with ID: {st.session_state['session_id']}")
#
#     # Usamos EncryptedCookieManager con un prefijo único por usuario basado en el session_id
#     cookies = EncryptedCookieManager(prefix=f"apptivity_cookies_{st.session_state['session_id']}",
#                                      password=os.getenv("APPTIVITY_COOKIES_PASSWORD"))
#
#     # Si las cookies no están listas (es decir, no hay cookies ya almacenadas), detén la app
#     if not cookies.ready():
#         st.stop()
#
#     # Si la cookie no existe, la creamos
#     if 'apptivty_authenticated' not in cookies:
#         print("No cookies found, creating a new session...")
#         # Aquí podrías modificar o agregar cookies según sea necesario
#         cookies['apptivty_authenticated'] = 'false'  # Ejemplo de creación de cookie
#         cookies.save()  # Guardamos las cookies de inmediato
#
#     return cookies
