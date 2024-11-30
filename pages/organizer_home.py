import streamlit as st
st.set_page_config(
    page_title="Apptivity",
    page_icon='',
    layout='centered',
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


st.header(f"Hola {cookies['organizer_name']}")

st.image(cookies['organizer_image_path'])

from datetime import datetime, timedelta
import pytz

from api.activity_api import activiti_api

activities = activiti_api.get_activities()


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

        if activity_date > current_time:
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

col1, col2 = st.columns([3, 3])

with col1:
    with st.container(border=True):
        st.subheader("Próximas Actividades")

        st.metric(label="📅 **Hoy**", value=today)

        st.metric(label="📅 **Esta semana**", value=this_week)

        st.metric(label="📅 **Este mes**", value=this_month)

        st.metric(label="📅 **Este año**", value=this_year)

with col2:
    with st.container(border=True):
        st.subheader("Total")

        st.metric(label="📊 Total de actividades", value=total, delta=None)
