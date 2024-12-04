import streamlit as st
st.set_page_config(
    page_title="Apptivity",
    page_icon='',
    layout='wide',
    initial_sidebar_state="expanded"
)
from dotenv import load_dotenv

import pandas as pd
from datetime import datetime
from api.category_api import category_api
from api.place_api import place_api
from api.user_api import user_api



load_dotenv()
from auth import cookies

from menu import check_authenticated

check_authenticated()


st.title(f"Hola {cookies['organizer_name']}")

for _ in range(5):
    st.write("")


from datetime import datetime, timedelta
import pytz

from api.activity_api import activiti_api

activities = activiti_api.get_activities()

@st.dialog("Información")
def show_activity_details(i, row):
    st.subheader(row['name'])
    place = place_api.get_place_by_id(row["place_id"])
    if not place['location_url']:
        st.write(f'📍 **Lugar**: {place["name"]}')
    else:
        st.write(f'📍 **Lugar:** {place["name"]}. **Ubicación:** {place["location_url"]}')
    date_obj = datetime.fromisoformat(row['date'])
    st.write(f"📅 **Fecha:** {date_obj.strftime('%A, %d de %B de %Y')}")
    st.write(f"🕒 **Hora:** {date_obj.strftime('%H:%M:%S')}")
    st.write(f"💰 **Precio:** {row['price']} €")
    st.write(f"📝 **Descripción:** {row['description']}")
    category = category_api.get_category_by_id(row['category_id'])['name']
    st.write(f"🏷️ **Categoría:** {category}")
    if row['cancelled']:
        st.write(f"🚫 **CANCELADA !!**")
    colm1, colm2, colm3 = st.columns([2, 2, 2])
    with colm1:
        st.metric(label=f"👥 **Número de posibles asistencias:**", value=f"{row['number_of_possible_assistances']}")
    with colm2:
        st.metric(label=f"📤 **Número de envios:** ", value=f"{row['number_of_shipments']}")
    with colm3:
        st.metric(label=f"🗑️ **Número de descartes:**", value=f" {row['number_of_discards']}")
    st.image(row['image_path'])

    col1, _, col2 = st.columns([2, 2, 2])

    with col1:
        if st.button("Editar Actividad", key=f'edit{i}'):
            st.session_state['activity_to_repeat'] = row
            st.switch_page('pages/update_activity.py')
    with col2:
        if st.button("Repetir Actividad", key=f'repeat{i}'):
            st.session_state['activity_to_repeat'] = row
            st.switch_page('pages/create_activity.py')


def parse_date(date_str):
    return datetime.fromisoformat(date_str.replace('Z', '+00:00'))


local_tz = pytz.timezone('Europe/Madrid')  # Usando la zona horaria de Madrid como ejemplo

current_time = datetime.now(local_tz)
start_of_week = current_time - timedelta(days=current_time.weekday())
end_of_week = start_of_week + timedelta(days=6)


def count_activities_by_timeframe(activities):
    today_count = 0
    this_week_count = 0
    this_month_count = 0
    this_year_count = 0
    total_count = len(activities)

    for activity in activities:
        activity_date = parse_date(activity['date'])

        # if activity_date > current_time:
        if activity_date.date() == current_time.date():
            today_count += 1

        if start_of_week <= activity_date <= end_of_week:
            this_week_count += 1

        if activity_date.year == current_time.year and activity_date.month == current_time.month:
            this_month_count += 1

        if activity_date.year == current_time.year:
            this_year_count += 1

    return total_count, today_count, this_week_count, this_month_count, this_year_count


total, today, this_week, this_month, this_year = count_activities_by_timeframe(activities)

st.header("Vista rápida de Actividades")
with st.container(border=True):

    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 2])
    # todo, obtener las de dia, mes, semana, año pasado...para meterlo en el delta
    with col1:
        st.metric(label="📅 **Hoy**", value=today)
    with col2:
        st.metric(label="📅 **Esta semana**", value=this_week)
    with col3:
        st.metric(label="📅 **Este mes**", value=this_month)
    with col4:
        st.metric(label="📅 **Este año**", value=this_year)
    with col5:
        st.metric(label="📊 Total de actividades creadas", value=total, delta=None)

