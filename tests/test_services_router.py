from fastapi.testclient import TestClient
from decimal import Decimal
from main import app
from models import Service

client = TestClient(app)


def test_create_service():
    # Verify no services exist initially
    assert Service.select().count() == 0

    service_data = {"name": "Test Service", "description": "A test service", "price": 100.00, "duration": 60}

    response = client.post("/services/", json=service_data, headers={"X-Medspa-ID": "1"})

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Service"
    assert data["description"] == "A test service"
    assert data["price"] == "100.0"
    assert data["duration"] == 60
    assert data["medspa_id"] == 1

    # Verify exactly one service was created
    assert Service.select().count() == 1


def test_update_service():
    # First create a service
    service = Service.create(
        medspa_id=1, name="Original Service", description="Original description", price=Decimal("50.00"), duration=30
    )

    # Verify exactly one service exists
    assert Service.select().count() == 1

    update_data = {"name": "Updated Service", "price": 75.00}

    response = client.post(f"/services/{service.id}", json=update_data, headers={"X-Medspa-ID": "1"})

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Service"
    assert data["price"] == "75.00"
    assert data["description"] == "Original description"  # Should remain unchanged
    assert data["duration"] == 30  # Should remain unchanged

    # Verify still exactly one service exists (update, not create)
    assert Service.select().count() == 1


def test_get_service():
    service = Service.create(
        medspa_id=1, name="Get Test Service", description="Service for get test", price=Decimal("25.00"), duration=15
    )

    response = client.get(f"/services/{service.id}", headers={"X-Medspa-ID": "1"})

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == service.id
    assert data["name"] == "Get Test Service"
    assert data["price"] == "25.00"


def test_get_all_services():
    # Create multiple services
    service1 = Service.create(medspa_id=1, name="Service 1", price=Decimal("10.00"), duration=10)
    service2 = Service.create(medspa_id=1, name="Service 2", price=Decimal("20.00"), duration=20)

    response = client.get("/services/", headers={"X-Medspa-ID": "1"})

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2

    # Verify the response contains both services (order doesn't matter)
    returned_ids = {service["id"] for service in data}
    expected_ids = {service1.id, service2.id}
    assert returned_ids == expected_ids
