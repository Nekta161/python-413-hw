"""
Домашнее задание по теме: ORM-модели и скрипт наполнения БД «Барбершоп»
Технологии: Python, SQLite, PeeWee ORM
"""

from datetime import datetime
from peewee import (
    Model,
    SqliteDatabase,
    CharField,
    TextField,
    DecimalField,
    DateTimeField,
    ForeignKeyField,
)

# === Настройка базы данных ===
DB = SqliteDatabase("barbershop.db")


# === Определение моделей ===
class Master(Model):
    first_name = CharField(max_length=50, null=False)
    last_name = CharField(max_length=50, null=False)
    middle_name = CharField(max_length=50, null=True)
    phone = CharField(max_length=20, unique=True)

    class Meta:
        database = DB


class Service(Model):
    title = CharField(max_length=100, unique=True)
    description = TextField(null=True)
    price = DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        database = DB


class Appointment(Model):
    client_name = CharField(max_length=100, null=False)
    client_phone = CharField(max_length=20, null=False)
    date = DateTimeField(default=datetime.now)
    master = ForeignKeyField(Master, backref="appointments")
    status = CharField(max_length=20, default="pending")

    class Meta:
        database = DB


class MasterService(Model):
    master = ForeignKeyField(Master)
    service = ForeignKeyField(Service)

    class Meta:
        database = DB
        primary_key = False


class AppointmentService(Model):
    appointment = ForeignKeyField(Appointment)
    service = ForeignKeyField(Service)

    class Meta:
        database = DB
        primary_key = False


# === Основная логика скрипта ===
def main() -> None:
    """Основная функция: создаёт БД, таблицы, наполняет тестовыми данными и выводит результаты."""
    DB.connect()
    DB.create_tables(
        [Master, Service, Appointment, MasterService, AppointmentService], safe=True
    )

    # --- Добавляем мастеров (без дубликатов) ---
    masters_data = [
        {"first_name": "Иван", "last_name": "Петров", "phone": "+79123456789"},
        {
            "first_name": "Алексей",
            "last_name": "Сидоров",
            "middle_name": "Викторович",
            "phone": "+79234567890",
        },
        {"first_name": "Михаил", "last_name": "Кузнецов", "phone": "+79345678901"},
    ]
    created_masters = []
    for data in masters_data:
        master, created = Master.get_or_create(phone=data["phone"], defaults=data)
        created_masters.append(master)

    # --- Добавляем услуги ---
    services_data = [
        {
            "title": "Стрижка",
            "description": "Классическая стрижка ножницами и машинкой",
            "price": "500.00",
        },
        {
            "title": "Бритьё бороды",
            "description": "Традиционное бритьё горячим полотенцем",
            "price": "300.00",
        },
        {
            "title": "Укладка",
            "description": "Стильная укладка с фиксацией",
            "price": "400.00",
        },
        {"title": "Стрижка усов", "price": "150.00"},
    ]
    created_services = []
    for data in services_data:
        service, created = Service.get_or_create(title=data["title"], defaults=data)
        created_services.append(service)

    # --- Связываем мастеров и услуги (многие-ко-многим) ---
    master_service_links = [
        (1, 1),
        (1, 2),
        (1, 3),
        (1, 4),  # Иван — все услуги
        (2, 1),
        (2, 3),  # Алексей — стрижка и укладка
        (3, 2),  # Михаил — только бритьё
    ]
    for master_id, service_id in master_service_links:
        MasterService.get_or_create(master=master_id, service=service_id)

    # --- Добавляем заявки (уникальность по телефону клиента) ---
    appointments_data = [
        {
            "client_name": "Дмитрий",
            "client_phone": "+79456789012",
            "master": 1,
            "status": "pending",
        },
        {
            "client_name": "Сергей",
            "client_phone": "+79567890123",
            "master": 2,
            "status": "confirmed",
        },
        {
            "client_name": "Олег",
            "client_phone": "+79678901234",
            "master": 3,
            "status": "completed",
        },
    ]
    created_appointments = []
    for data in appointments_data:
        appointment, created = Appointment.get_or_create(
            client_phone=data["client_phone"], defaults=data
        )
        created_appointments.append(appointment)

    # --- Связываем заявки с услугами (каждая — 2 услуги) ---
    appointment_service_pairs = [
        (created_appointments[0].id, 1),  # Дмитрий: стрижка
        (created_appointments[0].id, 2),  # и бритьё
        (created_appointments[1].id, 1),  # Сергей: стрижка
        (created_appointments[1].id, 3),  # и укладка
        (created_appointments[2].id, 2),  # Олег: бритьё
        (created_appointments[2].id, 4),  # и стрижка усов
    ]
    for appt_id, svc_id in appointment_service_pairs:
        AppointmentService.get_or_create(appointment=appt_id, service=svc_id)

    # === Вывод данных в консоль ===
    print("\n" + "=" * 50)
    print("МАСТЕРА")
    print("=" * 50)
    for master in Master.select():
        middle = f" {master.middle_name}" if master.middle_name else ""
        print(f"• {master.last_name} {master.first_name}{middle}, тел: {master.phone}")

    print("\n" + "=" * 50)
    print("УСЛУГИ")
    print("=" * 50)
    for service in Service.select():
        desc = f" — {service.description}" if service.description else ""
        print(f"• {service.title}: {service.price} ₽{desc}")

    print("\n" + "=" * 50)
    print("ЗАЯВКИ НА УСЛУГИ")
    print("=" * 50)
    for appointment in Appointment.select().join(Master):
        print(f"\nКлиент: {appointment.client_name}, тел: {appointment.client_phone}")
        print(f"Мастер: {appointment.master.last_name} {appointment.master.first_name}")
        print(
            f"Дата: {appointment.date.strftime('%d.%m.%Y %H:%M')}, Статус: {appointment.status}"
        )
        # Получаем услуги через связь
        services = [
            link.service.title
            for link in AppointmentService.select()
            .join(Service)
            .where(AppointmentService.appointment == appointment)
        ]
        print("Услуги:", ", ".join(services) if services else "—")

    DB.close()


# === Запуск ===
if __name__ == "__main__":
    main()
