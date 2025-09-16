# game_manager.py
from typing import List
from city_game import CityGame
from cities_serializer import CitiesSerializer


class GameManager:
    def __init__(self, cities_serializer: CitiesSerializer, city_game: CityGame):
        """
        Фасад игры.
        :param cities_serializer: сериализатор городов
        :param city_game: логика игры
        """
        self.cities_serializer = cities_serializer
        self.city_game = city_game

    def __call__(self):
        self.run_game()

    def run_game(self):
        """
        Основной цикл: игрок ходит первым.
        """
        print("🎮 Добро пожаловать в игру 'Города'!")
        print(
            "Правила: называйте город на последнюю букву предыдущего (кроме 'ь', 'ъ')."
        )
        print("Вы ходите первым.\n")

        while not self.city_game.check_game_over():
            user_input = input("Ваш ход (город или 'стоп'): ").strip()
            if user_input.lower() in ("стоп", "exit", "quit"):
                print("Вы вышли из игры.")
                break

            if not self.city_game.human_turn(user_input):
                continue

            if self.city_game.check_game_over():
                print("\n🎉 Поздравляем! Компьютер не может ответить — вы победили!")
                break

            computer_city = self.city_game.computer_turn()
            if computer_city:
                print(f"Компьютер: {computer_city}")
            else:
                print("\n🎉 Компьютер сдаётся! Вы победили!")
                break
        else:
            print("\n😢 Вы не можете назвать город. Компьютер победил!")

        self.display_game_result()

    def display_game_result(self):
        """
        Вывод итогов.
        """
        total = len(self.city_game.used_cities)
        print(f"\n--- Игра окончена ---")
        print(f"Всего названо городов: {total}")
        if total > 0:
            print(f"Последний город: {self.city_game.used_cities[-1].name}")
