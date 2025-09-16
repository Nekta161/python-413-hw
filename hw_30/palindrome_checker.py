# palindrome_checker.py
from abc import ABC, abstractmethod
from typing import Protocol


class PalindromeStrategy(Protocol):
    """
    Абстрактный интерфейс для стратегий проверки палиндромов.
    """

    def is_palindrome(self, text: str) -> bool: ...


class SingleWordPalindrome:
    """
    Стратегия проверки одиночного слова на палиндром (без учёта регистра).
    """

    def is_palindrome(self, text: str) -> bool:
        """
        Проверяет, является ли слово палиндромом.
        :param text: строка (одно слово)
        :return: True, если слово — палиндром
        """
        clean = text.strip().lower()
        return clean == clean[::-1]


class MultiWordPalindrome:
    """
    Стратегия проверки многословного выражения на палиндром.
    Игнорирует пробелы и регистр.
    """

    def is_palindrome(self, text: str) -> bool:
        """
        Проверяет, является ли фраза палиндромом.
        :param text: строка (фраза)
        :return: True, если фраза — палиндром
        """
        clean = "".join(text.split()).lower()
        return clean == clean[::-1]


class PalindromeContext:
    """
    Контекст, использующий стратегию проверки палиндрома.
    """

    def __init__(self, strategy: PalindromeStrategy):
        """
        Инициализация контекста с начальной стратегией.
        :param strategy: реализация PalindromeStrategy
        """
        self._strategy = strategy

    def set_strategy(self, strategy: PalindromeStrategy) -> None:
        """
        Устанавливает новую стратегию.
        :param strategy: новая стратегия
        """
        self._strategy = strategy

    def check(self, text: str) -> bool:
        """
        Проверяет текст с помощью текущей стратегии.
        :param text: строка для проверки
        :return: результат проверки
        """
        return self._strategy.is_palindrome(text)


class PalindromeFacade:
    """
    Фасад для упрощённой проверки палиндромов.
    Автоматически выбирает стратегию в зависимости от количества слов.
    """

    def __init__(self):
        """Инициализация фасада с контекстом."""
        self._context = PalindromeContext(SingleWordPalindrome())

    def check_palindrome(self, text: str) -> bool:
        """
        Проверяет, является ли текст палиндромом.
        Автоматически выбирает стратегию:
        - Одно слово → SingleWordPalindrome
        - Несколько слов → MultiWordPalindrome
        :param text: строка для проверки
        :return: True, если палиндром
        """
        if not text or not text.strip():
            return False

        words = text.strip().split()
        if len(words) == 1:
            self._context.set_strategy(SingleWordPalindrome())
        else:
            self._context.set_strategy(MultiWordPalindrome())

        return self._context.check(text)


# ——————————————————————————————————————————
# Пример использования
# ——————————————————————————————————————————
if __name__ == "__main__":
    facade = PalindromeFacade()

    # Тест 1: Одиночное слово-палиндром
    word = "Racecar"
    print(f"'{word}' — палиндром? {facade.check_palindrome(word)}")  # True

    # Тест 2: Одиночное слово не палиндром
    word = "Python"
    print(f"'{word}' — палиндром? {facade.check_palindrome(word)}")  # False

    # Тест 3: Многословное выражение-палиндром
    phrase = "A man a plan a canal Panama"
    print(f"'{phrase}' — палиндром? {facade.check_palindrome(phrase)}")  # True

    # Тест 4: Многословное выражение не палиндром
    phrase = "Hello World"
    print(f"'{phrase}' — палиндром? {facade.check_palindrome(phrase)}")  # False

    # Тест 5: Одно слово с разными регистрами
    word = "Deified"
    print(f"'{word}' — палиндром? {facade.check_palindrome(word)}")  # True

    # Тест 6: Сложная фраза с пробелами
    phrase = "Was it a car or a cat I saw"
    print(f"'{phrase}' — палиндром? {facade.check_palindrome(phrase)}")  # True

    # Тест 7: Пустая строка
    empty = ""
    print(f"'{empty}' — палиндром? {facade.check_palindrome(empty)}")  # False

    # Тест 8: Пробелы
    spaces = "   "
    print(f"'{spaces}' — палиндром? {facade.check_palindrome(spaces)}")  # False
