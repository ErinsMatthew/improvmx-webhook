import sqlite3
import click

from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    current_app.logger.debug("Running schema.sql...")

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


def insert_email(values):
    db = get_db()

    db.execute(
        "INSERT INTO email ( message_id, message_ts, to_email_text, from_name_text, from_email_text, subject_text ) VALUES ( ?, ?, ?, ?, ?, ? );",
        (
            values["message_id"],
            values["message_ts"],
            values["to_email_text"],
            values["from_name_text"],
            values["from_email_text"],
            values["subject_text"],
        ),
    )

    db.commit()


@click.command("init-db")
def init_db_command():
    init_db()

    click.echo("Initialized.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
