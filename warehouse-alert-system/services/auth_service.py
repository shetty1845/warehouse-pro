from services.dynamodb_service import create_user, get_user
from werkzeug.security import generate_password_hash, check_password_hash


# -----------------------------
# 📝 SIGNUP FUNCTION
# -----------------------------
def signup(username, password):
    try:
        # Check if user already exists
        existing_user = get_user(username)

        if existing_user:
            return False

        # 🔐 Hash password before storing
        hashed_password = generate_password_hash(password)

        # Create user
        success = create_user(username, hashed_password)

        return success

    except Exception as e:
        print("Signup Error:", e)
        return False


# -----------------------------
# 🔐 LOGIN FUNCTION
# -----------------------------
def login(username, password):
    try:
        user = get_user(username)

        if not user:
            return False

        # 🔐 Compare hashed password
        if check_password_hash(user['password'], password):
            return True

        return False

    except Exception as e:
        print("Login Error:", e)
        return False