import streamlit as st
from dotenv import load_dotenv
import json

from api.category_api import category_api
from api.user_api import user_api

st.set_page_config(
    page_title="Apptivity - Ajustes -",
    page_icon='',
    layout='centered',
    initial_sidebar_state="expanded"
)

load_dotenv()

from menu import check_authenticated

check_authenticated()

from auth import cookies

if cookies['user_role'] != 'true':
    st.stop()

categories: list = category_api.get_categories()
categories_options = {category["name"]: category["id"] for category in categories}

categories = json.loads(cookies['user_categories'])

if categories:
    st.header("Tus categorías favoritas")

    category_names = [category['name'] for category in categories]

    col1, col2 = st.columns(2)

    with col1:
        for i, category in enumerate(category_names[:len(category_names) // 2]):
            st.button(category, key=f"category_{i}", help=f"Ver más sobre {category}")

    with col2:
        for i, category in enumerate(category_names[len(category_names) // 2:]):
            st.button(category, key=f"category_{i + len(category_names) // 2}", help=f"Ver más sobre {category}")

else:
    st.info("No tienes categorías favoritas aún.")

for _ in range(3):
    st.write("")

st.subheader("Añade más categorías")

categories_selected = st.multiselect("Categorías", list(categories_options.keys()))

categories_ids = [categories_options[cat] for cat in categories_selected]

if st.button("Añadir categorias seleccionadas"):

    user_categories = json.loads(cookies['user_categories'])

    user_category_ids = [category['id'] for category in user_categories]

    merged_categories = list(set(categories_ids + user_category_ids))

    response = user_api.update_user(user_id=cookies['user_id'], data={
        "categories": merged_categories
    })

    if response.status_code == 200:

        user_basic_info: dict = user_api.get_user_basic_info(cookies['user_email'])
        cookies['user_categories'] = json.dumps(user_basic_info['categories'])

        cookies.save()
        st.rerun()

    else:
        st.error("Ocurrió un error. Intentelo de nuevo mas tarde")

for _ in range(6):
    st.write("")

st.header(f"Distancia de Notificación - {cookies['user_notification_distance']} Km -")
st.write('Ajusta para enterarte de las actividades más cercanas')

new_notification_distance = st.slider("Distancia - Km -", min_value=10, max_value=100, step=1, value=int(cookies['user_notification_distance']))

if st.button("Editar distancia de notificación",
             help=f'Se te mostrarán las actividades en un radio de {new_notification_distance} km respecto a tu municipio.'):

    response = user_api.update_user(user_id=cookies['user_id'], data={
        "notification_distance": new_notification_distance
    })

    if response.status_code == 200:

        user_basic_info: dict = user_api.get_user_basic_info(cookies['user_email'])
        cookies['user_notification_distance'] = str(user_basic_info['notification_distance'])

        cookies.save()
        st.rerun()

    else:
        st.error("Ocurrió un error. Intentelo de nuevo mas tarde")
