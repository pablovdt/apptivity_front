import requests
import json
from api.api import Api


class PlaceApi(Api):
    endpoint_base = 'places/'

    def insert_place(self, name: str, location: str, city_id: int):  # Cambiar str por int
        try:
            data = {
                "name": name,
                "city_id": city_id,
                "location_url": location
            }
            print(json.dumps(data))
            response = requests.post(
                f"{self.url}{self.endpoint_base}create_place/",
                headers={"Content-Type": "application/json"},
                data=json.dumps(data)
            )
            if response.status_code == 201:
                return True
            else:
                print(response.json())
                return False
        except Exception as e:
            print(f"Error: {e}")
            return False

    def get_places_by_id(self, place_id: str):
        try:
            response = requests.get(url=f"{self.url}{self.endpoint_base}places/?city_id={place_id}")

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
