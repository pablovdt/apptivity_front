import requests
import requests
import json
from api.api import Api


class CategoryApi(Api):
    endpoint_base = 'categories/'

    def get_categories(self):
        try:
            response = requests.get(url=f"{self.url}{self.endpoint_base}categories/")

            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")

    def get_category_by_id(self, category_id: str):
        try:
            response = requests.get(url=f"{self.url}{self.endpoint_base}category/{category_id}/")

            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")


category_api: CategoryApi = CategoryApi()
