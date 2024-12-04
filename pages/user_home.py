import streamlit as st

from api.city_api import city_api

st.set_page_config(
    page_title="Apptivity",
    page_icon='',
    layout='centered',
    initial_sidebar_state="expanded"
)
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

st.header(f"{cookies['user_name']}, tus actividades:")

user_activities = user_api.get_user_activities(cookies['user_id'], all=False,
                                               date_from=datetime.now().strftime("%Y-%m-%d"))


@st.dialog("Información")
def show_activity_details(item):
    place = place_api.get_place_by_id(item["place_id"])
    if not place['location_url']:
        st.write(f'📍 **Lugar**: {place["name"]}')
    else:
        st.write(f'📍 **Lugar**: {place["name"]}. **Ubicación**: {place["location_url"]}')

    st.write(f"♜ **Organizador**: {item['organizer_name']}")
    date_obj = datetime.fromisoformat(item['date'])
    st.write(f"📅 **Fecha**: {date_obj.strftime('%A, %d de %B de %Y')}")
    st.write(f"🕒 **Hora**: {date_obj.strftime('%H:%M:%S')}")
    st.write(f"💰 **Precio**: {item['price']} €")

    st.write(f"📝 **Descripción**: {item['description']}")

    category = category_api.get_category_by_id(item['category_id'])['name']
    st.write(f"🏷️ **Categoría**: {category}")

    if item['cancelled']:
        st.write(f"🚫 **CANCELADA!!**", color='red')

    st.image(item['image_path'], use_column_width=True)

    col_button_1, col_button_2, col_button_3 = st.columns([2, 2, 2])

    with col_button_1:
        if st.button("Asistiré"):
            if user_api.update_possible_assistance(user_id=cookies['user_id'], activity_id=item['id'], possible_assistance=True):
                st.rerun()

    with col_button_2:

        if st.button("No lo sé"):
            if user_api.update_possible_assistance(user_id=cookies['user_id'], activity_id=item['id'], possible_assistance=None):
                st.rerun()

    with col_button_3:
        if st.button("No Asistiré"):
            if user_api.update_possible_assistance(user_id=cookies['user_id'], activity_id=item['id'], possible_assistance=False):
                st.rerun()


if user_activities:
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

                if row['possible_assistance']:
                    st.markdown(f"<h2 style='color: #82b29a'>{row['name']}</h2>", unsafe_allow_html=True)
                elif row['possible_assistance'] is None:
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

                if st.button(f"Ver actividad - {row['name']}"):
                    show_activity_details(row)


else:
    st.info("Aquí aparecerán tus actividades")
