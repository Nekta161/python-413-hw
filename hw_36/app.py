"""
REST API для барбершопа на Flask и PeeWee ORM
Реализует CRUD для мастеров и записей
"""

from datetime import datetime
from flask import Flask, request, jsonify
from peewee import (
    Model,
    SqliteDatabase,
    CharField,
    TextField,
    DecimalField,
    DateTimeField,
    ForeignKeyField,
    IntegerField,
    DoesNotExist,
)

# === Инициализация базы данных и Flask ===
DB = SqliteDatabase("barbershop.db")
app = Flask(__name__)

# Убедимся, что JSON корректно отображает кириллицу
app.config["JSON_AS_ASCII"] = False


# === ORM-модели ===
class Master(Model):
    first_name = CharField(max_length=50, null=False)
    last_name = CharField(max_length=50, null=False)
    middle_name = CharField(max_length=50, null=True)
    phone = CharField(max_length=20, unique=True)

    class Meta:
        database = DB


class Appointment(Model):
    client_name = CharField(max_length=100, null=False)
    client_phone = CharField(max_length=20, null=False)
    date = DateTimeField(default=datetime.now)
    master = ForeignKeyField(Master, backref="appointments")
    status = CharField(max_length=20, default="pending")

    class Meta:
        database = DB


# === Функции конвертации в словари ===
def master_to_dict(master: Master) -> dict:
    """Преобразует объект Master в словарь."""
    return {
        "id": master.id,
        "first_name": master.first_name,
        "last_name": master.last_name,
        "middle_name": master.middle_name,
        "phone": master.phone,
    }


def appointment_to_dict(appointment: Appointment) -> dict:
    """Преобразует объект Appointment в словарь с информацией о мастере."""
    return {
        "id": appointment.id,
        "client_name": appointment.client_name,
        "client_phone": appointment.client_phone,
        "date": appointment.date.strftime("%Y-%m-%d %H:%M:%S"),
        "master": {
            "id": appointment.master.id,
            "first_name": appointment.master.first_name,
            "last_name": appointment.master.last_name,
        },
        "status": appointment.status,
    }


# === Функции валидации ===
def validate_master_data(dict) -> tuple[bool, str]:
    """Проверяет корректность данных для мастера."""
    if not isinstance(data, dict):
        return False, "Данные должны быть JSON-объектом"

    required = ["first_name", "last_name", "phone"]
    for field in required:
        if field not in data or not data[field] or not data[field].strip():
            return False, f"Поле '{field}' обязательно и не может быть пустым"
    phone = data["phone"].strip()
    if not isinstance(phone, str) or len(phone) > 20:
        return False, "Поле 'phone' должно быть строкой длиной до 20 символов"
    return True, ""


def validate_appointment_data(dict) -> tuple[bool, str]:
    """Проверяет корректность данных для записи."""
    if not isinstance(data, dict):
        return False, "Данные должны быть JSON-объектом"

    required = ["client_name", "client_phone", "master_id"]
    for field in required:
        if field not in data:
            return False, f"Поле '{field}' обязательно"
        value = data[field]
        if not value or not str(value).strip():
            return False, f"Поле '{field}' не может быть пустым"

    try:
        master_id = int(data["master_id"])
        if master_id <= 0:
            return False, "master_id должен быть положительным числом"
        if not Master.select().where(Master.id == master_id).exists():
            return False, "Мастер с таким ID не найден"
    except (ValueError, TypeError):
        return False, "master_id должен быть числом"

    status = data.get("status", "pending")
    allowed_statuses = ["pending", "confirmed", "completed", "cancelled"]
    if status and status not in allowed_statuses:
        return False, f"status может быть одним из: {', '.join(allowed_statuses)}"
    return True, ""


# === Маршруты: Master ===
@app.route("/masters", methods=["GET"])
def get_masters():
    """Получить список всех мастеров."""
    try:
        masters = Master.select()
        result = [master_to_dict(m) for m in masters]
        return jsonify({"masters": result}), 200
    except Exception as e:
        return (
            jsonify({"error": "Ошибка при получении мастеров", "details": str(e)}),
            500,
        )


