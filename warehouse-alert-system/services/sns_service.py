import boto3
from config import Config

sns = boto3.client(
    'sns',
    aws_access_key_id=Config.AWS_ACCESS_KEY,
    aws_secret_access_key=Config.AWS_SECRET_KEY,
    region_name=Config.REGION
)

def send_alert(message):
    sns.publish(
        TopicArn=Config.SNS_TOPIC_ARN,
        Message=message,
        Subject="Low Stock Alert"
    )