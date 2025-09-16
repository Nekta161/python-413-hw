from datetime import datetime
from flask import Blueprint, request, jsonify
from auth import (
    is_valid_api_key,
    is_admin,
    unauthorized_response,
    require_api_key,
    require_admin,
)
from models import Master


# Создание блюпринта с префиксом /masters
masters_bp = Blueprint("masters", __name__, url_prefix="/masters")


def master_to_dict(master):
    """Преобразует объект Master в словарь."""
    return {
        "id": master.id,
        "first_name": master.first_name,
        "last_name": master.last_name,
        "middle_name": master.middle_name,
        "phone": master.phone,
    }


def validate_master_data(data):
    """
    Валидация данных мастера.
    Возвращает (True, "") при успехе или (False, "сообщение об ошибке")
    """
    if not isinstance(data, dict):
        return False, "Данные должны быть JSON-объектом"

    required_fields = ["first_name", "last_name", "phone"]
    for field in required_fields:
        value = data.get(field)
        if not value or not isinstance(value, str) or not value.strip():
            return False, f"Поле '{field}' обязательно и не может быть пустым"

    phone = data["phone"].strip()
    if len(phone) > 20:
        return False, "Поле 'phone' должно содержать не более 20 символов"

    return True, ""


# === Декораторы для авторизации ===
def require_api_key(f):
    """Декоратор: требует корректный API-ключ."""
    from functools import wraps

    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("api_key")
        if not is_valid_api_key(api_key):
            return unauthorized_response("Неверный API-ключ")
        return f(*args, **kwargs)

    return decorated_function


def require_admin(f):
    """Декоратор: требует права администратора."""
    from functools import wraps

    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("api_key")
        if not is_admin(api_key):
            return unauthorized_response(
                "Отказано в доступе. Требуются права администратора"
            )
        return f(*args, **kwargs)

    return decorated_function


# === Маршруты ===


@masters_bp.route("/", methods=["GET"])
@require_api_key
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


@masters_bp.route("/<int:id>", methods=["GET"])
@require_api_key
def get_master(id):
    """Получить мастера по ID."""
    try:
        master = Master.get(Master.id == id)
        return jsonify({"master": master_to_dict(master)}), 200
    except Master.DoesNotExist:
        return jsonify({"error": "Мастер не найден"}), 404
    except Exception as e:
        return jsonify({"error": "Ошибка", "details": str(e)}), 500


@masters_bp.route("/", methods=["POST"])
@require_api_key
@require_admin
def create_master():
    """Создать нового мастера."""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Ожидается JSON"}), 400

        is_valid, msg = validate_master_data(data)
        if not is_valid:
            return jsonify({"error": msg}), 400

        phone = data["phone"].strip()
        if Master.select().where(Master.phone == phone).exists():
            return jsonify({"error": "Телефон уже используется другим мастером"}), 400

        master = Master.create(
            first_name=data["first_name"].strip(),
            last_name=data["last_name"].strip(),
            middle_name=data.get("middle_name"),
            phone=phone,
        )
        return jsonify({"master": master_to_dict(master)}), 201
    except Exception as e:
        print(f"Ошибка при создании мастера: {e}")
        return jsonify({"error": "Ошибка создания", "details": str(e)}), 500


@masters_bp.route("/<int:id>", methods=["PUT"])
@require_api_key
@require_admin
def update_master(id):
    """Обновить информацию о мастере."""
    try:
        master = Master.get(Master.id == id)
        data = request.json
        if not data:
            return jsonify({"error": "Ожидается JSON"}), 400

        is_valid, msg = validate_master_data(data)
        if not is_valid:
            return jsonify({"error": msg}), 400

        phone = data["phone"].strip()
        # Проверка уникальности телефона (исключая текущего мастера)
        if Master.select().where((Master.phone == phone) & (Master.id != id)).exists():
            return jsonify({"error": "Телефон уже используется другим мастером"}), 400

        master.first_name = data["first_name"].strip()
        master.last_name = data["last_name"].strip()
        master.middle_name = data.get("middle_name")
        master.phone = phone
        master.save()

        return jsonify({"master": master_to_dict(master)}), 200
    except Master.DoesNotExist:
        return jsonify({"error": "Мастер не найден"}), 404
    except Exception as e:
        print(f"Ошибка при обновлении мастера: {e}")
        return jsonify({"error": "Ошибка обновления", "details": str(e)}), 500


@masters_bp.route("/<int:id>", methods=["DELETE"])
@require_api_key
@require_admin
def delete_master(id):
    """Удалить мастера и все его записи."""
    try:
        master = Master.get(Master.id == id)
        from models import Appointment

        Appointment.delete().where(Appointment.master == master).execute()
        master.delete_instance()
        return "", 204
    except Master.DoesNotExist:
        return jsonify({"error": "Мастер не найден"}), 404
    except Exception as e:
        print(f"Ошибка при удалении мастера: {e}")
        return jsonify({"error": "Ошибка удаления", "details": str(e)}), 500
