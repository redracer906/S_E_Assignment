from flask import Flask, jsonify, request
import sqlite3
from pathlib import Path

app = Flask(__name__)
DB_PATH = Path(__file__).with_name("students.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        """)


@app.get("/students")
def get_students():
    with get_connection() as conn:
        rows = conn.execute("SELECT id, name, department, email FROM students ORDER BY id").fetchall()
    return jsonify([dict(row) for row in rows])


@app.get("/students/<int:student_id>")
def get_student(student_id):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, name, department, email FROM students WHERE id = ?", (student_id,)
        ).fetchone()
    if row is None:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(dict(row))


def validate_student_payload(data):
    if not isinstance(data, dict):
        return "Request body must be a JSON object"
    for field in ("name", "department", "email"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            return f"'{field}' is required and must be a non-empty string"
    return None


@app.post("/students")
def add_student():
    data = request.get_json(silent=True)
    error = validate_student_payload(data)
    if error:
        return jsonify({"error": error}), 400
    try:
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO students (name, department, email) VALUES (?, ?, ?)",
                (data["name"].strip(), data["department"].strip(), data["email"].strip()),
            )
            student_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        return jsonify({"error": "A student with this email already exists"}), 409
    return jsonify({"message": "Student added", "id": student_id}), 201


@app.put("/students/<int:student_id>")
def update_student(student_id):
    data = request.get_json(silent=True)
    error = validate_student_payload(data)
    if error:
        return jsonify({"error": error}), 400
    try:
        with get_connection() as conn:
            cursor = conn.execute(
                "UPDATE students SET name = ?, department = ?, email = ? WHERE id = ?",
                (data["name"].strip(), data["department"].strip(), data["email"].strip(), student_id),
            )
            if cursor.rowcount == 0:
                return jsonify({"error": "Student not found"}), 404
    except sqlite3.IntegrityError:
        return jsonify({"error": "A student with this email already exists"}), 409
    return jsonify({"message": "Student updated"})


@app.delete("/students/<int:student_id>")
def delete_student(student_id):
    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
        if cursor.rowcount == 0:
            return jsonify({"error": "Student not found"}), 404
    return jsonify({"message": "Student deleted"})


if __name__ == "__main__":
    initialize_database()
    app.run(host="127.0.0.1", port=5001, debug=False)
