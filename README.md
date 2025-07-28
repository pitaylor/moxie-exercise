# Appointment Booking API

An appointment booking API for medspas.

## Getting Started

There are two ways to run the API:

### Option A: Using Docker (Easiest)

**Prerequisites:** Docker, Docker Compose

```bash
docker compose up
```

### Option B: Local Development

This option allows you to run tests.

**Prerequisites:** Python 3.13, PostgreSQL, [uv](https://docs.astral.sh/uv/), [Task](https://taskfile.dev/)

```bash
# Install dependencies
uv sync

# Create databases and load sample data
task setup

# Start the development server
task start

# Run tests
task test
```

### API Usage

The API will be available at `http://localhost:8000`. The interactive Swagger UI can be accessed at `http://localhost:8000/docs`.

All API requests require a `X-Medspa-ID` header to identify the medspa.

#### Services API Examples

```bash
# Create a service
curl -X POST "http://localhost:8000/services/" \
  -H "Content-Type: application/json" \
  -H "X-Medspa-ID: 1" \
  -d '{"name": "Facial Treatment", "price": 250.00, "duration": 60}'

# List All Services
curl -X GET "http://localhost:8000/services/" -H "X-Medspa-ID: 1"

# Get a Specific Service
curl -X GET "http://localhost:8000/services/1" -H "X-Medspa-ID: 1"

# Update a Service
curl -X POST "http://localhost:8000/services/1" \
  -H "Content-Type: application/json" \
  -H "X-Medspa-ID: 1" \
  -d '{"price": 175.00, "duration": 75}'
```

#### Appointments API Examples

```bash
# Create an Appointment
curl -X POST "http://localhost:8000/appointments/" \
  -H "Content-Type: application/json" \
  -H "X-Medspa-ID: 1" \
  -d '{"start_time": "2024-01-15T14:00:00", "service_ids": [1, 2], "status": "scheduled"}'

# List All Appointments
curl -X GET "http://localhost:8000/appointments/" -H "X-Medspa-ID: 1"

# Get a Specific Appointment
curl -X GET "http://localhost:8000/appointments/1" -H "X-Medspa-ID: 1"

# Update Appointment Status
curl -X PATCH "http://localhost:8000/appointments/1" \
  -H "Content-Type: application/json" \
  -H "X-Medspa-ID: 1" \
  -d '{"status": "completed"}'
```
