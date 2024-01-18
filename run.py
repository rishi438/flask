from flask import make_response, render_template

from app_build import create_app
from api.route_handler import api_routes
from app.tasks import init_celery

app, mail, celery = create_app()
celery_scheduler = init_celery(app, celery)

with app.app_context():
    app.register_blueprint(api_routes, url_prefix="/api")


def page_not_found(ex):
    return make_response(render_template("error.html"), 404)


app.register_error_handler(404, page_not_found)


@app.route("/test")
def home():
    data = {
        "name": "UP and Running."
    }
    return make_response(render_template("index.html", **data), 200)


if __name__ == "__main__":
    app.debug = True
    app.run()
