# main.py
from json_reader import JSONReader
from cities_serializer import CitiesSerializer
from city_game import CityGame
from game_manager import GameManager
import os


def main():
    # 🔹 Гарантированно ищем файл в папке скрипта
    file_path = os.path.join(os.path.dirname(__file__), "cities.json")

    if not os.path.exists(file_path):
        print(f"❌ Файл не найден: {file_path}")
        print("👉 Убедитесь, что 'cities.json' лежит в той же папке, что и 'main.py'.")
        return

    try:
        reader = JSONReader()
        data = reader.read_file(file_path)
    except Exception as e:
        print(f"❌ Ошибка чтения JSON: {e}")
        return

    serializer = CitiesSerializer(data)
    game = CityGame(serializer)
    manager = GameManager(serializer, game)

    # Запуск игры
    manager()


if __name__ == "__main__":
    main()
