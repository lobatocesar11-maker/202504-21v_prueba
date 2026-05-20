from datetime import datetime, timezone


REQUIRED_FIELDS = ("dni", "name", "age", "grade", "is_approved")
ALLOWED_FIELDS = set(REQUIRED_FIELDS)


def current_timestamp():
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


def student_to_dict(row):
    return {
        "id": row["id"],
        "dni": row["dni"],
        "name": row["name"],
        "age": row["age"],
        "grade": row["grade"],
        "is_approved": bool(row["is_approved"]),
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


def validate_student(data, partial=False):
    errors = {}
    values = {}

    if not isinstance(data, dict):
        return {}, {"body": "El cuerpo debe ser un objeto JSON"}

    if not partial:
        for field in REQUIRED_FIELDS:
            if field not in data:
                errors[field] = "Este campo es obligatorio"

    for field in data:
        if field not in ALLOWED_FIELDS:
            errors[field] = "Campo no permitido"

    if "dni" in data:
        dni = str(data["dni"]).strip()
        if not dni:
            errors["dni"] = "El dni no puede estar vacio"
        else:
            values["dni"] = dni

    if "name" in data:
        name = str(data["name"]).strip()
        if not name:
            errors["name"] = "El nombre no puede estar vacio"
        else:
            values["name"] = name

    if "age" in data:
        age = data["age"]
        if isinstance(age, bool) or not isinstance(age, int):
            errors["age"] = "La edad debe ser un numero entero"
        elif age <= 0:
            errors["age"] = "La edad debe ser mayor que cero"
        else:
            values["age"] = age

    if "grade" in data:
        grade = data["grade"]
        if isinstance(grade, bool) or not isinstance(grade, (int, float)):
            errors["grade"] = "La nota debe ser numerica"
        elif grade < 0 or grade > 20:
            errors["grade"] = "La nota debe estar entre 0 y 20"
        else:
            values["grade"] = float(grade)

    if "is_approved" in data:
        is_approved = data["is_approved"]
        if not isinstance(is_approved, bool):
            errors["is_approved"] = "El valor debe ser booleano"
        else:
            values["is_approved"] = 1 if is_approved else 0

    return values, errors
