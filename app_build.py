from celery import Celery
from flask_mail import Mail
from flask_cors import CORS
from flask import Flask

from app.models import db
from utils.environment import (
    CELERY_RABBITMQ_BROKER,
    DATABASE_URI,
    FRONTEND_URL,
    MAIL_DEFAULT_SENDER,
    MAIL_PASSWORD,
    MAIL_PORT,
    MAIL_SERVER,
    MAIL_USE_TLS,
    MAIL_USERNAME,
    TEMPLATES_AUTO_RELOAD,
)


def create_app():
    app = Flask(__name__)

    CORS(app, resources={r"/api/*": {"origins": FRONTEND_URL}})

    celery = Celery(
        "app",
        broker=CELERY_RABBITMQ_BROKER,
        include=["app.tasks"]
    )
    celery.conf.update(app.config)

    # Configure Flask app and extensions
    app.config["TEMPLATES_AUTO_RELOAD"] = TEMPLATES_AUTO_RELOAD
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI

    # Configure Flask-Mail
    app.config["MAIL_SERVER"] = MAIL_SERVER
    app.config["MAIL_PORT"] = MAIL_PORT
    app.config["MAIL_USE_TLS"] = MAIL_USE_TLS
    app.config["MAIL_USERNAME"] = MAIL_USERNAME
    app.config["MAIL_PASSWORD"] = MAIL_PASSWORD
    app.config["MAIL_DEFAULT_SENDER"] = MAIL_DEFAULT_SENDER

    db.init_app(app)
    mail = Mail(app)

    with app.app_context():
        db.create_all()

    return app, mail, celery
