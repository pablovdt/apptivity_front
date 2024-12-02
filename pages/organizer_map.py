import streamlit as st
st.set_page_config(
    page_title="Apptivity - Mapa-",
    page_icon='',
    layout='centered',
    initial_sidebar_state="expanded"
)
from dotenv import load_dotenv
from menu import check_authenticated
import pandas as pd
import numpy as np
import pydeck as pdk

load_dotenv()
from auth import cookies

check_authenticated()

if cookies['organizer_role'] != 'true':
    st.stop()

st.title("Consulta de donde procede tu turismo")

# Coordenadas de la ubicación central (puedes ajustarlas a tu ciudad o destino turístico)
latitude = 42.36   # Latitud de la ciudad de ejemplo (puedes cambiarla por la ciudad o lugar deseado)
longitude = -2.86  # Longitud de la ciudad de ejemplo (puedes cambiarla por la ciudad o lugar deseado)

# Aquí debes pasar los datos de latitud y longitud de las ubicaciones de los turistas
# Ejemplo de datos que puedes pasar:
tourism_data = pd.DataFrame({
    "lat": [40.7128, 51.5074, 48.8566, 34.0522, 35.6895],  # Latitudes de origen de los turistas
    "lon": [-74.0060, -0.1278, 2.3522, -118.2437, 139.6917],  # Longitudes de origen de los turistas
})

# Mapa de la ciudad con los puntos de turismo
st.pydeck_chart(
    pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=latitude,
            longitude=longitude,
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=tourism_data,
                get_position="[lon, lat]",
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
            pdk.Layer(
                "ScatterplotLayer",
                data=tourism_data,
                get_position="[lon, lat]",
                get_color="[200, 30, 0, 160]",
                get_radius=200,
            ),
        ],
    )
)