months_translation = {
    "January": "Enero",
    "February": "Febrero",
    "March": "Marzo",
    "April": "Abril",
    "May": "Mayo",
    "June": "Junio",
    "July": "Julio",
    "August": "Agosto",
    "September": "Septiembre",
    "October": "Octubre",
    "November": "Noviembre",
    "December": "Diciembre"
}

days_translation = {
    "Monday": "Lunes",
    "Tuesday": "Martes",
    "Wednesday": "Miércoles",
    "Thursday": "Jueves",
    "Friday": "Viernes",
    "Saturday": "Sábado",
    "Sunday": "Domingo"
}
activities_by_year = {}

for activity in activities:
    date_obj = datetime.fromisoformat(activity["date"])
    year_str = date_obj.strftime('%Y')
    month_str = date_obj.strftime('%B')
    day_str = date_obj.strftime('%A %d')

    if year_str not in activities_by_year:
        activities_by_year[year_str] = {}

    if month_str not in activities_by_year[year_str]:
        activities_by_year[year_str][month_str] = {}

    if day_str not in activities_by_year[year_str][month_str]:
        activities_by_year[year_str][month_str][day_str] = []

    activities_by_year[year_str][month_str][day_str].append(activity)

for year, months in sorted(activities_by_year.items()):
    with st.container():
        st.markdown(
            f"""
            <div style="background-color: #82b29a; padding: 2px; margin:20px; border-radius:1em; text-align:center;">
                <h2>{year}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )


    for month, days in sorted(months.items()):

        st.header(months_translation.get(month, month.capitalize()))

        for day, activities_in_day in sorted(days.items()):
            with st.container():
                st.markdown(f"<h4>{days_translation.get(day.split(' ')[0], day.split(' ')[0]).capitalize()} {day.split(' ')[-1]}</h4>", unsafe_allow_html=True)

            for i, activity in enumerate(activities_in_day):

                col1, col2 = st.columns([6, 1])
                with col1:
                    date_obj = datetime.fromisoformat(activity["date"])
                    time_str = date_obj.strftime('%H:%M')

                    div_html = f"""
                        <div style="border: 2px solid #82b29a; border-radius: 1em; padding: 7px; margin: 10px;
                                    background-color: #323232; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); text-align: center;">
                            <p style="font-size: 18px; color: #F3E8EB; font-weight: bold;">{time_str}</p>
                            <p style="font-size: 20px; color: #F3E8EB; font-weight: 600;">{activity['name']}</p>
                        </div>
                    """

                    st.markdown(div_html, unsafe_allow_html=True)

                with col2:
                    st.markdown("""
                        <style>
                            .stButton>button {
                                background-color: #82b29a;
                                color: white;
                                padding: 40px;  /* Aumenta el tamaño del botón */
                                font-size: 18px;  /* Aumenta el tamaño de la fuente */
                                border-radius: 1em;  /* Bordes redondeados */
                                border: none;  /* Sin borde */
                                cursor: pointer;  /* Cambia el cursor al pasar sobre el botón */
                            }
                            .stButton>button:hover {
                                background-color: #F3E8EB;  /* Color de fondo cuando el mouse pasa sobre el botón */
                            }
                        </style>
                    """, unsafe_allow_html=True)

                    # Crear el botón con Streamlit
                    if st.button("Ver Actividad", key=activity['name']):
                        show_activity_details(i, activity)



for _ in range(3):
    st.write("")

st.header("Actividades por mes")

from datetime import datetime

current_year = datetime.now().year

year = st.selectbox('Selecciona un año', [2020, 2021, 2022, 2023, 2024, 2025],
                    index=[2020, 2021, 2022, 2023, 2024, 2025].index(current_year))

activities_by_month = activiti_api.get_activities_by_month(year=year)

df = pd.DataFrame(list(activities_by_month.items()), columns=['Mes', 'Actividades'])

month_order = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
               'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

df['Mes'] = pd.Categorical(df['Mes'], categories=month_order, ordered=True)

df = df.sort_values('Mes')

for _ in range(5):
    st.write('')
st.line_chart(df.set_index('Mes')['Actividades'])

