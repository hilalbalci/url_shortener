import logging

from flask import Flask

from controller.account import account_blueprint
from controller.url import url_blueprint
from db import db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shortener.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.register_blueprint(account_blueprint)
app.register_blueprint(url_blueprint)
logging.basicConfig(level=logging.DEBUG)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
