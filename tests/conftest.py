import pytest
from models import db, Service, Appointment


@pytest.fixture(autouse=True)
def clear_tables():
    """Clear appointment and service tables before each test."""
    Appointment.delete().execute()
    Service.delete().execute()

    yield

    Appointment.delete().execute()
    Service.delete().execute()


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Ensure database connection is established for tests."""
    db.connect()
    yield
    db.close()
