import streamlit as st

st.set_page_config(
    page_title="Apptivity - Actividades -",
    page_icon='',
    layout='centered',
    initial_sidebar_state="expanded"
)
from api.activity_api import activiti_api
from api.city_api import city_api

from menu import check_authenticated
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
from api.category_api import category_api
from api.place_api import place_api
from api.user_api import user_api

load_dotenv()
from auth import cookies

check_authenticated()

if cookies['user_role'] != 'true':
    st.stop()

st.header(f"Más actividades basadas en tus categorias...")

user_activities = user_api.get_more_activities(user_id=cookies['user_id'], user_categories=cookies['user_categories'])

if user_activities:
    st.write("¿Quieres editar tus categorias? Modificalo en Ajustes")

    df = pd.DataFrame(user_activities)

    df_sorted = df.sort_values(by='date', ascending=True)

    col1, col2 = st.columns(2)

    for i, (index, row) in enumerate(df_sorted.iterrows()):
        if i % 2 == 0:
            col = col1
        else:
            col = col2

        with col:

            with st.container(border=True):

                if row['assistance']:
                    st.markdown(f"<h2 style='color: #82b29a'>{row['name']}</h2>", unsafe_allow_html=True)
                elif row['assistance'] is None:
                    st.markdown(f"<h2>{row['name']}</h2>", unsafe_allow_html=True)

                place = place_api.get_place_by_id(row["place_id"])
                place_city_id = place["city_id"]

                city_name = city_api.get_city_by_id(place_city_id)['name']

                st.write(city_name)

                date_obj = datetime.fromisoformat(row['date'])
                st.write(f"📅 {date_obj.strftime('%d/%m/%Y')} 🕒 {date_obj.strftime('%H:%M')}")

                st.write(f"💰 {row['price']} €")

                if row.get('image_path'):
                    st.image(row['image_path'], use_column_width=True)

                if st.button(f"Añadir actividad a Inicio",key=row['id']):
                    user_api.add_user_activity(user_id=cookies['user_id'], activity_id=row['id'])
                    st.rerun()

else:
    st.info("Aquí aparecerán actividades de tu interés")
