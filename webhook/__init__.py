import os
import json

from flask import Flask, request
from . import auth, db, email


def load_config(app):
    # default config?

    app.config.from_file("config.json", load=json.load, silent=True)

    app.config["DATABASE"] = os.path.join(
        app.instance_path, app.config["DATABASE_FILENAME"]
    )


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    load_config(app)

    @app.before_request
    def authenticate():
        if not auth.is_allowed(request):
            return "Forbidden", 403

    @app.post("/")
    def process():
        if email.is_valid(request):
            email.process(request)

            return "", 204
        else:
            return "Invalid", 400

    db.init_app(app)

    return app
