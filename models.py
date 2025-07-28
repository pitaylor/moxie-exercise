from peewee import (
    BigAutoField,
    CharField,
    TextField,
    ForeignKeyField,
    IntegerField,
    DecimalField,
    Model,
    PostgresqlDatabase,
)

db = PostgresqlDatabase("moxiedb")


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
    duration_minutes = IntegerField()

    class Meta:
        table_name = "services"
