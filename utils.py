import base64

import bcrypt


def set_background_image(image_path):
    pass


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password.decode('utf-8')


def verify_hash_password(password: str, stored_hased_password: str) -> bool:
    if bcrypt.checkpw(password.encode('utf-8'), stored_hased_password.encode('utf-8')):
        return True
    else:
        return False


def add_one_year(date):
    """Añadir un año a la fecha dada."""
    try:
        # Calcular el próximo año
        next_year = date.year + 1

        # Manejar el caso del 29 de febrero en años no bisiestos
        # Si la fecha original es el 29 de febrero y el próximo año no es bisiesto, ajustar a 28 de febrero
        if date.month == 2 and date.day == 29:
            try:
                return date.replace(year=next_year)
            except ValueError:
                # Ajustar el 29 de febrero a 28 de febrero si el próximo año no es bisiesto
                return date.replace(year=next_year, day=28)

        return date.replace(year=next_year)
    except ValueError as e:
        # Manejar errores si la fecha no es válida
        print(f"Error al añadir un año a la fecha: {e}")
        return date
