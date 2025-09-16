"""
ORM-модели для барбершопа: Master и Appointment
Созданы на основе PeeWee ORM. Поле id добавляется автоматически.
"""

from datetime import datetime
from peewee import (
    Model,
    SqliteDatabase,
    CharField,
    DateTimeField,
    ForeignKeyField,
)

# Подключение к SQLite-базе
DB = SqliteDatabase("barbershop.db")


class Master(Model):
    """
    Модель мастера барбершопа.
    """

    first_name = CharField(max_length=50, null=False)
    last_name = CharField(max_length=50, null=False)
    middle_name = CharField(max_length=50, null=True)
    phone = CharField(max_length=20, unique=True)

    class Meta:
        database = DB


class Appointment(Model):
    """
    Модель записи на услугу.
    """

    client_name = CharField(max_length=100, null=False)
    client_phone = CharField(max_length=20, null=False)
    date = DateTimeField(default=datetime.now)
    master = ForeignKeyField(Master, backref="appointments")
    status = CharField(max_length=20, default="pending")

    class Meta:
        database = DB
