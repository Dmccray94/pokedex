from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


login= LoginManager()

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    
    app.config.from_object(config_class)
    

    login.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    
    login.login_view='auth.login'
    login.login_message = "Please Login to access this page."
    login.login_message_category='warning'

login= LoginManager()

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    
    app.config.from_object(config_class)
    

    login.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    
    login.login_view='auth.login'
    login.login_message = "Please Login to access this page."
    login.login_message_category='warning'
    
    return app
