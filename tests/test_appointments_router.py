from fastapi.testclient import TestClient
from datetime import datetime
from decimal import Decimal
from main import app
from models import Service, Appointment

client = TestClient(app)


def test_create_appointment():
    # Verify no appointments exist initially
    assert Appointment.select().count() == 0

    # Create services first
    service1 = Service.create(medspa_id=1, name="Service 1", price=Decimal("50.00"), duration=30)
    service2 = Service.create(medspa_id=1, name="Service 2", price=Decimal("25.00"), duration=15)

    appointment_data = {
        "start_time": "2024-01-15T10:00:00",
        "service_ids": [service1.id, service2.id],
        "status": "scheduled",
    }

    response = client.post("/appointments/", json=appointment_data, headers={"X-Medspa-ID": "1"})

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "scheduled"
    assert data["medspa_id"] == 1
    assert len(data["services"]) == 2
    assert data["total_price"] == "75.00"
    assert data["total_duration"] == 45

    # Verify exactly one appointment was created
    assert Appointment.select().count() == 1


def test_update_appointment():
    # Create a service and appointment
    service = Service.create(medspa_id=1, name="Test Service", price=Decimal("30.00"), duration=20)

    appointment = Appointment.create(medspa_id=1, start_time=datetime(2024, 1, 15, 14, 0, 0), status="scheduled")
    appointment.services.add([service])

    # Verify exactly one appointment exists
    assert Appointment.select().count() == 1

    update_data = {"status": "completed"}

    response = client.patch(f"/appointments/{appointment.id}", json=update_data, headers={"X-Medspa-ID": "1"})

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert data["id"] == appointment.id

    # Verify still exactly one appointment exists (update, not create)
    assert Appointment.select().count() == 1


def test_get_appointment():
    service = Service.create(medspa_id=1, name="Get Test Service", price=Decimal("40.00"), duration=25)

    appointment = Appointment.create(medspa_id=1, start_time=datetime(2024, 1, 20, 9, 0, 0), status="scheduled")
    appointment.services.add([service])

    response = client.get(f"/appointments/{appointment.id}", headers={"X-Medspa-ID": "1"})

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == appointment.id
    assert data["status"] == "scheduled"
    assert len(data["services"]) == 1


def test_get_all_appointments():
    # Create services
    service = Service.create(medspa_id=1, name="List Test Service", price=Decimal("15.00"), duration=10)

    # Create appointments
    appointment1 = Appointment.create(medspa_id=1, start_time=datetime(2024, 1, 25, 10, 0, 0), status="scheduled")
    appointment1.services.add([service])

    appointment2 = Appointment.create(medspa_id=1, start_time=datetime(2024, 1, 25, 11, 0, 0), status="completed")
    appointment2.services.add([service])

    response = client.get("/appointments/", headers={"X-Medspa-ID": "1"})

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2

    # Verify the response contains both appointments (order doesn't matter)
    returned_ids = {appointment["id"] for appointment in data}
    expected_ids = {appointment1.id, appointment2.id}
    assert returned_ids == expected_ids
