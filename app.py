import sqlite3
import os
from pathlib import Path

from dataclasses import dataclass

from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "app.db"

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "development-only-secret-key")


@dataclass
class Student:
    name: str
    email: str
    age: int
    gender: str
    course: str
    password: str


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
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                course TEXT NOT NULL,
                password TEXT NOT NULL
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
    name = form.get("full_name", "").strip()
    email = form.get("email", "").strip().lower()
    age_value = form.get("age", "").strip()
    gender = form.get("gender", "").strip()
    course = form.get("course", "").strip()
    password = form.get("password", "")

    if not all((name, email, age_value, gender, course, password)):
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

    student = Student(name, email, age, gender, course, password)

    try:
        with sqlite3.connect(DATABASE_PATH) as connection:
            connection.execute(
                """
                INSERT INTO students (name, email, age, gender, course, password)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    student.name,
                    student.email,
                    student.age,
                    student.gender,
                    student.course,
                    generate_password_hash(student.password),
                ),
            )
            connection.commit()
    except sqlite3.IntegrityError:
        return render_template(
            "index.html",
            message="That email address is already registered.",
            message_type="error",
        ), 409
    except sqlite3.Error:
        return render_template(
            "index.html",
            message="Registration could not be saved. Please try again.",
            message_type="error",
        ), 500

    return redirect(url_for("success", name=student.name))


@app.get("/success")
def success():
    name = request.args.get("name", "").strip()
    if not name:
        return redirect(url_for("home"))
    return render_template("success.html", name=name)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", message=None)

    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    if not email or not password:
        return render_template(
            "login.html",
            message="Email and password are required.",
        ), 400

    try:
        with sqlite3.connect(DATABASE_PATH) as connection:
            connection.row_factory = sqlite3.Row
            student = connection.execute(
                "SELECT id, name, email, age, gender, course, password "
                "FROM students WHERE email = ?",
                (email,),
            ).fetchone()
    except sqlite3.Error:
        return render_template(
            "login.html",
            message="Login is temporarily unavailable. Please try again.",
        ), 500

    if student is None or not check_password_hash(student["password"], password):
        return render_template(
            "login.html",
            message="Incorrect email or password.",
        ), 401

    session.clear()
    session["student_id"] = student["id"]
    return redirect(url_for("profile"))


@app.get("/profile")
def profile():
    student_id = session.get("student_id")
    if student_id is None:
        return redirect(url_for("login"))

    try:
        with sqlite3.connect(DATABASE_PATH) as connection:
            connection.row_factory = sqlite3.Row
            student = connection.execute(
                "SELECT name, email, age, gender, course "
                "FROM students WHERE id = ?",
                (student_id,),
            ).fetchone()
    except sqlite3.Error:
        return render_template(
            "login.html",
            message="Profile is temporarily unavailable. Please try again.",
        ), 500

    if student is None:
        session.clear()
        return redirect(url_for("login"))

    return render_template("profile.html", student=student)


@app.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.post("/update-course")
def update_course():
    student_id = session.get("student_id")
    course = request.form.get("course", "").strip()
    allowed_courses = {
        "Python",
        "Web Development",
        "Data Science",
        "Cloud Computing",
    }

    if student_id is None:
        return jsonify({"success": False, "message": "Please log in again."}), 401
    if course not in allowed_courses:
        return jsonify({"success": False, "message": "Please select a valid course."}), 400

    try:
        with sqlite3.connect(DATABASE_PATH) as connection:
            cursor = connection.execute(
                "UPDATE students SET course = ? WHERE id = ?",
                (course, student_id),
            )
            connection.commit()
    except sqlite3.Error:
        return jsonify(
            {"success": False, "message": "Course could not be updated."}
        ), 500

    if cursor.rowcount != 1:
        session.clear()
        return jsonify({"success": False, "message": "Student account not found."}), 404

    return jsonify({"success": True, "course": course})


init_database()


if __name__ == "__main__":
    app.run(debug=True)
