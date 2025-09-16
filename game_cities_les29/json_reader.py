# json_reader.py
import json
from typing import List, Dict


class JSONReader:
    @staticmethod
    def read_file(filepath: str) -> List[Dict]:
        """
        Считывает JSON-файл и возвращает список словарей.
        :param filepath: путь к файлу
        :return: список словарей с данными о городах
        """
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
