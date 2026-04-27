import boto3
from config import Config

# ✅ NO KEYS (IAM ROLE USED)
sns = boto3.client(
    'sns',
    region_name=Config.REGION
)

def send_alert(message):
    try:
        sns.publish(
            TopicArn=Config.SNS_TOPIC_ARN,
            Message=message,
            Subject="Low Stock Alert"
        )
    except Exception as e:
        print("SNS Error:", e)
