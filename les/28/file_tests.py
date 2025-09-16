from file_classes import JsonFile, TxtFile, CsvFile


def test_json_file():
    print("Тестирование JsonFile:")
    json_file = JsonFile("test.json")
    json_file.write({"key1": "value1", "key2": "value2"})
    print("После записи:", json_file.read())
    json_file.append({"key3": "value3"})
    print("После добавления:", json_file.read())


def test_txt_file():
    print("\nТестирование TxtFile:")
    txt_file = TxtFile("test.txt")
    txt_file.write("Первая строка.")
    print("После записи:", txt_file.read())
    txt_file.append("Вторая строка.")
    print("После добавления:", txt_file.read())


def test_csv_file():
    print("\nТестирование CsvFile:")
    csv_file = CsvFile("test.csv")
    csv_file.write([["Name", "Age"], ["Alice", "30"], ["Bob", "25"]])
    print("После записи:", csv_file.read())
    csv_file.append(["Charlie", "35"])
    print("После добавления:", csv_file.read())


if __name__ == "__main__":
    test_json_file()
    test_txt_file()
    test_csv_file()