# cities_serializer.py
from typing import List, Dict, Any
from city import City


class CitiesSerializer:
    def __init__(self, city_data: List[Dict[str, Any]]):
        """
        Преобразует данные из JSON в список объектов City.
        Обрабатывает вложенность coords и конвертирует строки в числа.
        :param city_data: список словарей из JSON
        """
        self._cities: List[City] = []

        for item in city_data:
            try:
                coords = item.get("coords", {})
                lat_str = coords.get("lat")
                lon_str = coords.get("lon")

                if not lat_str or not lon_str:
                    raise ValueError("Отсутствуют координаты 'lat' или 'lon'")

                try:
                    latitude = float(lat_str)
                    longitude = float(lon_str)
                except (ValueError, TypeError):
                    raise ValueError(
                        f"Невозможно преобразовать координаты: lat={lat_str}, lon={lon_str}"
                    )

                city = City(
                    name=item["name"],
                    population=item["population"],
                    subject=item["subject"],
                    district=item["district"],
                    latitude=latitude,
                    longitude=longitude,
                )
                self._cities.append(city)

            except (KeyError, ValueError) as e:
                print(
                    f"[Ошибка] Пропущен город: {item.get('name', 'неизвестно')} — {e}"
                )

    def get_all_cities(self) -> List[City]:
        """
        Возвращает список валидных экземпляров City.
        :return: список объектов City
        """
        return self._cities
