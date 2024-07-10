import datetime
import os

import bcrypt
import jwt
from dotenv import load_dotenv

from errors.user_not_found import UserNotFound
from errors.wrong_password import WrongPassword
from services.user import UserService

load_dotenv()
user_service = UserService()


def login(username, password):
    try:
        user = user_service.get_user(username)
        if user:
            password_is_correct = check_password(password, user["password"])
            if not password_is_correct:
                raise WrongPassword()

            token = generate_token({"username": username})
            return True, user, token

        raise UserNotFound()
    except Exception as e:
        print(e)
        return False, None, None


def sing_up(username, name, password):
    password_hashed = hash_password(password)

    exists_user = user_service.get_user(username)

    if exists_user:
        return False, "User already exists", None

    user_service.insert_user(
        {"username": username, "password": password_hashed, "name": name})

    user = user_service.get_user(username)
    del user["password"]

    token = generate_token({"username": username})

    return True, token, user


def hash_password(password):
    salt = bcrypt.gensalt()

    password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)

    return password_hash


def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)


def valid_token(token):
    is_valid, _ = decode_token(token)
    return is_valid


def generate_token(payload):
    secret_key = os.getenv('SECRET_KEY_JWT')

    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token


def decode_token(token):
    secret_key = os.getenv('SECRET_KEY_JWT')

    try:
        decoded_payload = jwt.decode(
            token, secret_key, algorithms=['HS256'])
        return True, decoded_payload
    except jwt.ExpiredSignatureError:
        return False, "Token expirado"
    except jwt.InvalidTokenError:
        return False, "Token inválido"
