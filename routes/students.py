import sqlite3

from flask import Blueprint, jsonify, render_template, request

from database.db import get_db
from models.student import current_timestamp, student_to_dict, validate_student


students_bp = Blueprint("students", __name__)


def error_response(message, status_code, details=None):
    response = {"error": message}
    if details:
        response["details"] = details
    return jsonify(response), status_code


def find_student(student_id):
    return get_db().execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()


@students_bp.post("/students")
def create_student():
    data = request.get_json(silent=True)
    values, errors = validate_student(data)
    if errors:
        return error_response("Datos invalidos", 400, errors)

    now = current_timestamp()
    db = get_db()

    try:
        cursor = db.execute(
            """
            INSERT INTO students (dni, name, age, grade, is_approved, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                values["dni"],
                values["name"],
                values["age"],
                values["grade"],
                values["is_approved"],
                now,
                now,
            ),
        )
        db.commit()
    except sqlite3.IntegrityError:
        return error_response("El dni ya existe", 400)

    student = find_student(cursor.lastrowid)
    return jsonify(student_to_dict(student)), 201


@students_bp.get("/students")
def list_students():
    rows = get_db().execute("SELECT * FROM students ORDER BY id").fetchall()
    return jsonify([student_to_dict(row) for row in rows])


@students_bp.get("/students/<int:student_id>")
def get_student(student_id):
    student = find_student(student_id)
    if student is None:
        return error_response("Estudiante no encontrado", 404)
    return jsonify(student_to_dict(student))


@students_bp.route("/students/<int:student_id>", methods=["PUT", "PATCH"])
def update_student(student_id):
    student = find_student(student_id)
    if student is None:
        return error_response("Estudiante no encontrado", 404)

    data = request.get_json(silent=True)
    values, errors = validate_student(data, partial=request.method == "PATCH")
    if errors:
        return error_response("Datos invalidos", 400, errors)
    if not values:
        return error_response("No hay datos para actualizar", 400)

    values["updated_at"] = current_timestamp()
    fields = ", ".join(f"{field} = ?" for field in values)
    params = list(values.values()) + [student_id]
    db = get_db()

    try:
        db.execute(f"UPDATE students SET {fields} WHERE id = ?", params)
        db.commit()
    except sqlite3.IntegrityError:
        return error_response("El dni ya existe", 400)

    updated_student = find_student(student_id)
    return jsonify(student_to_dict(updated_student))


@students_bp.delete("/students/<int:student_id>")
def delete_student(student_id):
    student = find_student(student_id)
    if student is None:
        return error_response("Estudiante no encontrado", 404)

    db = get_db()
    db.execute("DELETE FROM students WHERE id = ?", (student_id,))
    db.commit()
    return jsonify({"message": "Estudiante eliminado"})


@students_bp.post("/students/bulk")
def bulk_create_students():
    payload = request.get_json(silent=True)
    items = payload.get("students") if isinstance(payload, dict) else payload

    if not isinstance(items, list) or not items:
        return error_response("Debe enviar una lista de estudiantes", 400)

    validated_students = []
    validation_errors = {}

    for index, item in enumerate(items):
        values, errors = validate_student(item)
        if errors:
            validation_errors[index] = errors
        else:
            validated_students.append(values)

    if validation_errors:
        return error_response("Datos invalidos", 400, validation_errors)

    now = current_timestamp()
    db = get_db()
    created_ids = []

    try:
        for values in validated_students:
            cursor = db.execute(
                """
                INSERT INTO students (dni, name, age, grade, is_approved, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    values["dni"],
                    values["name"],
                    values["age"],
                    values["grade"],
                    values["is_approved"],
                    now,
                    now,
                ),
            )
            created_ids.append(cursor.lastrowid)
        db.commit()
    except sqlite3.IntegrityError:
        db.rollback()
        return error_response("Uno o mas dni ya existen", 400)

    placeholders = ", ".join("?" for _ in created_ids)
    rows = db.execute(
        f"SELECT * FROM students WHERE id IN ({placeholders}) ORDER BY id", created_ids
    ).fetchall()
    return jsonify([student_to_dict(row) for row in rows]), 201


@students_bp.get("/students/average")
def average_grade():
    row = get_db().execute("SELECT AVG(grade) AS average, COUNT(*) AS total FROM students").fetchone()
    average = row["average"] if row["average"] is not None else 0
    return jsonify({"average": round(average, 2), "total": row["total"]})


@students_bp.get("/students/table")
def students_table():
    rows = get_db().execute("SELECT * FROM students ORDER BY id").fetchall()
    students = [student_to_dict(row) for row in rows]
    return render_template("partials/students_table.html", students=students)
