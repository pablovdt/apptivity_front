import requests
import json
import random
from utils import hash_password
if __name__ == '__main__':

    # categories = [
    #     {"name": "Vino"},
    #     {"name": "Deporte"},
    #     {"name": "Coche"},
    #     {"name": "Moto"},
    #     {"name": "Paseo"},
    #     {"name": "Senderismo"},
    #     {"name": "Ciclismo"},
    #     {"name": "Pesca"},
    #     {"name": "Caza"},
    #     {"name": "Aventura"},
    #     {"name": "Agroturismo"},
    #     {"name": "Equitación"},
    #     {"name": "Observación de aves"},
    #     {"name": "Camping"},
    #     {"name": "Escalada"},
    #     {"name": "Navegación"},
    #     {"name": "Fotografía rural"},
    #     {"name": "Relax"},
    #     {"name": "Trekking"},
    #     {"name": "Gastronomía local"},
    #     {"name": "Recolección de setas"},
    #     {"name": "Arte y cultura local"},
    #     {"name": "Vía ferrata"},
    #     {"name": "Rutas en 4x4"},
    #     {"name": "Turismo rural"},
    #     {"name": "Caballos"},
    #     {"name": "Conducción en la naturaleza"},
    #     {"name": "Talleres artesanales"},
    #     {"name": "Rutas gastronómicas"},
    #     {"name": "Termalismo"},
    #     {"name": "Relax en la naturaleza"},
    #     {"name": "Degustación de vinos"},
    #     {"name": "Cata de aceites"},
    #     {"name": "Talleres de cocina tradicional"},
    #     {"name": "Mercados locales"},
    #     {"name": "Fiestas populares"},
    #     {"name": "Rutas de queso"},
    #     {"name": "Recogida de frutas"},
    #     {"name": "Catas de productos locales"},
    #     {"name": "Visitas a bodegas"},
    #     {"name": "Rutas de miel"},
    #     {"name": "Jornadas de caza y pesca"},
    #     {"name": "Festivales rurales"},
    #     {"name": "Senderismo en la naturaleza"},
    #     {"name": "Visita a granjas"},
    #     {"name": "Arte rural"},
    #     {"name": "Días de campo"},
    #     {"name": "Excursiones en tractor"},
    #     {"name": "Rutas en quad"},
    #     {"name": "Paseos en carro"},
    #     {"name": "Actividades en granja"},
    #     {"name": "Fiestas de la cosecha"},
    #     {"name": "Escapadas rurales"},
    #     {"name": "Rutas en bici de montaña"},
    #     {"name": "Convivencia con animales de granja"},
    #     {"name": "Rutas por los campos"},
    #     {"name": "Observación de estrellas"},
    #     {"name": "Fiestas de tradiciones locales"},
    #     {"name": "Jornadas de intercambio cultural"},
    #     {"name": "Ruta de los embutidos"},
    #     {"name": "Catas de cerveza artesanal"},
    #     {"name": "Talleres de cerámica"},
    #     {"name": "Recreación histórica"},
    #     {"name": "Rutas por caminos rurales"},
    #     {"name": "Vuelta en carreta tirada por caballos"},
    #     {"name": "Visitas a museos rurales"},
    #     {"name": "Talleres de cestería"},
    #     {"name": "Escuelas de oficios tradicionales"},
    #     {"name": "Rutas de pastores"},
    #     {"name": "Rutas por viñedos"},
    #     {"name": "Caminos del vino"},
    #     {"name": "Convivencia en aldeas"}
    # ]
    #
    # for category in categories:
    #     try:
    #         response = requests.post(url='http://localhost:8000/categories/create_category/',  data=json.dumps(category))
    #         print(response.status_code)
    #     except requests.exceptions.RequestException as e:
    #         print(f"Error en la solicitud: {e}")
    #

    def generate_name():
        first_names = ["Juan", "Ana", "Pedro", "Maria", "Carlos", "Laura", "Jose", "Lucia", "Miguel", "Sofia"]
        last_names = ["Gomez", "Martinez", "Lopez", "Perez", "Fernandez", "Gonzalez", "Rodriguez", "Sanchez", "Garcia",
                      "Hernandez"]
        return f"{random.choice(first_names)} {random.choice(last_names)}"


    # Función para generar un correo electrónico
    def generate_email(name):
        name_parts = name.split()
        return f"{name_parts[0].lower()}.{name_parts[1].lower()}@mail.com"



    # Generar 100 usuarios de ejemplo
    users = []
    for _ in range(100):
        name = generate_name()
        email = generate_email(name)
        password = hash_password("123456")
        city_id = random.randint(1, 174)

        # Generar category_ids (con muchos 1, como se indicó)
        categories_ids = [random.randint(1, 72) for _ in
                          range(random.randint(1, 5))]  # Entre 1 y 5 categorías por usuario
        if random.random() < 0.7:  # 70% de probabilidad de que al menos un ID de categoría sea 1
            categories_ids.append(1)

        # Crear el diccionario de datos del usuario
        data = {
            "name": name,
            "city_id": city_id,
            "email": email,
            "password": password,
            "category_ids": list(set(categories_ids)),  # Eliminamos duplicados
            "settings": "",
            "notification_distance": 20
        }

        users.append(data)

        # Realizar la solicitud POST para crear el usuario
        try:
            response = requests.post(
                url='http://localhost:8000/users/create_user/',
                data=json.dumps(data),
                headers={'Content-Type': 'application/json'}
            )
            print(f"Usuario {name} creado, status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error al crear usuario {name}: {e}")
