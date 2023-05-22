from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
import os

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
login_manager = LoginManager()
csrf = CSRFProtect()

db_info = {'host': 'dpg-ch7adag2qv26p1btlsig-a.oregon-postgres.render.com',
           'database': 'render_6bjb',
           'psw': 'jGuMtISwrcjpyNbCwFS5F2h2i3zsJJpr',
           'user': 'khvol',
           'port': '5432'}


def create_app(static_url_path="", static_folder="static"):
    app = Flask(__name__)
    csrf.init_app(app)
    login_manager.init_app(app)
    app.config['DEBUG'] = True 
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    #os.path.join(basedir, 'stocks.db')
    # postgres://khvol:gqPQc1ZZOzDZCVuygWpWT3Rj1GOhRUUS@dpg-chltrkvdvk4sq15e8is0-a.oregon-postgres.render.com/stock_viewer
    app.config['SECRET_KEY']='123456'
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    
    from app.stocks import bp as stocks_bp
    app.register_blueprint(stocks_bp, url_prefix="/viewer")

    from app.authentication import auth
    app.register_blueprint(auth, url_prefix="/auth")

    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models import User 
    return User.query.get(int(user_id))

from app import models 