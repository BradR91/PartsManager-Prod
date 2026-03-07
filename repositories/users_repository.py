from models import db, User
class UserRepository:
    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(Username=username).first()

    @staticmethod
    def create(username, password, role_id):
        user = User(Username=username, Password=password, RoleID=role_id)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update_password(username, new_password):
        user = User.query.filter_by(Username=username).first()
        if user:
            user.Password = new_password
            db.session.commit()
        return user

    @staticmethod
    def delete(username):
        user = User.query.filter_by(Username=username).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False

    @staticmethod
    def authenticate(username, password):
        user = User.query.filter_by(Username=username).first()
        if user and user.Password == password:
            return user
        return None
