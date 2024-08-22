import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime
from api.activity_api import activiti_api
from api.category_api import category_api
from api.place_api import place_api

st.set_page_config(
    page_title="Apptivity - Ver Proximas actividades -",
    page_icon='',
    layout='centered',
    initial_sidebar_state="expanded"
)

load_dotenv()
from auth import cookies
from menu import check_authenticated

check_authenticated()

activities = activiti_api.get_activities(date_from=datetime.now().strftime("%Y-%m-%d"))

df = pd.DataFrame(activities)

for index, row in df.iterrows():
    with st.container(border=True):
        st.subheader(row['name'])

        place = place_api.get_place_by_id(row["place_id"])['name']
        st.write(f'Lugar: {place}')
        st.write(f"Fecha:{row['date']}")
        st.write(f"Precio: {row['price']}")
        st.write(f"Descripción:{row['description']}")
        category = category_api.get_category_by_id(row['category_id'])['name']
        st.write(f"Categoría:{category}")
        if row['cancelled'] == "False":
            st.write(f"CANCELADA !!")
        st.write(f"Número de asistencias:{row['number_of_assistances']}")
        st.write(f"Número de envios:{row['number_of_shipments']}")
        st.write(f"Número de descartes:{row['number_of_discards']}")
