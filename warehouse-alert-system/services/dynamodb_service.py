import boto3
from config import Config
import uuid
from datetime import datetime
from boto3.dynamodb.conditions import Key


# -----------------------------
# 🔌 CONNECT TO DYNAMODB
# -----------------------------
dynamodb = boto3.resource(
    'dynamodb',
    region_name=Config.REGION   # Uses aws configure credentials
)

users_table = dynamodb.Table(Config.USERS_TABLE)
items_table = dynamodb.Table(Config.ITEMS_TABLE)


# -----------------------------
# 👤 USER FUNCTIONS
# -----------------------------

def create_user(username, password, email=""):
    try:
        users_table.put_item(Item={
            'user_id': f"USER-{uuid.uuid4()}",
            'username': username,
            'password': password,
            'email': email,
            'role': 'user',
            'created_at': datetime.utcnow().isoformat()
        })
        return True
    except Exception as e:
        print("Create User Error:", e)
        return False


def get_user(username):
    try:
        response = users_table.query(
            IndexName='username-index',  # Make sure this exists
            KeyConditionExpression=Key('username').eq(username)
        )

        items = response.get('Items', [])

        if items:
            return items[0]

        return None

    except Exception as e:
        print("Get User Error:", e)
        return None


# -----------------------------
# 📦 INVENTORY FUNCTIONS
# -----------------------------

def add_item(name, quantity, threshold, category="General", unit="pcs"):
    try:
        items_table.put_item(Item={
            'item_id': f"ITEM-{uuid.uuid4()}",
            'name': name,
            'category': category,
            'quantity': int(quantity),
            'threshold': int(threshold),
            'unit': unit,
            'created_at': datetime.utcnow().isoformat(),
            'last_updated': datetime.utcnow().isoformat()
        })
        return True
    except Exception as e:
        print("Add Item Error:", e)
        return False


def get_items():
    try:
        response = items_table.scan()
        return response.get('Items', [])
    except Exception as e:
        print("Get Items Error:", e)
        return []


def update_stock(item_id, quantity):
    try:
        items_table.update_item(
            Key={'item_id': item_id},
            UpdateExpression="""
                SET quantity = :q,
                    last_updated = :t
            """,
            ExpressionAttributeValues={
                ':q': int(quantity),
                ':t': datetime.utcnow().isoformat()
            }
        )
        return True
    except Exception as e:
        print("Update Stock Error:", e)
        return False


def delete_item(item_id):
    try:
        items_table.delete_item(
            Key={'item_id': item_id}
        )
        return True
    except Exception as e:
        print("Delete Item Error:", e)
        return False


# -----------------------------
# 🔍 SEARCH FUNCTION
# -----------------------------

def search_items(query):
    try:
        items = get_items()
        return [
            item for item in items
            if query.lower() in item.get('name', '').lower()
        ]
    except Exception as e:
        print("Search Error:", e)
        return []