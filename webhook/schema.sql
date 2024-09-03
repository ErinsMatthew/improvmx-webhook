DROP TABLE IF EXISTS email;

CREATE TABLE email (
    email_id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_id TEXT NOT NULL,
    message_ts TIMESTAMP NOT NULL,
    to_email_text TEXT NOT NULL,
    from_name_text TEXT NOT NULL,
    from_email_text TEXT NOT NULL,
    subject_text TEXT NOT NULL,
    call_ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);