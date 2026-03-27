from models import Part, PartPrefix

def login(client, username, password, role_id):
    client.post("/register", data={"username": username, "password": password, "role_id": role_id})
    client.post("/login", data={"username": username, "password": password})


def test_create_prefix_adds_prefix(client, app):
    login(client, "regularuser", "Password1", 1)
    client.post("/parts/create", data={"part_no": "PN-001", "part_desc": "Test Part"})
    with app.app_context():
        part = Part.query.filter_by(PartNo="PN-001").first()
        part_id = part.ID
    client.post("/prefixes/create", data={"part_id": part_id, "prefix": "ABC"})
    with app.app_context():
        assert PartPrefix.query.filter_by(PartID=part_id, Prefix="ABC").first() is not None


def test_delete_prefix_removes_prefix(client, app):
    login(client, "adminuser", "Password1", 2)
    client.post("/parts/create", data={"part_no": "PN-001", "part_desc": "Test Part"})
    with app.app_context():
        part = Part.query.filter_by(PartNo="PN-001").first()
        part_id = part.ID
    client.post("/prefixes/create", data={"part_id": part_id, "prefix": "ABC"})
    with app.app_context():
        prefix = PartPrefix.query.filter_by(PartID=part_id, Prefix="ABC").first()
        prefix_id = prefix.ID
    client.post(f"/prefixes/delete/{prefix_id}")
    with app.app_context():
        assert PartPrefix.query.get(prefix_id) is None
