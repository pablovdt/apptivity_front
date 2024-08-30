import requests
import json
from api.api import Api

from auth import cookies


class ActivityApi(Api):
    endpoint_base = 'activities/'

    def create_activity(self, activity: dict):
        # Enviar solicitud POST
        try:
            response = requests.post(
                'http://localhost:8000/activities/create_activity/',
                headers={"Content-Type": "application/json"},
                data=json.dumps(activity)  # Convertir a JSON
            )
            return response

        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")

    def update_activity(self, activity: dict, activity_id: str):
        try:
            response = requests.patch(
                f'http://localhost:8000/activities/activity/{activity_id}',
                headers={"Content-Type": "application/json"},
                data=json.dumps(activity)
            )
            return response

        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")

    def get_activities(self, is_date_order_asc: bool = True, date_from: str = None, activity_name: str = None,
                       place_id: int = None, cancelled: bool = False):

        url = f'{self.url}{self.endpoint_base}activities?organizer_id={cookies["organizer_id"]}'
        try:
            if date_from:
                url += f'&date_from={date_from}'

            if not is_date_order_asc:
                url += f"&is_date_order_asc=false"

            if activity_name:
                url += f'&name={activity_name}'

            if place_id:
                url += f'&place_id={place_id}'

            if cancelled:
                url += f'&cancelled=true'

            response = requests.get(url=url)

            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")


activiti_api: ActivityApi = ActivityApi()
