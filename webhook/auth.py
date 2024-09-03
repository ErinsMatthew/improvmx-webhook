from flask import current_app


def is_allowed(request):
    return request.remote_addr in current_app.config["CLIENTS"]
