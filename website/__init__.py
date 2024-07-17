import this

from flask import Flask, session
from os import path
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_login import UserMixin


db = SQLAlchemy()
DB_NAME = "university.db"
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'aalskdffpwenvcpweif'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .adminAuth import adminAuth
    from .userAuth import userAuth
    from .views import views
    app.register_blueprint(adminAuth,url_prefix='/')
    app.register_blueprint(userAuth, url_prefix='/')
    app.register_blueprint(views,url_prefix='/')

    from .models import Student, Faculty

    with app.app_context():
        create_database()
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'userAuth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):

        stype = session.get('type')
        if stype == 'student':
            user = Student.query.filter_by(id=id).first()
        elif stype == 'faculty':
            user = Faculty.query.filter_by(id=id).first()
        else:
            user = None
        return user

    return app

def create_database():
    if not path.exists('instance/' + DB_NAME):
        db.create_all()
        print('Created Database!')