@app.route("/masters/<int:master_id>", methods=["GET"])
def get_master(master_id: int):
    """Получить мастера по ID."""
    try:
        master = Master.get(Master.id == master_id)
        return jsonify({"master": master_to_dict(master)}), 200
    except DoesNotExist:
        return jsonify({"error": "Мастер не найден"}), 404
    except Exception as e:
        return jsonify({"error": "Внутренняя ошибка", "details": str(e)}), 500


@app.route("/masters", methods=["POST"])
def create_master():
    """Создать нового мастера."""
    try:
        data = request.json  # ← Сначала получаем data
        if not data or not isinstance(data, dict):
            return jsonify({"error": "Ожидается JSON"}), 400

        is_valid, msg = validate_master_data(data)  # ← Только теперь используем
        if not is_valid:
            return jsonify({"error": msg}), 400

        phone = data["phone"].strip()
        if Master.select().where(Master.phone == phone).exists():
            return jsonify({"error": "Телефон уже используется другим мастером"}), 400

        master = Master.create(
            first_name=data["first_name"].strip(),
            last_name=data["last_name"].strip(),
            middle_name=data.get("middle_name", None),
            phone=phone,
        )
        return jsonify({"master": master_to_dict(master)}), 201
    except Exception as e:
        print(f"Ошибка при создании мастера: {e}")
        return jsonify({"error": "Не удалось создать мастера", "details": str(e)}), 500


@app.route("/masters/<int:master_id>", methods=["PUT"])
def update_master(master_id: int):
    """Обновить информацию о мастере."""
    try:
        master = Master.get(Master.id == master_id)
        data = request.json
        if not data or not isinstance(data, dict):
            return jsonify({"error": "Ожидается JSON"}), 400

        is_valid, msg = validate_master_data(data)
        if not is_valid:
            return jsonify({"error": msg}), 400

        phone = data["phone"].strip()
        # Проверка уникальности телефона (кроме текущего мастера)
        if (
            Master.select()
            .where(Master.phone == phone, Master.id != master_id)
            .exists()
        ):
            return jsonify({"error": "Телефон уже используется другим мастером"}), 400

        master.first_name = data["first_name"].strip()
        master.last_name = data["last_name"].strip()
        master.middle_name = data.get("middle_name", None)
        master.phone = phone
        master.save()

        return jsonify({"master": master_to_dict(master)}), 200
    except DoesNotExist:
        return jsonify({"error": "Мастер не найден"}), 404
    except Exception as e:
        print(f"Ошибка при обновлении мастера: {e}")
        return jsonify({"error": "Ошибка обновления", "details": str(e)}), 500


@app.route("/masters/<int:master_id>", methods=["DELETE"])
def delete_master(master_id: int):
    """Удалить мастера."""
    try:
        master = Master.get(Master.id == master_id)
        # Удаляем все записи, связанные с мастером
        Appointment.delete().where(Appointment.master == master).execute()
        master.delete_instance()
        return "", 204
    except DoesNotExist:
        return jsonify({"error": "Мастер не найден"}), 404
    except Exception as e:
        print(f"Ошибка при удалении мастера: {e}")
        return jsonify({"error": "Ошибка удаления", "details": str(e)}), 500


# === Маршруты: Appointment ===
@app.route("/appointments", methods=["GET"])
def get_appointments():
    """Получить все записи с опциональной сортировкой."""
    try:
        sort_by = request.args.get("sort_by", "id")
        direction = request.args.get("direction", "asc").lower()

        valid_sort_fields = {
            "id": Appointment.id,
            "date": Appointment.date,
            "client_name": Appointment.client_name,
            "status": Appointment.status,
        }

        query = Appointment.select().join(Master)

        if sort_by in valid_sort_fields:
            field = valid_sort_fields[sort_by]
            if direction == "desc":
                query = query.order_by(field.desc())
            else:
                query = query.order_by(field.asc())
        else:
            query = query.order_by(Appointment.id.asc())

        result = [appointment_to_dict(a) for a in query]
        return jsonify({"appointments": result}), 200
    except Exception as e:
        print(f"Ошибка при получении записей: {e}")
        return (
            jsonify({"error": "Ошибка при получении записей", "details": str(e)}),
            500,
        )


