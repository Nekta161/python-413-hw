from datetime import datetime
from flask import Blueprint, request, jsonify
from auth import (
    is_valid_api_key,
    is_admin,
    unauthorized_response,
    require_api_key,
    require_admin,
)
from models import Appointment, Master


# Создание блюпринта с префиксом /appointments
appointments_bp = Blueprint("appointments", __name__, url_prefix="/appointments")


def appointment_to_dict(appointment):
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


def validate_appointment_data(data):
    """
    Валидация данных записи.
    Возвращает (True, "") при успехе или (False, "сообщение об ошибке")
    """
    if not isinstance(data, dict):
        return False, "Данные должны быть JSON-объектом"

    required_fields = ["client_name", "client_phone", "master_id"]
    for field in required_fields:
        value = data.get(field)
        if not value or not isinstance(value, str) or not value.strip():
            return False, f"Поле '{field}' обязательно и не может быть пустым"

    try:
        master_id = int(data["master_id"])
        if master_id <= 0:
            return False, "master_id должен быть положительным числом"
        if not Master.select().where(Master.id == master_id).exists():
            return False, "Мастер с таким ID не найден"
    except (ValueError, TypeError):
        return False, "master_id должен быть целым числом"

    status = data.get("status", "pending").strip()
    allowed_statuses = ["pending", "confirmed", "completed", "cancelled"]
    if status not in allowed_statuses:
        return False, f"status может быть одним из: {', '.join(allowed_statuses)}"

    return True, ""


@appointments_bp.route("/", methods=["GET"])
@require_api_key
def get_appointments():
    """Получить все записи с возможной сортировкой."""
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
        return (
            jsonify({"error": "Ошибка при получении записей", "details": str(e)}),
            500,
        )


@appointments_bp.route("/<int:id>", methods=["GET"])
@require_api_key
def get_appointment(id):
    """Получить запись по ID."""
    try:
        appointment = Appointment.get(Appointment.id == id)
        return jsonify({"appointment": appointment_to_dict(appointment)}), 200
    except Appointment.DoesNotExist:
        return jsonify({"error": "Запись не найдена"}), 404
    except Exception as e:
        return jsonify({"error": "Ошибка", "details": str(e)}), 500


@appointments_bp.route("/master/<int:master_id>", methods=["GET"])
@require_api_key
def get_appointments_by_master(master_id):
    """Получить все записи для заданного мастера."""
    try:
        if not Master.select().where(Master.id == master_id).exists():
            return jsonify({"error": "Мастер не найден"}), 404

        appointments = Appointment.select().where(Appointment.master == master_id)
        result = [appointment_to_dict(a) for a in appointments]
        return jsonify({"appointments": result}), 200

    except Exception as e:
        return (
            jsonify({"error": "Ошибка при получении записей", "details": str(e)}),
            500,
        )


@appointments_bp.route("/", methods=["POST"])
@require_api_key
@require_admin
def create_appointment():
    """Создать новую запись."""
    try:
        data = request.json
        if not data or not isinstance(data, dict):
            return jsonify({"error": "Ожидается JSON"}), 400

        is_valid, msg = validate_appointment_data(data)
        if not is_valid:
            return jsonify({"error": msg}), 400

        master_id = int(data["master_id"])
        try:
            master = Master.get(Master.id == master_id)
        except Master.DoesNotExist:
            return jsonify({"error": "Мастер с таким ID не найден"}), 404

        appointment = Appointment.create(
            client_name=data["client_name"].strip(),
            client_phone=data["client_phone"].strip(),
            master=master,
            status=data.get("status", "pending").strip(),
        )
        return jsonify({"appointment": appointment_to_dict(appointment)}), 201

    except Exception as e:
        print(f"Ошибка при создании записи: {e}")
        return jsonify({"error": "Ошибка создания", "details": str(e)}), 500


@appointments_bp.route("/<int:id>", methods=["PUT"])
@require_api_key
@require_admin
def update_appointment(id):
    """Обновить запись."""
    try:
        appointment = Appointment.get(Appointment.id == id)
        data = request.json
        if not data or not isinstance(data, dict):
            return jsonify({"error": "Ожидается JSON"}), 400

        if "master_id" in data:
            master_id = data["master_id"]
            if not isinstance(master_id, int) or master_id <= 0:
                return (
                    jsonify({"error": "master_id должен быть положительным числом"}),
                    400,
                )
            if not Master.select().where(Master.id == master_id).exists():
                return jsonify({"error": "Мастер не найден"}), 400
            appointment.master = master_id

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

    except Appointment.DoesNotExist:
        return jsonify({"error": "Запись не найдена"}), 404
    except Exception as e:
        print(f"Ошибка при обновлении записи: {e}")
        return jsonify({"error": "Ошибка обновления", "details": str(e)}), 500


@appointments_bp.route("/<int:id>", methods=["DELETE"])
@require_api_key
@require_admin
def delete_appointment(id):
    """Удалить запись."""
    try:
        appointment = Appointment.get(Appointment.id == id)
        appointment.delete_instance()
        return "", 204
    except Appointment.DoesNotExist:
        return jsonify({"error": "Запись не найдена"}), 404
    except Exception as e:
        print(f"Ошибка при удалении записи: {e}")
        return jsonify({"error": "Ошибка удаления", "details": str(e)}), 500
