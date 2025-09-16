import sqlite3

# Подключаемся к базе (если нет — создастся)
conn = sqlite3.connect("barbershop.db")
cursor = conn.cursor()

# Читаем SQL-файл
try:
    with open("barbershop_setup.sql", "r", encoding="utf-8") as f:
        sql_script = f.read()

    # Выполняем все команды
    cursor.executescript(sql_script)
    conn.commit()
    print("✅ Успех! База данных 'barbershop.db' создана и заполнена.")
except Exception as e:
    print(f"❌ Ошибка: {e}")
finally:
    conn.close()
