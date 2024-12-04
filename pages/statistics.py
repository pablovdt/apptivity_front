import streamlit as st
st.set_page_config(
    page_title="Apptivity - Estadisticas -",
    page_icon='',
    layout='centered',
    initial_sidebar_state="expanded"
)
import pandas as pd
from dotenv import load_dotenv

from api.activity_api import activiti_api
from api.category_api import category_api



load_dotenv()
from auth import cookies
from menu import check_authenticated

check_authenticated()

from auth import cookies
if cookies['organizer_role'] != 'true':
    st.stop()

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


# metrics

total_shipments = 0
total_assistances = 0
total_possible_assistances = 0

activities = activiti_api.get_activities()

categorias = set()

for activity in activities:
    category = category_api.get_category_by_id(activity['category_id'])
    categorias.add(category['name'])

    total_shipments += activity['number_of_shipments']
    total_assistances += activity['number_of_assistances']
    total_possible_assistances += activity['number_of_possible_assistances']

if total_shipments > 0:
    porcentaje_asistencia = (total_assistances / total_shipments) * 100
else:
    porcentaje_asistencia = 0.0

if total_possible_assistances > 0:
    porcentaje_cumplimiento = (total_assistances / total_possible_assistances) * 100
else:
    porcentaje_cumplimiento = 0.0


st.header("Categorías de tus actividades:")
for categoria in categorias:
    st.write(categoria)


st.header("Porcentajes de asistencias")

col1, col2 = st.columns([2, 2])

with col1:
    st.metric(label="Porcentaje de asistencia", value=f"{porcentaje_asistencia:.1f}%", delta=None)
with col2:
    st.metric(label="Porcentaje de cumplimiento", value=f"{porcentaje_cumplimiento:.1f}%", delta=None)