import uvicorn
from fastapi import FastAPI
from mongoengine import Document, StringField, connect

app = FastAPI()

connect(
    db="test",
    host="mongodb",
    port=27017,
    username="root",
    password="example"
)

class User(Document):
    name = StringField(required=True)
    email = StringField(required=True)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/users")
def get_users():
    return User.objects().to_json()

@app.post("/users")
def create_user(name: str, email: str):
    user = User(name=name, email=email).save()
    return user.to_json()

@app.get("/users/{user_id}")
def get_user(user_id: str):
    return User.objects(id=user_id).to_json()

@app.put("/users/{user_id}")
def update_user(user_id: str, name: str, email: str):
    user = User.objects(id=user_id).first()
    user.update(name=name, email=email)
    return user.to_json()

@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    user = User.objects(id=user_id).first()
    user.delete()
    return user.to_json()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)