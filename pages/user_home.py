import streamlit as st

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

st.header(f"Hola {cookies['user_name']}")

user_activities = user_api.get_user_activities(cookies['user_id'])

if user_activities:
    df = pd.DataFrame(user_activities)

    col1, col2 = st.columns(2)

    for i, (index, row) in enumerate(df.iterrows()):
        if i % 2 == 0:
            col = col1
        else:
            col = col2

        with col:

            with st.container(border=True):
                st.subheader(row['name'])

                place = place_api.get_place_by_id(row["place_id"])
                if not place['location_url']:
                    st.write(f'📍 **Lugar**: {place["name"]}')
                else:
                    st.write(f'📍 **Lugar**: {place["name"]}. **Ubicación**: {place["location_url"]}')

                date_obj = datetime.fromisoformat(row['date'])
                st.write(f"📅 **Fecha**: {date_obj.strftime('%A, %d de %B de %Y')}")
                st.write(f"🕒 **Hora**: {date_obj.strftime('%H:%M:%S')}")
                st.write(f"💰 **Precio**: {row['price']} €")

                st.write(f"📝 **Descripción**: {row['description']}")

                category = category_api.get_category_by_id(row['category_id'])['name']
                st.write(f"🏷️ **Categoría**: {category}")

                if row['cancelled']:
                    st.write(f"🚫 **CANCELADA!!**", color='red')

                st.image(row['image_path'], use_column_width=True)

else:
    st.info("Aquí aparecerán tus actividades")
