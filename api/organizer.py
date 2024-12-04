import requests
import requests
import json
from api.api import Api
from utils import verify_hash_password


class OrganizerApi(Api):
    endpoint_base = 'organizers/'

    def get_organizers(self, name: str = None, city_id: int = None):

        url = f"{self.url}{self.endpoint_base}organizers/"

        if name:
            url += f"?name={name}"
        if city_id:
            url += f"?city_id={city_id}"

        try:
            response = requests.get(url=url)
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")

    def create_organizer(self, organizer: dict):

        try:
            response = requests.post(
                url=f'{self.url}{self.endpoint_base}create_organizer/',
                headers={"Content-Type": "application/json"},
                data=json.dumps(organizer)  # Convertir a JSON
            )
            return response

        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")

    def validate_organizer(self, organizer_email: str, organizer_password: str):

        response = requests.get(url=f"{self.url}{self.endpoint_base}organizer/password_by_email/{organizer_email}")

        if response.status_code == 200:

            stored_password = response.json()

            if verify_hash_password(password=organizer_password, stored_hased_password=stored_password):
                return True
            else:
                return False
        else:
            return False

    def get_organizer_basic_info(self, organizer_email):
        response = requests.get(url=f"{self.url}{self.endpoint_base}organizer_by_email/{organizer_email}")

        organizer_basic_info = response.json()

        return organizer_basic_info

    def get_user_coordinates(self, organizer_id: int):

        response = requests.get(url=f"{self.url}{self.endpoint_base}user_coordinates/{organizer_id}")

        if response.status_code == 200:
            return response.json()
        else:
            return None


organizer_api: OrganizerApi = OrganizerApi()
