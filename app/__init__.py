from flask import Flask
from .config import SECRET_KEY, db_string, SQLALCHEMY_TRACK_MODIFICATIONS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = db_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'bp.login_get'  # Use the endpoint name of login route
login_manager.init_app(app)

from app.routes.controller import bp
app.register_blueprint(bp)
