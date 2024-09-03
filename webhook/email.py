from flask import current_app
from webhook.db import insert_email


def is_valid(request):
    return request.is_json


def process(request):
    values = {
        "message_id": request.json["message-id"],
        "message_ts": request.json["timestamp"],
        "to_email_text": request.json["headers"]["Delivered-To"],
        "from_name_text": request.json["from"]["name"],
        "from_email_text": request.json["from"]["email"],
        "subject_text": request.json["subject"],
    }

    current_app.logger.debug(
        "Processing email message (%s).",
        values,
    )

    insert_email(values)

    return ""
