import boto3
import os
import uuid

# Ensure AWS region is set
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

# LocalStack DynamoDB connection
dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:4566')
table = dynamodb.Table("AppData")

# Dummy users
users = [
    {"user_id": str(uuid.uuid4()), "username": "Alice"},
    {"user_id": str(uuid.uuid4()), "username": "Bob"},
    {"user_id": str(uuid.uuid4()), "username": "Charlie"},
]

# Dummy test papers
test_papers = [
    {"questions": {"q1": "A", "q2": "B"}},
    {"questions": {"q1": "C", "q2": "D"}},
]

# Populate users
for user in users:
    table.put_item(Item={
        "PK": f"USER#{user['user_id']}",
        "SK": "METADATA",
        "username": user["username"],
    })

    # Assign tests to each user
    for test in test_papers:
        test_id = str(uuid.uuid4())
        table.put_item(Item={
            "PK": f"USER#{user['user_id']}",
            "SK": f"TEST#{test_id}",
            "questions": test["questions"],
            "answers": {},
            "score": 0
        })

print("Database populated successfully!")
