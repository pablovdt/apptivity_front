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

    def get_activities(self, is_date_order_asc: bool = True, date_from: str = None):

        url = f'{self.url}{self.endpoint_base}activities?organizer_id={cookies["organizer_id"]}'
        try:
            if date_from:
                url += f'&date_from={date_from}'

            if not is_date_order_asc:
                url += f"&is_date_order_asc=false"

            response = requests.get(url=url)

            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")


activiti_api: ActivityApi = ActivityApi()
