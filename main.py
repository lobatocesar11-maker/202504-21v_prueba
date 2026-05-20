from flask import Flask, jsonify

from database.db import close_db, init_db
from routes.students import students_bp


def create_app():
    app = Flask(__name__)
    init_db()
    app.register_blueprint(students_bp)
    app.teardown_appcontext(close_db)

    @app.get("/")
    def home():
        return jsonify(
            {
                "message": "API de estudiantes",
                "endpoints": [
                    "GET /students",
                    "POST /students",
                    "GET /students/<id>",
                    "PUT /students/<id>",
                    "PATCH /students/<id>",
                    "DELETE /students/<id>",
                    "POST /students/bulk",
                    "GET /students/average",
                    "GET /students/table",
                ],
            }
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
