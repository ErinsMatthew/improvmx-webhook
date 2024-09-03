from flask import current_app
from webhook.db import insert_email


class Email:
    def __init__(self, request):
        self.valid = False

        self.request = request
        
        self.values = {
            "message_id": request.json["message-id"],
            "message_ts": request.json["timestamp"],
            "to_email_text": request.json["headers"]["Delivered-To"],
            "from_name_text": request.json["from"]["name"],
            "from_email_text": request.json["from"]["email"],
            "subject_text": request.json["subject"],
        }

    def is_valid(self):
        self.valid = self.request.is_json

        return self.valid

    def process(self):
        current_app.logger.debug(
            "Processing email message (%s).",
            self.values,
        )

        insert_email(self.values)

        return ""
