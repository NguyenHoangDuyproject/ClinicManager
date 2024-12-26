from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from urllib.parse import quote
import cloudinary

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'zaq12wsxcde34rfvbgt56yhnmju78ik,.lo90p;/'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/phongkham?charset=utf8mb4'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    cloudinary.config(
        cloud_name='dcvdmnrvo',
        api_key='483432986537474',
        api_secret='QuLYz0193idvCinKaxTNbh1u4io'
    )

    from app.routes import main
    app.register_blueprint(main)
    # register modules
    from . import dao
    from app.modules.admin import init_admin
    from app.modules.nurse import init_nurse
    init_admin(app)
    init_nurse(app)
    return app
