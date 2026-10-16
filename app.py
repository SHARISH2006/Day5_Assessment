import sqlite3
from pathlib import Path

from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "app.db"

app = Flask(__name__)


def init_database() -> None:
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS registrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                course TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.commit()


@app.route("/")
def home():
    return render_template("index.html", message=None, message_type=None)


@app.post("/register")
def register():
    form = request.form
    full_name = form.get("full_name", "").strip()
    email = form.get("email", "").strip().lower()
    age_value = form.get("age", "").strip()
    gender = form.get("gender", "").strip()
    course = form.get("course", "").strip()
    password = form.get("password", "")

    if not all((full_name, email, age_value, gender, course, password)):
        return render_template(
            "index.html",
            message="Please complete every required field.",
            message_type="error",
        ), 400

    try:
        age = int(age_value)
    except ValueError:
        return render_template(
            "index.html",
            message="Age must be a whole number.",
            message_type="error",
        ), 400

    if age < 1 or age > 120:
        return render_template(
            "index.html",
            message="Please enter an age between 1 and 120.",
            message_type="error",
        ), 400

    if len(password) < 6:
        return render_template(
            "index.html",
            message="Password must contain at least 6 characters.",
            message_type="error",
        ), 400

    try:
        with sqlite3.connect(DATABASE_PATH) as connection:
            connection.execute(
                """
                INSERT INTO registrations
                    (full_name, email, age, gender, course, password_hash)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    full_name,
                    email,
                    age,
                    gender,
                    course,
                    generate_password_hash(password),
                ),
            )
            connection.commit()
    except sqlite3.IntegrityError:
        return render_template(
            "index.html",
            message="That email address is already registered.",
            message_type="error",
        ), 409

    return render_template(
        "index.html",
        message="Registration submitted successfully!",
        message_type="success",
    )


init_database()


if __name__ == "__main__":
    app.run(debug=True)
