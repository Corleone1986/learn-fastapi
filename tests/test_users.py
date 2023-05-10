from app import schames
from .database import client, session



def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json().get("message") == "Hello word"


def test_create_user(client):
    response = client.post("/users/", json={"email": "test.createuser@gmail.com", "password": "123456"})
    new_user = schames.UserOut(**response.json())
    print(new_user)
    assert new_user.email == "test.createuser@gmail.com"
    assert response.status_code == 201


def test_login_user(client):
    response = client.post("/login", data={"username": "test.createuser@gmail.com", "password": "123456"})
    print(response.json())
    assert response.status_code  == 200