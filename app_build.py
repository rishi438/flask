from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from app.models import db
from celery import Celery

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:8000"}})

    celery = Celery(
        'app',  # Set to the name of your Flask application package
        broker='pyamqp://guest:guest@localhost:5672//',
        include=['app.tasks']  # Correct path to the tasks module
    )
    celery.conf.update(app.config)
    # Configure Flask app and extensions
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///sites.db'
    
    # Configure Flask-Mail
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'zoomzombie438@gmail.com'
    app.config['MAIL_PASSWORD'] = 'wtvb vtam lkpp ijbu'
    app.config['MAIL_DEFAULT_SENDER'] = 'zoomzombie438@gmail.com'

    db.init_app(app)
    mail = Mail(app)

    with app.app_context():
        db.create_all()

    return app, mail, celery
