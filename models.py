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
)

db = PostgresqlDatabase("moxiedb")


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

    class Meta:
        table_name = "appointments"


class AppointmentService(BaseModel):
    id = BigAutoField(primary_key=True)
    appointment = ForeignKeyField(Appointment, backref="appointment_services", on_delete="CASCADE")
    service = ForeignKeyField(Service, backref="appointment_services", on_delete="CASCADE")

    class Meta:
        table_name = "appointment_services"
