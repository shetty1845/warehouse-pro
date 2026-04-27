import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    REGION = os.getenv("AWS_REGION")

    USERS_TABLE = os.getenv("DYNAMODB_USERS_TABLE")
    ITEMS_TABLE = os.getenv("DYNAMODB_ITEMS_TABLE")

    SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN")

    SECRET_KEY = os.getenv("SECRET_KEY")