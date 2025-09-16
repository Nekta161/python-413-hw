-- Создание таблицы "Мастера"
CREATE TABLE IF NOT EXISTS Masters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    middle_name TEXT,
    phone TEXT NOT NULL
);
;

-- Создание таблицы "Услуги"
CREATE TABLE IF NOT EXISTS Services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL UNIQUE,
    description TEXT,
    price REAL NOT NULL CHECK (price >= 0)
);
;

-- Создание таблицы "Запись на услуги"
CREATE TABLE IF NOT EXISTS Appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    Дата DATETIME DEFAULT CURRENT_TIMESTAMP,
    master_id INTEGER NOT NULL,
    status TEXT DEFAULT 'ожидает',
    FOREIGN KEY (master_id) REFERENCES Masters(id) ON DELETE CASCADE ON UPDATE CASCADE
);
;

-- Создание связующей таблицы "masters_services"
CREATE TABLE IF NOT EXISTS masters_services (
    master_id INTEGER NOT NULL,
    service_id INTEGER NOT NULL,
    PRIMARY KEY (master_id, service_id),
    FOREIGN KEY (master_id) REFERENCES Masters(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (service_id) REFERENCES Services(id) ON DELETE CASCADE ON UPDATE CASCADE
);
;

-- Создание связующей таблицы "appointments_services"
CREATE TABLE IF NOT EXISTS appointments_services (
    appointment_id INTEGER NOT NULL,
    service_id INTEGER NOT NULL,
    PRIMARY KEY (appointment_id, service_id),
    FOREIGN KEY (appointment_id) REFERENCES Appointments(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (service_id) REFERENCES Services(id) ON DELETE CASCADE ON UPDATE CASCADE
);
;

-- Добавление данных: 2 мастера
INSERT INTO Masters (first_name, last_name, middle_name, phone) VALUES
('Александр', 'Волков', 'Петрович', '+79001234567'),
('Михаил', 'Кузнецов', 'Сергеевич', '+79007654321');
;

-- Добавление данных: 5 услуг
INSERT INTO Services (title, description, price) VALUES
('Классическая стрижка', 'Стрижка ножницами и машинкой', 700.0),
('Стрижка + борода', 'Полная стрижка и укладка бороды', 1100.0),
('Бритьё опасной бритвой', 'Традиционное бритьё с паром', 900.0),
('Детская стрижка', 'Для детей до 12 лет', 500.0),
('Укладка', 'Стилевая укладка с феном и воском', 400.0);
;

-- Связывание мастеров и услуг
INSERT INTO masters_services (master_id, service_id) VALUES
(1, 1), -- Александр — классическая стрижка
(1, 2), -- Александр — стрижка + борода
(1, 3), -- Александр — бритьё
(1, 5), -- Александр — укладка
(2, 1), -- Михаил — классическая стрижка
(2, 4), -- Михаил — детская стрижка
(2, 5); -- Михаил — укладка
;

-- Добавление 4 записей на услуги
INSERT INTO Appointments (name, phone, master_id, status) VALUES
('Иван', '+79111111111', 1, 'подтверждена'),
('Олег', '+79222222222', 1, 'ожидает'),
('Дмитрий', '+79333333333', 2, 'отменена'),
('Артём', '+79444444444', 2, 'подтверждена');
;

-- Связывание записей и услуг
INSERT INTO appointments_services (appointment_id, service_id) VALUES
(1, 2), -- Иван — стрижка + борода
(2, 1), -- Олег — классическая стрижка
(2, 5), -- Олег — укладка
(3, 3), -- Дмитрий — бритьё
(4, 4), -- Артём — детская стрижка
(4, 5); -- Артём — укладка
;

-- Обновление статуса записи
UPDATE Appointments
SET status = 'завершена'
WHERE id = 1;
;