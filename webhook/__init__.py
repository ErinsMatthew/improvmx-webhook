import os
import json

from flask import Flask, request
from . import auth, db
from webhook.email import Email


def load_config(app):
    app.config.from_mapping(
        SECRET_KEY="<secret key goes here>",
        AUTO_CREATE_TABLE=False,
        HAS_PROXY=False,
        DATABASE=os.path.join(app.instance_path, "improvmx-webhook-data.sqlite"),
    )

    app.config.from_file("config.json", load=json.load, silent=True)

    app.config["DATABASE"] = os.path.join(
        app.instance_path, app.config["DATABASE_FILENAME"]
    )


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    load_config(app)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    if app.config["HAS_PROXY"]:
        # see <https://flask.palletsprojects.com/en/3.0.x/deploying/proxy_fix/>
        
        from werkzeug.middleware.proxy_fix import ProxyFix

        app.wsgi_app = ProxyFix(
            app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
        )

    @app.before_request
    def authenticate():
        if not auth.is_allowed(request):
            return "Forbidden", 403

    @app.post("/")
    def process():
        email = Email(request)

        if email.is_valid():
            email.process()

            return "", 204
        else:
            return "Invalid", 400

    db.init_app(app)

    return app
