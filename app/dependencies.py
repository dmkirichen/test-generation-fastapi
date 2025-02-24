import os
import boto3
from dotenv import load_dotenv

load_dotenv()
dynamodb = boto3.resource('dynamodb', 
                          region_name=os.getenv("AWS_REGION", "us-east-1"),
                          endpoint_url=os.getenv("DYNAMODB_ENDPOINT", "http://localhost:4566"))  # LocalStack
app_table = dynamodb.Table("AppData")
