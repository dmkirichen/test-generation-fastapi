from fastapi import FastAPI, Depends
from .auth import hash_password, create_access_token
from .crud import create_user, get_user_by_username, save_test, submit_test, get_user_tests
from .dependencies import app_table
from .schemas import UserCreate, TestSubmit
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()

@app.post("/register")
def register(user: UserCreate):
    hashed_password = hash_password(user.password)
    user_id = create_user(user.username, hashed_password, user.email)
    return {"user_id": user_id}

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_username(form_data.username)
    if not user or not hash_password(form_data.password, user["password_hash"]):
        return {"error": "Invalid credentials"}
    token = create_access_token(data={"sub": user['username']})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/tests/")
def create_test(user_id: str, questions: dict):
    test_id = save_test(user_id, questions)
    return {"test_id": test_id}

@app.post("/tests/{test_id}/submit")
def submit(test_id: str, user_id: str, submission: TestSubmit):
    score = submit_test(user_id, test_id, submission.answers)
    return {"score": score}

@app.get("/users/{user_id}/tests")
def get_tests(user_id: str):
    return get_user_tests(user_id)
