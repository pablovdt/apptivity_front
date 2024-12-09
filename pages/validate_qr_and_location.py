import streamlit as st
import streamlit as st
from streamlit_geolocation import streamlit_geolocation
from api.user_api import user_api
from pages.create_activity import cookies


def process_url_params():
    params = st.experimental_get_query_params()

    if "activity_id" in params and "organizer_id" in params:
        activity_id = params["activity_id"][0]
        organizer_id = params["organizer_id"][0]

        return activity_id, organizer_id

    else:
        st.warning("Algo salio mal, intentelo de nuevo mas tarde")


activity_id, organizer_id = process_url_params()

location = streamlit_geolocation()

response = user_api.validate_qr_and_location(activity_id=activity_id, organizer_id=organizer_id,
                                             user_id=cookies['user_id'], latitude=location['latitude'],
                                             longitude=location['longitude'])

if response.status_code == 200:
    if response.json():
        st.success("Tu asistencia ha sido confirmada !!")
    else:
        st.warning("No se ha podido confirmar, prueba de nuevo mas tarde.")
else:
    st.warning("No se ha podido confirmar, prueba de nuevo mas tarde.")
