# city_game.py
from typing import Optional, List
from city import City


class CityGame:
    def __init__(self, cities_serializer):
        """
        Инициализация игры.
        :param cities_serializer: сериализатор, возвращающий список городов
        """
        self.cities_serializer = cities_serializer
        self.cities: List[City] = self.cities_serializer.get_all_cities()
        self.used_cities: List[City] = []
        self.last_letter: Optional[str] = None  # буква для следующего хода

    def human_turn(self, city_input: str) -> bool:
        """
        Ход игрока.
        :param city_input: название города
        :return: True, если ход корректный
        """
        city_name = city_input.strip().title()
        if not city_name:
            print("Ошибка: введите название города.")
            return False

        city_obj = next((c for c in self.cities if c.name == city_name), None)
        if not city_obj:
            print(f"Ошибка: город '{city_name}' не найден.")
            return False

        if city_obj in self.used_cities:
            print(f"Ошибка: город '{city_name}' уже использован.")
            return False

        if self.last_letter:
            first_letter = self._get_first_letter(city_name)
            if first_letter.lower() != self.last_letter.lower():
                print(
                    f"Ошибка: город должен начинаться с буквы '{self.last_letter.upper()}'."
                )
                return False

        self.used_cities.append(city_obj)
        self.last_letter = self._get_last_letter(city_name)
        return True

    def computer_turn(self) -> str:
        """
        Ход компьютера.
        :return: название города или пустая строка
        """
        if not self.last_letter:
            return ""

        available = [
            c
            for c in self.cities
            if c not in self.used_cities
            and self._get_first_letter(c.name).lower() == self.last_letter.lower()
        ]

        if available:
            chosen = available[0]
            self.used_cities.append(chosen)
            self.last_letter = self._get_last_letter(chosen.name)
            return chosen.name

        return ""

    def check_game_over(self) -> bool:
        """
        Проверяет, может ли компьютер ответить.
        :return: True, если игра окончена
        """
        if not self.last_letter:
            return False
        return not any(
            c not in self.used_cities
            and self._get_first_letter(c.name).lower() == self.last_letter.lower()
            for c in self.cities
        )

    @staticmethod
    def _get_first_letter(name: str) -> str:
        return name[0] if name else ""

    @staticmethod
    def _get_last_letter(name: str) -> str:
        name = name.lower()
        for char in reversed(name):
            if char not in "ьъ":
                return char
        return name[-1]
