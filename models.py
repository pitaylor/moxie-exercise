import os
from enum import Enum
from peewee import (
    BigAutoField,
    CharField,
    TextField,
    ForeignKeyField,
    IntegerField,
    DecimalField,
    DateTimeField,
    Model,
    PostgresqlDatabase,
    ManyToManyField,
)

DB_NAME = os.getenv("DATABASE_NAME", "moxiedb")
DB_USER = os.getenv("DATABASE_USER", "postgres")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD", "postgres")
DB_HOST = os.getenv("DATABASE_HOST", "localhost")
DB_PORT = os.getenv("DATABASE_PORT", "5432")
db = PostgresqlDatabase(DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=int(DB_PORT))


class AppointmentStatus(Enum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELED = "canceled"


class BaseModel(Model):
    class Meta:
        database = db


class Medspa(BaseModel):
    id = BigAutoField(primary_key=True)
    name = CharField(max_length=255, unique=True)
    address = TextField()
    phone_number = CharField(max_length=20)
    email_address = CharField(max_length=254)

    class Meta:
        table_name = "medspas"


class Service(BaseModel):
    id = BigAutoField(primary_key=True)
    medspa = ForeignKeyField(Medspa, backref="services", on_delete="CASCADE")
    name = CharField(max_length=255)
    description = TextField(null=True)
    price = DecimalField(max_digits=10, decimal_places=2)
    duration = IntegerField()

    class Meta:
        table_name = "services"


class Appointment(BaseModel):
    id = BigAutoField(primary_key=True)
    medspa = ForeignKeyField(Medspa, backref="appointments", on_delete="CASCADE")
    start_time = DateTimeField()
    status = CharField(max_length=20, default=AppointmentStatus.SCHEDULED.value)
    services = ManyToManyField(Service, backref="appointments")

    @property
    def total_duration(self):
        return sum(service.duration for service in self.services)

    @property
    def total_price(self):
        return sum(service.price for service in self.services)

    class Meta:
        table_name = "appointments"


AppointmentService = Appointment.services.through_model
