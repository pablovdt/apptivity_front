import requests
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

    def get_user_activities(self, user_id: int, all: bool, date_from: str = None, is_date_order_asc: bool = None):

        url = f"{self.url}{self.endpoint_base}{user_id}/activities/?all={all}"

        if date_from:
            url += f'&date_from={date_from}'

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

    def get_more_activities(self, user_id: int, user_categories):

        user_categories_p = json.loads(user_categories)

        user_categories_ids = [cat_id['id'] for cat_id in user_categories_p]

        url = f"{self.url}{self.endpoint_base}more_activities?user_id={user_id}"

        for category_id in user_categories_ids:
            url += f"&categories_ids={category_id}"

        response = requests.get(url=url)

        if response.status_code == 200:

            return response.json()
        else:
            return None


user_api: UserApi = UserApi()
