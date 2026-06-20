from fastapi import FastAPI
from database import Base, engine, SessionLocal
from services import get_random_users
from crud import create_user
from models import User
from crud import create_user, get_users

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Meetup Backend Running"}

@app.get("/load-users")
def load_users():

    db = SessionLocal()

    users = get_random_users()

    for user in users:

        create_user(
            db,
            user["name"]["first"],
            float(user["location"]["coordinates"]["latitude"]),
            float(user["location"]["coordinates"]["longitude"])
        )

    return {"message": "100 users loaded"}
@app.get("/users")
def users():

    db = SessionLocal()

    return get_users(db)
@app.get("/users")
def users():
    db = SessionLocal()
    users = get_users(db)
    db.close()
    return users