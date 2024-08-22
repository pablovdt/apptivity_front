import requests

from api.api import Api


class PlaceApi(Api):
    endpoint_base = 'places/'

    def get_places_by_cp(self, cp: str):
        try:
            response = requests.get(url=f"{self.url}{self.endpoint_base}places/?city_cp={cp}")

            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")

    def get_place_by_id(self, place_id: str):
        try:
            response = requests.get(url=f"{self.url}{self.endpoint_base}place/{place_id}/")

            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")


place_api: PlaceApi = PlaceApi()
