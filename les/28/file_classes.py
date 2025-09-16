from abc import ABC, abstractmethod
import json
import csv


class AbstractFile(ABC):
    """
    Абстрактный класс для работы с файлами.
    Предписывает методы для чтения, записи и добавления данных в файл.
    """

    @abstractmethod
    def read(self):
        """Чтение данных из файла."""
        pass

    @abstractmethod
    def write(self, data):
        """Запись данных в файл."""
        pass

    @abstractmethod
    def append(self, data):
        """Добавление данных в файл."""
        pass


class JsonFile(AbstractFile):
    """
    Класс для работы с JSON-файлами.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

    def read(self) -> dict:
        """Чтение данных из JSON-файла."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Файл {self.file_path} не найден.")
            return {}
        except json.JSONDecodeError:
            print(f"Файл {self.file_path} содержит некорректные данные JSON.")
            return {}

    def write(self, data: dict):
        """Запись данных в JSON-файл."""
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def append(self, data: dict):
        """Добавление данных в JSON-файл."""
        existing_data = self.read()
        existing_data.update(data)
        self.write(existing_data)



class TxtFile(AbstractFile):
    """
    Класс для работы с текстовыми файлами.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

    def read(self) -> str:
        """Чтение данных из текстового файла."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Файл {self.file_path} не найден.")
            return ""

    def write(self, data: str):
        """Запись данных в текстовый файл."""
        with open(self.file_path, 'w', encoding='utf-8') as file:
            file.write(data)

    def append(self, data: str):
        """Добавление данных в текстовый файл."""
        with open(self.file_path, 'a', encoding='utf-8') as file:
            file.write(data + '\n')


class CsvFile(AbstractFile):
    """
    Класс для работы с CSV-файлами.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

    def read(self) -> list[list[str]]:
        """Чтение данных из CSV-файла."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                return [row for row in reader]
        except FileNotFoundError:
            print(f"Файл {self.file_path} не найден.")
            return []

    def write(self, data: list[list[str]]):
        """Запись данных в CSV-файл."""
        with open(self.file_path, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

    def append(self, data: list[str]):
        """Добавление данных в CSV-файл."""
        with open(self.file_path, 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)