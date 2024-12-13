import requests
import json
from api.api import Api

from utils import verify_hash_password


class UserApi(Api):
    endpoint_base = 'users/'

    def create_user(self, user: dict):

        try:
            response = requests.post(
                url=f'{self.url}{self.endpoint_base}create_user/',
                headers={"Content-Type": "application/json"},
                data=json.dumps(user)  # Convertir a JSON
            )
            return response

        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")

    def add_user_activity(self, user_id: int, activity_id: int):
        try:
            response = requests.post(
                url=f'{self.url}{self.endpoint_base}add_user_activity?user_id={user_id}&activity_id={activity_id}'
            )

            return response
        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")

    def organizer_subscribe(self, organizer_id: int, user_id: int):

        try:
            requests.post(
                url=f'{self.url}{self.endpoint_base}add_user_organizer?user_id={user_id}&organizer_id={organizer_id}'
            )

            return True
        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")
            return False

    def update_user(self, user_id, data: dict):
        try:
            response = requests.patch(
                url=f'{self.url}{self.endpoint_base}user/{user_id}',
                headers={"Content-Type": "application/json"},
                data=json.dumps(data)  # Convertir a JSON
            )
            return response

        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")

    def validate_user(self, user_email: str, user_password: str):
        response = requests.get(url=f"{self.url}{self.endpoint_base}user/password_by_email/{user_email}")

        if response.status_code == 200:

            stored_password = response.json()

            if verify_hash_password(password=user_password, stored_hased_password=stored_password):
                return True
            else:
                return False
        else:
            return False

    def get_user_basic_info(self, user_email):
        response = requests.get(url=f"{self.url}{self.endpoint_base}user_by_email/{user_email}")

        user_basic_info = response.json()

        return user_basic_info

    def get_user_activities(self, user_id: int, all: bool, date_from: str = None, is_date_order_asc: bool = None, date_to=None):

        url = f"{self.url}{self.endpoint_base}{user_id}/activities/?all={all}"

        if date_from:
            url += f'&date_from={date_from}'

        if date_to:
            url += f'&date_to={date_to}'

        if is_date_order_asc:
            url += f"&is_date_order_asc=true"
        else:
            url += f"&is_date_order_asc=false"

        response = requests.get(url=url)

        return response.json()

    def update_possible_assistance(self, user_id: int, activity_id: int, possible_assistance):
        update_assistance_url = f"{self.url}{self.endpoint_base}{user_id}/activities/{activity_id}"

        params = {}
        if possible_assistance is not None:
            params['possible_assistance'] = possible_assistance

        response = requests.patch(url=update_assistance_url, params=params)

        if response.status_code == 200:
            return True
        else:
            response.raise_for_status()

    def get_more_activities(self, user_id: int, user_categories=None):

        url = f"{self.url}{self.endpoint_base}more_activities?user_id={user_id}"

        if user_categories:
            user_categories_p = json.loads(user_categories)

            user_categories_ids = [cat_id['id'] for cat_id in user_categories_p]

            for category_id in user_categories_ids:
                url += f"&categories_ids={category_id}"

        response = requests.get(url=url)

        if response.status_code == 200:

            return response.json()
        else:
            return None

    def get_subscribe_organizers(self, user_id: int):

        url = f"{self.url}{self.endpoint_base}{user_id}/organizers/"

        response = requests.get(url=url)

        return response.json()

    def get_activities_updated(self, user_id):

        url = f'{self.url}{self.endpoint_base}{user_id}/activities_updated'

        response = requests.get(url=url)

        if response.status_code == 200:

            return response.json()
        else:
            return False

    def post_activity_updated_confirmed(self, user_id, activity_id, updated_confirmed: bool):

        url = f"{self.url}{self.endpoint_base}{user_id}/user_activities/{activity_id}?updated_confirmed={updated_confirmed}"

        requests.patch(url)

    def validate_qr_and_location(self, activity_id: int, organizer_id: int, user_id: int, latitude: float,
                                 longitude: float):
        try:
            data = {"activity_id": activity_id,
                    "organizer_id": organizer_id,
                    "user_id": user_id,
                    "latitude": latitude,
                    "longitude": longitude
                    }

            response = requests.post(
                url=f'{self.url}{self.endpoint_base}validate_qr_and_location/',
                headers={"Content-Type": "application/json"},
                data=json.dumps(data)
            )
            return response

        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")

    def get_user_assistances(self, user_id: int):

        url = f'{self.url}{self.endpoint_base}{user_id}/assistances'

        response = requests.get(url=url)

        if response.status_code == 200:

            return response.json()
        else:
            return False

user_api: UserApi = UserApi()
