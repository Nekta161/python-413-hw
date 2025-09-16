"""
Модуль аутентификации: проверка API-ключей и ролей.
"""

import json
from typing import Dict, List
from flask import Response
from functools import wraps


# Список пользователей с API-ключами и ролями
USERS = [
    {"username": "admin", "api_key": "admin_secret_key_123", "role": "admin"},
    {"username": "user", "api_key": "user_readonly_key_456", "role": "user"},
]


def is_valid_api_key(api_key: str) -> bool:
    """
    Проверяет, является ли API-ключ действительным.
    """
    print(f"DEBUG: Received header 'api_key' = {repr(api_key)}")
    if not api_key:
        return False
    api_key = api_key.strip()
    return any(user["api_key"] == api_key for user in USERS)


def is_admin(api_key: str) -> bool:
    """
    Проверяет, является ли пользователь администратором.
    """
    if not api_key:
        return False
    api_key = api_key.strip()
    return any(user["api_key"] == api_key and user["role"] == "admin" for user in USERS)


def unauthorized_response(message: str) -> Response:
    """
    Возвращает JSON-ответ с ошибкой 403 и поддержкой кириллицы.
    """
    return Response(
        json.dumps({"error": message}, ensure_ascii=False),
        status=403,
        mimetype="application/json; charset=utf-8",
    )


# === Декораторы для авторизации ===


def require_api_key(f):
    """
    Декоратор: требует корректный API-ключ.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("api_key")
        if not is_valid_api_key(api_key):
            return unauthorized_response("Неверный API-ключ")
        return f(*args, **kwargs)

    return decorated_function


def require_admin(f):
    """
    Декоратор: требует права администратора.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("api_key")
        if not is_admin(api_key):
            return unauthorized_response(
                "Отказано в доступе. Требуются права администратора"
            )
        return f(*args, **kwargs)

    return decorated_function
