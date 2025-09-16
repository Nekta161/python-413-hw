import sqlite3
from typing import List, Tuple

# Константы
DB_PATH = "barbershop.db"
SQL_PATH = "setup_database.sql"


def read_sql_file(filepath: str) -> str:
    """
    Читает SQL-скрипт из файла и возвращает его содержимое.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def execute_script(conn, script: str) -> None:
    """
    Выполняет SQL-скрипт через курсор и сохраняет изменения.
    """
    cursor = conn.cursor()
    cursor.executescript(script)
    conn.commit()


def find_appointment_by_phone(conn, phone: str) -> List[Tuple]:
    """
    Ищет записи по точному номеру телефона.
    Возвращает: (имя, телефон, мастер, услуги, статус, комментарий)
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT 
            a.name,
            a.phone,
            m.first_name || ' ' || m.last_name AS master,
            GROUP_CONCAT(s.title, ', ') AS services,
            a.status,
            a.comment
        FROM Appointments a
        JOIN Masters m ON a.master_id = m.id
        JOIN appointments_services aps ON a.id = aps.appointment_id
        JOIN Services s ON aps.service_id = s.id
        WHERE a.phone = ?
        GROUP BY a.id
    """,
        (phone,),
    )
    return cursor.fetchall()


def find_appointment_by_comment(conn, comment_part: str) -> List[Tuple]:
    """
    Ищет записи, где комментарий содержит переданную строку.
    """
    cursor = conn.cursor()
    safe_part = comment_part.replace("%", "\\%").replace("_", "\\_")
    pattern = f"%{safe_part}%"
    cursor.execute(
        """
        SELECT 
            a.name,
            a.phone,
            m.first_name || ' ' || m.last_name AS master,
            GROUP_CONCAT(s.title, ', ') AS services,
            a.status,
            a.comment
        FROM Appointments a
        JOIN Masters m ON a.master_id = m.id
        JOIN appointments_services aps ON a.id = aps.appointment_id
        JOIN Services s ON aps.service_id = s.id
        WHERE a.comment LIKE ? ESCAPE '\\'
        GROUP BY a.id
    """,
        (pattern,),
    )
    return cursor.fetchall()


def create_appointment(
    conn,
    client_name: str,
    client_phone: str,
    master_name: str,
    services_list: List[str],
    comment: str = None,
) -> int:
    """
    Создаёт новую запись. Возвращает ID записи.
    """
    cursor = conn.cursor()

    # Найти мастера по имени
    first_name = master_name.strip().split()[0]
    cursor.execute("SELECT id FROM Masters WHERE first_name = ?", (first_name,))
    master = cursor.fetchone()
    if not master:
        raise ValueError(f"Мастер с именем {first_name} не найден")
    master_id = master[0]

    # Вставить запись
    cursor.execute(
        """
        INSERT INTO Appointments (name, phone, master_id, status, comment)
        VALUES (?, ?, ?, 'ожидает', ?)
    """,
        (client_name, client_phone, master_id, comment),
    )
    appointment_id = cursor.lastrowid

    # Привязать услуги
    for title in services_list:
        cursor.execute("SELECT id FROM Services WHERE title = ?", (title,))
        service = cursor.fetchone()
        if not service:
            raise ValueError(f"Услуга '{title}' не найдена")
        service_id = service[0]
        cursor.execute(
            """
            INSERT OR IGNORE INTO appointments_services (appointment_id, service_id)
            VALUES (?, ?)
        """,
            (appointment_id, service_id),
        )

    conn.commit()
    return appointment_id


# === Тестирование ===
if __name__ == "__main__":
    with sqlite3.connect(DB_PATH) as conn:
        sql = read_sql_file(SQL_PATH)
        execute_script(conn, sql)
        print("✅ База данных создана")

        print("\n🔍 Поиск по телефону +79111111111:")
        for row in find_appointment_by_phone(conn, "+79111111111"):
            print(row)

        print("\n🔍 Поиск по части комментария 'срочно':")
        for row in find_appointment_by_comment(conn, "срочно"):
            print(row)

        print("\n📝 Создание новой записи:")
        try:
            new_id = create_appointment(
                conn=conn,
                client_name="Евгений",
                client_phone="+79555555555",
                master_name="Александр",
                services_list=["Классическая стрижка", "Укладка"],
                comment="Срочно, до встречи с начальством",
            )
            print(f"✅ Запись создана: ID={new_id}")
        except ValueError as e:
            print(f"❌ Ошибка: {e}")

        print("\n🔍 Проверка новой записи:")
        for row in find_appointment_by_phone(conn, "+79555555555"):
            print(row)
