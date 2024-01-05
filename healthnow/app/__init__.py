from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "ygpU9Um57GvBNqKPZXIZdMHxWBsdJ1kl8A"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///healthnow.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
