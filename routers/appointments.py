from fastapi import APIRouter, HTTPException, Depends
from typing import List
from peewee import prefetch
from models import Appointment, Service, AppointmentService
from schemas import AppointmentCreate, AppointmentUpdate, AppointmentResponse
from dependencies import get_medspa_id

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.post("/", response_model=AppointmentResponse)
def create_appointment(appointment: AppointmentCreate, medspa_id: int = Depends(get_medspa_id)):
    # Check if all services exist and belong to the medspa
    services = list(
        Service.select().where((Service.id.in_(appointment.service_ids)) & (Service.medspa_id == medspa_id))
    )

    if len(services) != len(appointment.service_ids):
        raise HTTPException(status_code=400, detail="One or more services not found")

    new_appointment = Appointment.create(
        medspa_id=medspa_id, start_time=appointment.start_time, status=appointment.status
    )

    # Associate services with appointment
    new_appointment.services.add(services)

    return AppointmentResponse.from_model(new_appointment)


@router.patch("/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(
    appointment_id: int, appointment_update: AppointmentUpdate, medspa_id: int = Depends(get_medspa_id)
):
    try:
        appointment = Appointment.get((Appointment.id == appointment_id) & (Appointment.medspa_id == medspa_id))
    except Appointment.DoesNotExist:
        raise HTTPException(status_code=404, detail="Appointment not found")

    appointment.status = appointment_update.status
    appointment.save()

    return AppointmentResponse.from_model(appointment)


@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(appointment_id: int, medspa_id: int = Depends(get_medspa_id)):
    try:
        appointment = Appointment.get((Appointment.id == appointment_id) & (Appointment.medspa_id == medspa_id))
    except Appointment.DoesNotExist:
        raise HTTPException(status_code=404, detail="Appointment not found")

    return AppointmentResponse.from_model(appointment)


@router.get("/", response_model=List[AppointmentResponse])
def get_all_appointments(medspa_id: int = Depends(get_medspa_id)):
    # todo: prefetch services
    appointments = Appointment.select().where(Appointment.medspa_id == medspa_id)

    result = []

    for appointment in appointments:
        result.append(AppointmentResponse.from_model(appointment))

    return result
