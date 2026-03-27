from models import User

def test_register_creates_user(client, app):
    client.post("/register", data={"username": "regularuser", "password": "Password1", "role_id": 1})
    with app.app_context():
        assert User.query.filter_by(Username="regularuser").first() is not None

def test_register_invalid_password_rejected(client):
    response = client.post("/register", data={"username": "regularuser", "password": "abc", "role_id": 1}, follow_redirects=True)
    assert User.query.filter_by(Username="regularuser").first() is None

def test_login_invalid_credentials_rejected(client):
    response = client.post("/login", data={"username": "nobody", "password": "WrongPass1"}, follow_redirects=True)
    assert b"wrong" in response.data.lower()
