import streamlit as st

st.set_page_config(
    page_title="Apptivity - Mapa-",
    page_icon='',
    layout='centered',
    initial_sidebar_state="expanded"
)
from collections import Counter
from api.organizer import organizer_api

import numpy as np
from dotenv import load_dotenv
from menu import check_authenticated
import pandas as pd
import pydeck as pdk

load_dotenv()
from auth import cookies

check_authenticated()

if cookies['organizer_role'] != 'true':
    st.stop()

st.title("Consulta de donde procede tu turismo")
st.write("Basado en los municipios de los usuarios que asisten a tus actividades")

user_coordinates = organizer_api.get_user_coordinates(cookies['organizer_id'])

if user_coordinates:

    # Convertir las coordenadas en un DataFrame
    latitudes = [coord['latitude'] for coord in user_coordinates]
    longitudes = [coord['longitude'] for coord in user_coordinates]

    tourism_data = pd.DataFrame({
        "lat": latitudes,
        "lon": longitudes
    })

    # Visualización del mapa
    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",  # Estilo del mapa
            initial_view_state=pdk.ViewState(
                latitude=float(cookies['organizer_latitude']),
                longitude=float(cookies['organizer_longitude']),
                zoom=9,
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
                    get_color="[130, 178, 154, 160]",  # 82b29a
                    get_radius=200,
                ),
            ],
        )
    )


    city_names = [user['city_name'] for user in user_coordinates]

    city_counts = Counter(city_names)

    data = [{'Municipio': city, 'Nº de Usuarios': count} for city, count in city_counts.items()]

    df = pd.DataFrame(data)

    df = df.sort_values(by='Nº de Usuarios', ascending=False)

    df = df.reset_index(drop=True)

    for _ in range(5):
        st.write("")


    st.dataframe(df, use_container_width=True, hide_index=True)  # Aquí usamos hide_index=True
else:
    st.info("Cuando crees actividades, aqui podrás ver en un mapa de donde proceden las personas interesadas en ellas")