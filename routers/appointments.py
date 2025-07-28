from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models import Appointment, AppointmentService, Service
from schemas import AppointmentCreate, AppointmentUpdate, AppointmentResponse, ServiceResponse
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

    # Create appointment-service relationships
    for service_id in appointment.service_ids:
        AppointmentService.create(appointment=new_appointment, service_id=service_id)

    services_data = [ServiceResponse.model_validate(service) for service in services]

    return AppointmentResponse(
        id=new_appointment.id,
        medspa_id=new_appointment.medspa_id,
        start_time=new_appointment.start_time,
        status=new_appointment.status,
        services=services_data,
    )


@router.patch("/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(
    appointment_id: int, appointment_update: AppointmentUpdate, medspa_id: int = Depends(get_medspa_id)
):
    try:
        appointment = Appointment.get((Appointment.id == appointment_id) & (Appointment.medspa_id == medspa_id))
    except Appointment.DoesNotExist:
        raise HTTPException(status_code=404, detail="Appointment not found")

    # Update status
    appointment.status = appointment_update.status
    appointment.save()

    # Get services for response
    services = Service.select().join(AppointmentService).where(AppointmentService.appointment_id == appointment.id)
    services_data = [ServiceResponse.model_validate(service) for service in services]

    return AppointmentResponse(
        id=appointment.id,
        medspa_id=appointment.medspa_id,
        start_time=appointment.start_time,
        status=appointment.status,
        services=services_data,
    )


@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(appointment_id: int, medspa_id: int = Depends(get_medspa_id)):
    try:
        appointment = Appointment.get((Appointment.id == appointment_id) & (Appointment.medspa_id == medspa_id))
    except Appointment.DoesNotExist:
        raise HTTPException(status_code=404, detail="Appointment not found")

    # Get services for this appointment
    services = Service.select().join(AppointmentService).where(AppointmentService.appointment_id == appointment.id)
    services_data = [ServiceResponse.model_validate(service) for service in services]

    return AppointmentResponse(
        id=appointment.id,
        medspa_id=appointment.medspa_id,
        start_time=appointment.start_time,
        status=appointment.status,
        services=services_data,
    )


@router.get("/", response_model=List[AppointmentResponse])
def get_all_appointments(medspa_id: int = Depends(get_medspa_id)):
    appointments = Appointment.select().where(Appointment.medspa_id == medspa_id).order_by(Appointment.start_time)

    result = []
    for appointment in appointments:
        # TODO: fix n+1
        services = Service.select().join(AppointmentService).where(AppointmentService.appointment_id == appointment.id)

        services_data = [ServiceResponse.model_validate(service) for service in services]

        result.append(
            AppointmentResponse(
                id=appointment.id,
                medspa_id=appointment.medspa_id,
                start_time=appointment.start_time,
                status=appointment.status,
                services=services_data,
            )
        )

    return result
