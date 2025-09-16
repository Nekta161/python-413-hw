# main.py
from json_reader import JSONReader
from cities_serializer import CitiesSerializer


def main():
    # 1. Чтение данных из JSON
    reader = JSONReader()
    try:
        data = reader.read_file("cities.json")
    except FileNotFoundError:
        print("Ошибка: файл cities.json не найден.")
        return
    except json.JSONDecodeError as e:
        print(f"Ошибка: файл cities.json содержит некорректный JSON: {e}")
        return

    # 2. Сериализация: JSON → City
    serializer = CitiesSerializer(data)
    cities = serializer.get_all_cities()

    # 3. Вывод статистики и списка
    print(f"Загружено {len(cities)} городов.\n")

    print("Список городов (объекты City):")
    for city in cities:
        print(city)

    # Найти Абаза и Абакан
    abaza = next((c for c in cities if c.name == "Абаза"), None)
    abakan = next((c for c in cities if c.name == "Абакан"), None)

    if abaza and abakan:
        result = abaza > abakan
        print(
            f"{abaza.name} ({abaza.population:,}) > {abakan.name} ({abakan.population:,})? {result}"
        )
    elif not abaza:
        print("Город 'Абаза' не найден в данных.")
    elif not abakan:
        print("Город 'Абакан' не найден в данных.")

    # 5. Самый большой город
    if cities:
        largest = max(cities)
        print(f"\nСамый большой город: {largest}")
    else:
        print("\nНет валидных городов для анализа.")


if __name__ == "__main__":
    main()
