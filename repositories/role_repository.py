from models import db, Role
class RoleRepository:
    @staticmethod
    def get_all():
        return Role.query.all()

    @staticmethod
    def get_by_id(role_id):
        return Role.query.get(role_id)