@app.route("/appointments/<int:appointment_id>", methods=["GET"])
def get_appointment(appointment_id: int):
    """Получить запись по ID."""
    try:
        appointment = Appointment.get(Appointment.id == appointment_id)
        return jsonify({"appointment": appointment_to_dict(appointment)}), 200
    except DoesNotExist:
        return jsonify({"error": "Запись не найдена"}), 404
    except Exception as e:
        print(f"Ошибка при получении записи: {e}")
        return jsonify({"error": "Внутренняя ошибка", "details": str(e)}), 500


@app.route("/appointments/master/<int:master_id>", methods=["GET"])
def get_appointments_by_master(master_id: int):
    """Получить все записи для заданного мастера."""
    try:
        if not Master.select().where(Master.id == master_id).exists():
            return jsonify({"error": "Мастер не найден"}), 404

        appointments = Appointment.select().where(Appointment.master == master_id)
        result = [appointment_to_dict(a) for a in appointments]
        return jsonify({"appointments": result}), 200
    except Exception as e:
        print(f"Ошибка при получении записей: {e}")
        return (
            jsonify({"error": "Ошибка при получении записей", "details": str(e)}),
            500,
        )


@app.route("/appointments", methods=["POST"])
def create_appointment():
    """Создать новую запись."""
    try:
        data = request.json
        if not data or not isinstance(data, dict):
            return jsonify({"error": "Ожидается JSON"}), 400

        is_valid, msg = validate_appointment_data(data)
        if not is_valid:
            return jsonify({"error": msg}), 400

        appointment = Appointment.create(
            client_name=data["client_name"].strip(),
            client_phone=data["client_phone"].strip(),
            master=data["master_id"],
            status=data.get("status", "pending").strip(),
        )
        return jsonify({"appointment": appointment_to_dict(appointment)}), 201
    except Exception as e:
        print(f"Ошибка при создании записи: {e}")
        return jsonify({"error": "Не удалось создать запись", "details": str(e)}), 500


@app.route("/appointments/<int:appointment_id>", methods=["PUT"])
def update_appointment(appointment_id: int):
    """Обновить запись."""
    try:
        appointment = Appointment.get(Appointment.id == appointment_id)
        data = request.json
        if not data or not isinstance(data, dict):
            return jsonify({"error": "Ожидается JSON"}), 400

        if "master_id" in data:
            if not Master.select().where(Master.id == data["master_id"]).exists():
                return jsonify({"error": "Мастер с таким ID не найден"}), 400
            appointment.master = data["master_id"]

        if "client_name" in data:
            name = data["client_name"].strip()
            if not name:
                return jsonify({"error": "client_name не может быть пустым"}), 400
            appointment.client_name = name

        if "client_phone" in data:
            phone = data["client_phone"].strip()
            if not phone:
                return jsonify({"error": "client_phone не может быть пустым"}), 400
            appointment.client_phone = phone

        if "status" in data:
            status = data["status"].strip()
            allowed = ["pending", "confirmed", "completed", "cancelled"]
            if status not in allowed:
                return (
                    jsonify({"error": f"status: допустимы {', '.join(allowed)}"}),
                    400,
                )
            appointment.status = status

        appointment.save()
        return jsonify({"appointment": appointment_to_dict(appointment)}), 200
    except DoesNotExist:
        return jsonify({"error": "Запись не найдена"}), 404
    except Exception as e:
        print(f"Ошибка при обновлении записи: {e}")
        return jsonify({"error": "Ошибка обновления", "details": str(e)}), 500


@app.route("/appointments/<int:appointment_id>", methods=["DELETE"])
def delete_appointment(appointment_id: int):
    """Удалить запись."""
    try:
        appointment = Appointment.get(Appointment.id == appointment_id)
        appointment.delete_instance()
        return "", 204
    except DoesNotExist:
        return jsonify({"error": "Запись не найдена"}), 404
    except Exception as e:
        print(f"Ошибка при удалении записи: {e}")
        return jsonify({"error": "Ошибка удаления", "details": str(e)}), 500


# === Запуск приложения ===
if __name__ == "__main__":
    # Создание таблиц при запуске
    DB.connect()
    DB.create_tables([Master, Appointment], safe=True)
    DB.close()

    # Запуск сервера
    app.run(debug=True, host="127.0.0.1", port=5000)
