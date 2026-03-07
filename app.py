from flask import Flask
import models
from models import db, Role
from repositories import RoleRepository
from controllers.auth_controller import auth_bp
from controllers.parts_controller import parts_bp
from controllers.prefix_controller import prefix_bp
from controllers.users_controller import users_bp


def create_app():
    app = Flask(__name__)
    app = Flask(__name__, static_folder='public')
    app.secret_key = 'your-secret-key-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///partsmanager.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(parts_bp)
    app.register_blueprint(prefix_bp)
    app.register_blueprint(users_bp)

    with app.app_context():
        db.create_all()

        if not RoleRepository.get_by_id(1):
            db.session.add(Role(ID=1, RoleDesc='Regular User'))

        if not RoleRepository.get_by_id(2):
            db.session.add(Role(ID=2, RoleDesc='Admin'))

        db.session.commit()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
