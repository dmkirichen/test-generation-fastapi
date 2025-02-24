from .dependencies import app_table
import uuid

def create_user(username, password_hash):
    user_id = str(uuid.uuid4())
    app_table.put_item(
        Item={
            "PK": f"USER#{user_id}",
            "SK": "METADATA",
            'username': username,
            'password_hash': password_hash
        }
    )
    return user_id

def get_user_by_username(username):
    response = app_table.scan(
        FilterExpression='username = :u', ExpressionAttributeValues={":u": username})
    return response['Items'][0] if response['Items'] else None

def save_test(user_id, questions):
    test_id = str(uuid.uuid4())
    app_table.put_item(
        Item={
            "PK": f"USER#{user_id}",
            "SK": f"TEST#{test_id}",
            'test_id': test_id,
            'questions': questions,
            'answers': {},
            'score': 0
        }
    )
    return test_id

def submit_test(user_id, test_id, user_answers):
    response = app_table.get_item(Key={"PK": f"USER#{user_id}", "SK": f"TEST#{test_id}"})
    test = response.get("Item")
    if not test:
        return None
    
    correct_answers = {"q1": "A", "q2": "B"}  # Example grading logic
    score = sum(1 for q, a in user_answers.items() if correct_answers.get(q) == a)

    app_table.update_item(
        Key={"PK": f"USER#{user_id}", "SK": f"TEST#{test_id}"},
        UpdateExpression="SET answers = :a, score = :s",
        ExpressionAttributeValues={":a": user_answers, ":s": score},
    )
    return score

def get_user_tests(user_id):
    response = app_table.query(
        KeyConditionExpression='PK = :pk AND begins_with(SK, :sk)',
        ExpressionAttributeValues={":pk": f"USER#{user_id}", ":sk": "TEST#"}
    )
    return response.get("Items", [])
