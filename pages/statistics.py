import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from api.activity_api import activiti_api


st.set_page_config(
    page_title="Apptivity - Estadisticas -",
    page_icon='',
    layout='centered',
    initial_sidebar_state="expanded"
)

load_dotenv()
from auth import cookies
from menu import check_authenticated

check_authenticated()

st.title("Actividades por mes")

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
