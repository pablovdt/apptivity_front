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

    def update_user(self, user_id, data:dict):
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


    def get_user_activities(self, user_id: int):

        response = requests.get(url=f"{self.url}{self.endpoint_base}{user_id}/activities")

        return response.json()

    def update_assistance(self, user_id: int, activity_id: int, assistance):

        # users/10/activities/10/assistance?assistance=false

        response = requests.patch(url=f"{self.url}{self.endpoint_base}{user_id}/activities/{activity_id}/{assistance}")

        if response.status_code == 200:

            return True

user_api: UserApi = UserApi()
