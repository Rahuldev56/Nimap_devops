from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from typing import List
import os

app = FastAPI()

# Data file path
DATA_FILE = "data/users.json"

# Ensure data directory exists
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

# User model
class User(BaseModel):
    first_name: str
    last_name: str
    age:int

def load_users() -> List[dict]:
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Return empty list if file doesn't exist
        return []

def save_users(users: List[dict]):
    with open(DATA_FILE, 'w') as f:
        json.dump(users, f, indent=2)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI ;}

@app.get("/users")
def get_users():
    users = load_users()
    return {"users": users}

@app.post("/users")
def create_user(user: User):
    users = load_users()
    
    # Check for duplicate email
    if any(u['email'] == user.email for u in users):
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Add new user
    new_user = user.dict()
    users.append(new_user)
    save_users(users)
    return new_user
