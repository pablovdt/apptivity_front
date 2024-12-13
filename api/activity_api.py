import requests
import json
from api.api import Api


class ActivityApi(Api):
    endpoint_base = 'activities/'

    def create_activity(self, activity: dict):
        try:
            response = requests.post(
                f'{self.url}{self.endpoint_base}create_activity/',
                headers={"Content-Type": "application/json"},
                data=json.dumps(activity)  # Convertir a JSON
            )
            return response

        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")

    def update_activity(self, activity: dict, activity_id: str):
        try:
            response = requests.patch(
                f'{self.url}{self.endpoint_base}activities/activity/{activity_id}',
                headers={"Content-Type": "application/json"},
                data=json.dumps(activity)
            )
            return response

        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")

    def get_activities(self, is_date_order_asc: bool = True, date_from: str = None, activity_name: str = None,
                       place_id: int = None, cancelled: bool = False, organizer_id=None, order_by_assistance:bool = None, limit:int=None, date_to=None):

        url = f'{self.url}{self.endpoint_base}activities?'
        try:
            if organizer_id:
                url += f"&organizer_id={organizer_id}"

            if date_from:
                url += f'&date_from={date_from}'

            if date_to:
                url += f'&date_to={date_to}'

            if not is_date_order_asc:
                url += f"&is_date_order_asc=false"

            if activity_name:
                url += f'&name={activity_name}'

            if place_id:
                url += f'&place_id={place_id}'

            if cancelled:
                url += f'&cancelled=true'

            if organizer_id:
                url += f'&organizer_id={organizer_id}'

            if order_by_assistance:
                url += '&order_by_assistance=true'

            if limit:
                url += f'&limit={limit}'

            response = requests.get(url=url)

            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")

    def get_activities_by_month(self, organizer_id: int, year: int):

        url = f'{self.url}{self.endpoint_base}activities_by_month/?organizer_id={organizer_id}&year={year}'
        try:
            response = requests.get(url=url)

            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")

    def get_activities_by_city_id(self, city_id):
        url = f'{self.url}{self.endpoint_base}activities_by_city/?city_id={city_id}'
        try:
            response = requests.get(url=url)

            if response.status_code == 200:

                return response.json()
            else:
                return False

        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")

activiti_api: ActivityApi = ActivityApi()
