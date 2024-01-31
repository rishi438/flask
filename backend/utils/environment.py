import os

DATABASE_URI = os.environ.get("DATABASE_URI", "sqlite:///sites.db")
TEMPLATES_AUTO_RELOAD = os.environ.get("TEMPLATES_AUTO_RELOAD", True)

current_directory = os.getcwd()
CELERY_CACHE_DIRECTORY = "celery_cache"
SCHEDULE_FILENAME = "celerybeat-schedule"
absolute_celery_cache_directory = os.path.join(
    current_directory, CELERY_CACHE_DIRECTORY
)
absolute_schedule_filename = os.path.join(
    absolute_celery_cache_directory, SCHEDULE_FILENAME
)
CELERYBEAT_SCHEDULE_FILENAME = os.environ.get(
    "CELERYBEAT_SCHEDULE_FILENAME", absolute_schedule_filename
)

# Mail Configuration
MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
MAIL_PORT = os.environ.get("MAIL_PORT", 587)
MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", True)
MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "********************")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "************************")
MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "****************")

# Celery
CELERY_RABBITMQ_BROKER = os.environ.get(
    "CELERY_RABBITMQ_BROKER", "pyamqp://guest:guest@localhost:5672//"
)
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:4173")
