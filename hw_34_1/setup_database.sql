PRAGMA foreign_keys = OFF;

BEGIN TRANSACTION;

-- Удаление таблиц, если уже существуют
DROP TABLE IF EXISTS appointments_services;
DROP TABLE IF EXISTS masters_services;
DROP TABLE IF EXISTS Appointments;
DROP TABLE IF EXISTS Services;
DROP TABLE IF EXISTS Masters;

-- Создание таблицы "Мастера"
CREATE TABLE IF NOT EXISTS Masters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    middle_name TEXT,
    phone TEXT NOT NULL UNIQUE
);

-- Создание таблицы "Услуги"
CREATE TABLE IF NOT EXISTS Services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL UNIQUE,
    description TEXT,
    price REAL NOT NULL CHECK (price >= 0)
);

-- Создание таблицы "Запись на услуги"
CREATE TABLE IF NOT EXISTS Appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    Дата DATETIME DEFAULT CURRENT_TIMESTAMP,
    master_id INTEGER NOT NULL,
    status TEXT DEFAULT 'ожидает',
    comment TEXT,
    FOREIGN KEY (master_id) REFERENCES Masters(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Связующая таблица: мастера и услуги
CREATE TABLE IF NOT EXISTS masters_services (
    master_id INTEGER NOT NULL,
    service_id INTEGER NOT NULL,
    PRIMARY KEY (master_id, service_id),
    FOREIGN KEY (master_id) REFERENCES Masters(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (service_id) REFERENCES Services(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Связующая таблица: записи и услуги
CREATE TABLE IF NOT EXISTS appointments_services (
    appointment_id INTEGER NOT NULL,
    service_id INTEGER NOT NULL,
    PRIMARY KEY (appointment_id, service_id),
    FOREIGN KEY (appointment_id) REFERENCES Appointments(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (service_id) REFERENCES Services(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Вставка: 2 мастера
INSERT INTO Masters (first_name, last_name, middle_name, phone) VALUES
('Александр', 'Волков', 'Петрович', '+79001234567'),
('Михаил', 'Кузнецов', 'Сергеевич', '+79007654321');

-- Вставка: 5 услуг
INSERT INTO Services (title, description, price) VALUES
('Классическая стрижка', 'Стрижка ножницами и машинкой', 700.0),
('Стрижка + борода', 'Полная стрижка и укладка бороды', 1100.0),
('Бритьё опасной бритвой', 'Традиционное бритьё с паром', 900.0),
('Детская стрижка', 'Для детей до 12 лет', 500.0),
('Укладка', 'Стилевая укладка с феном и воском', 400.0);

-- Связь: мастера и услуги
INSERT INTO masters_services (master_id, service_id) VALUES
(1, 1), (1, 2), (1, 3), (1, 5),
(2, 1), (2, 4), (2, 5);

-- Вставка: 4 записи
INSERT INTO Appointments (name, phone, master_id, status, comment) VALUES
('Иван', '+79111111111', 1, 'подтверждена', 'Хочу стрижку как у Тони Старка'),
('Олег', '+79222222222', 1, 'ожидает', 'Первый раз, посоветуйте что-то'),
('Дмитрий', '+79333333333', 2, 'отменена', 'Не успеваю, перенесём'),
('Артём', '+79444444444', 2, 'подтверждена', 'Срочно, до встречи с девушкой');

-- Связь: записи и услуги
INSERT INTO appointments_services (appointment_id, service_id) VALUES
(1, 2),
(2, 1), (2, 5),
(3, 3),
(4, 4), (4, 5);

-- Индекс 1: ускоряет поиск по телефону клиента
CREATE INDEX IF NOT EXISTS idx_appointments_phone ON Appointments(phone);

-- Индекс 2: ускоряет поиск по статусу записи
CREATE INDEX IF NOT EXISTS idx_appointments_status ON Appointments(status);

-- Составной индекс 3: ускоряет поиск по мастеру и дате
CREATE INDEX IF NOT EXISTS idx_appointments_master_date ON Appointments(master_id, Дата);

-- Составной индекс 4: ускоряет поиск услуг по мастеру
CREATE INDEX IF NOT EXISTS idx_masters_services_lookup ON masters_services(master_id, service_id);

COMMIT;

PRAGMA foreign_keys = ON;