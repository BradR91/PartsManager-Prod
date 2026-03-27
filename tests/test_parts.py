from models import Part

def login(client, username, password, role_id):
    client.post("/register", data={"username": username, "password": password, "role_id": role_id})
    client.post("/login", data={"username": username, "password": password})


def test_create_part_adds_part(client, app):
    login(client, "regularuser", "Password1", 1)
    client.post("/parts/create", data={"part_no": "PN-001", "part_desc": "Test Part"})
    with app.app_context():
        assert Part.query.filter_by(PartNo="PN-001").first() is not None

def test_list_parts_returns_parts(client):
    login(client, "regularuser", "Password1", 1)
    client.post("/parts/create", data={"part_no": "PN-001", "part_desc": "Test Part"})
    response = client.get("/parts/")
    assert b"PN-001" in response.data

def test_update_part_changes_values(client, app):
    login(client, "adminuser", "Password1", 2)
    client.post("/parts/create", data={"part_no": "PN-001", "part_desc": "Original Desc"})
    with app.app_context():
        part = Part.query.filter_by(PartNo="PN-001").first()
        part_id = part.ID
    client.post(f"/parts/update/{part_id}", data={"part_no": "PN-001", "part_desc": "Updated Desc"})
    with app.app_context():
        updated = Part.query.get(part_id)
        assert updated.PartDesc == "Updated Desc"

def test_delete_part_removes_part(client, app):
    login(client, "adminuser", "Password1", 2)
    client.post("/parts/create", data={"part_no": "PN-001", "part_desc": "To Be Deleted"})
    with app.app_context():
        part = Part.query.filter_by(PartNo="PN-001").first()
        part_id = part.ID
    client.post(f"/parts/delete/{part_id}")
    with app.app_context():
        assert Part.query.get(part_id) is None
