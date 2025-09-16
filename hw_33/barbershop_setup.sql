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
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    master_id INTEGER NOT NULL,
    status TEXT DEFAULT 'ожидает',
    FOREIGN KEY (master_id) REFERENCES Masters(id) ON DELETE CASCADE ON UPDATE CASCADE
);
;

-- Создание связующей таблицы "masters_services" (связь многие-ко-многим: мастера и услуги)
CREATE TABLE IF NOT EXISTS masters_services (
    master_id INTEGER NOT NULL,
    service_id INTEGER NOT NULL,
    PRIMARY KEY (master_id, service_id),
    FOREIGN KEY (master_id) REFERENCES Masters(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (service_id) REFERENCES Services(id) ON DELETE CASCADE ON UPDATE CASCADE
);
;

-- Создание связующей таблицы "appointments_services" (связь многие-ко-многим: запись и услуги)
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
('Алексей', 'Иванов', 'Сергеевич', '+79123456789'),
('Дмитрий', 'Петров', 'Андреевич', '+79234567890');
;

-- Добавление данных: 5 услуг
INSERT INTO Services (title, description, price) VALUES
('Стрижка классическая', 'Классическая стрижка ножницами и машинкой', 800.0),
('Стрижка + борода', 'Полная стрижка головы и моделирование бороды', 1200.0),
('Бритьё опасной бритвой', 'Традиционное бритьё с пеной и разогретым полотенцем', 1000.0),
('Укладка', 'Стилевая укладка с использованием средств', 500.0),
('Детская стрижка', 'Стрижка для детей до 12 лет', 600.0);
;

-- Связывание мастеров и услуг: Алексей делает все, кроме детской
INSERT INTO masters_services (master_id, service_id) VALUES
(1, 1), -- Алексей — стрижка классическая
(1, 2), -- Алексей — стрижка + борода
(1, 3), -- Алексей — бритьё опасной бритвой
(1, 4), -- Алексей — укладка
(2, 1), -- Дмитрий — стрижка классическая
(2, 4), -- Дмитрий — укладка
(2, 5); -- Дмитрий — детская стрижка
;

-- Добавление 4 записей на услуги
INSERT INTO Appointments (name, phone, master_id, status) VALUES
('Иван Сидоров', '+79345678901', 1, 'подтверждена'),
('Максим Кузнецов', '+79456789012', 1, 'ожидает'),
('Олег Фролов', '+79567890123', 2, 'отменена'),
('Артём Лебедев', '+79678901234', 2, 'подтверждена');
;

-- Связывание записей и услуг
INSERT INTO appointments_services (appointment_id, service_id) VALUES
(1, 2), -- Иван: стрижка + борода
(2, 1), -- Максим: классическая стрижка
(2, 4), -- Максим: + укладка
(3, 3), -- Олег: бритьё опасной бритвой
(4, 5), -- Артём: детская стрижка
(4, 4); -- Артём: + укладка
;

-- Пример обновления статуса записи
UPDATE Appointments
SET status = 'завершена'
WHERE id = 1;
;