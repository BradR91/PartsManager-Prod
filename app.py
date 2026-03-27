from flask import Flask
import models
from models import db, Role
from repositories import RoleRepository, UserRepository, PartRepository, PrefixRepository
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

        if not UserRepository.get_by_username('regular'):
            UserRepository.create('regular', 'password', 1)

        if not UserRepository.get_by_username('admin'):
            UserRepository.create('admin', 'password1', 2)

        if not PartRepository.get_by_part_no('SABBTTC5359'):
            part1 = PartRepository.create('SABBTTC5359', 'Super Hub 3')
            PrefixRepository.create(part1.ID, '3172J7650')

        if not PartRepository.get_by_part_no('SABTTC5364'):
            part2 = PartRepository.create('SABTTC5364', 'Hub 3')
            PrefixRepository.create(part2.ID, '3772469890')
            PrefixRepository.create(part2.ID, '3727447888')

        if not PartRepository.get_by_part_no('TTDLINK2780'):
            part3 = PartRepository.create('TTDLINK2780', 'Hub 1')
            PrefixRepository.create(part3.ID, '2848B3421')
            PrefixRepository.create(part3.ID, '2849C7550')

        if not PartRepository.get_by_part_no('SABBTTB5359'):
            part4 = PartRepository.create('SABBTTB5359', 'Business Super Hub 3')
            PrefixRepository.create(part4.ID, '3172J7650')

        if not PartRepository.get_by_part_no('SABTTB5364'):
            part5 = PartRepository.create('SABTTB5364', 'Business Hub 3')
            PrefixRepository.create(part5.ID, '3772469890')
            PrefixRepository.create(part5.ID, '3727447888')

        if not PartRepository.get_by_part_no('TTBDLINK2780'):
            part6 = PartRepository.create('TTBDLINK2780', 'Business Hub 1')
            PrefixRepository.create(part6.ID, '3551E8892')
        
        if not PartRepository.get_by_part_no('TTHUAWEI522'):
            part7 = PartRepository.create('TTHUAWEI522', 'Legacy Hub 1')
            PrefixRepository.create(part7.ID, '1923F5667')
        
        if not PartRepository.get_by_part_no('TTBHUAWEI532'):
            part8 = PartRepository.create('TTBHUAWEI532', 'Legacy Business Hub 1')
            PrefixRepository.create(part8.ID, '2034G7779')
            PrefixRepository.create(part8.ID, '2035H8881')
        
        if not PartRepository.get_by_part_no('TTDLINK1780'):
            part9 = PartRepository.create('TTDLINK1780', 'Legacy Hub 1')
            PrefixRepository.create(part9.ID, '1721K2334')

        if not PartRepository.get_by_part_no('TTEERO6'):
            part10 = PartRepository.create('TTEERO6', 'Mesh Hub 1')
            PrefixRepository.create(part10.ID, '4562L5556')

        db.session.commit()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
