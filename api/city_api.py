
import requests
from api.api import Api


class CityApi(Api):
    endpoint_base = 'cities/'

    def get_cities(self):
        try:
            response = requests.get(url=f"{self.url}{self.endpoint_base}cities")
            print(f"{self.url}{self.endpoint_base}cities")
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")

    def get_city_by_id(self, city_id: int):

        try:
            response = requests.get(url=f"{self.url}{self.endpoint_base}city/id/{city_id}")

            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")


city_api: CityApi = CityApi()
