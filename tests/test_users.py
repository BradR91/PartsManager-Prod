from models import User

def login(client, username, password, role_id):
    client.post("/register", data={"username": username, "password": password, "role_id": role_id})
    client.post("/login", data={"username": username, "password": password})

def test_list_users_returns_users(client):
    login(client, "adminuser", "Password1", 2)
    client.post("/register", data={"username": "targetuser", "password": "Password1", "role_id": 1})
    response = client.get("/users/")
    assert b"targetuser" in response.data

def test_update_password_changes_password(client, app):
    login(client, "adminuser", "Password1", 2)
    client.post("/register", data={"username": "targetuser", "password": "Password1", "role_id": 1})
    client.post("/users/update_password/targetuser", data={"new_password": "NewPass9"})
    with app.app_context():
        user = User.query.filter_by(Username="targetuser").first()
        assert user.Password == "NewPass9"

def test_delete_user_removes_user(client, app):
    login(client, "adminuser", "Password1", 2)
    client.post("/register", data={"username": "targetuser", "password": "Password1", "role_id": 1})
    client.post("/users/delete/targetuser")
    with app.app_context():
        assert User.query.filter_by(Username="targetuser").first() is None