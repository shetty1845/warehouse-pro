from services.dynamodb_service import create_user, get_user
from werkzeug.security import generate_password_hash, check_password_hash


def signup(username, password):
    try:
        existing_user = get_user(username)

        if existing_user:
            return False

        hashed_password = generate_password_hash(password)

        return create_user(username, hashed_password)

    except Exception as e:
        print("Signup Error:", e)
        return False


def login(username, password):
    try:
        user = get_user(username)

        if not user:
            return False

        return check_password_hash(user['password'], password)

    except Exception as e:
        print("Login Error:", e)
        return False
