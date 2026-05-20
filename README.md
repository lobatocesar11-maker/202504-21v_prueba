# API REST de estudiantes

Proyecto en Python con Flask y SQLite para gestionar estudiantes mediante endpoints REST.

## Requisitos

- Python 3.10 o superior
- pip

## Instalacion

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

## Ejecucion

```bash
python main.py
```

La API se ejecuta por defecto en:

```text
http://127.0.0.1:5000
```

## Endpoints

| Metodo | Ruta | Descripcion |
| --- | --- | --- |
| POST | `/students` | Crear un estudiante |
| GET | `/students` | Obtener todos los estudiantes |
| GET | `/students/<id>` | Obtener un estudiante por ID |
| PUT | `/students/<id>` | Actualizar un estudiante completo |
| PATCH | `/students/<id>` | Actualizar datos parciales |
| DELETE | `/students/<id>` | Eliminar un estudiante |
| POST | `/students/bulk` | Crear varios estudiantes |
| GET | `/students/average` | Obtener promedio de notas |
| GET | `/students/table` | Renderizar tabla HTML parcial |

## Ejemplo para crear un estudiante

```bash
curl -X POST http://127.0.0.1:5000/students \
  -H "Content-Type: application/json" \
  -d '{"dni":"12345678","name":"Juan Perez","age":20,"grade":15.5,"is_approved":true}'
```

## Ejemplo para creacion masiva

```bash
curl -X POST http://127.0.0.1:5000/students/bulk \
  -H "Content-Type: application/json" \
  -d '[
    {"dni":"11111111","name":"Ana Torres","age":19,"grade":18,"is_approved":true},
    {"dni":"22222222","name":"Luis Ramos","age":21,"grade":12.5,"is_approved":false}
  ]'
```
