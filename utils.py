import base64

import bcrypt


def set_background_image(image_path):
    pass

def hash_password(password: str)-> str:
    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password.decode('utf-8')

def verify_hash_password(password: str, stored_hased_password: str)-> bool:
    if bcrypt.checkpw(password.encode('utf-8'), stored_hased_password.encode('utf-8')):
        return True
    else:
        return False