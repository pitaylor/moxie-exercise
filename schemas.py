from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional, List, Literal
from datetime import datetime

AppointmentStatusLiteral = Literal["scheduled", "completed", "canceled"]


class ServiceCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal = Field(ge=0)
    duration: int = Field(ge=0)


class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, ge=0)
    duration: Optional[int] = Field(None, ge=0)


class ServiceResponse(BaseModel):
    id: int
    medspa_id: int
    name: str
    description: Optional[str]
    price: Decimal
    duration: int

    @classmethod
    def from_model(cls, service):
        return cls(
            id=service.id,
            medspa_id=service.medspa_id,
            name=service.name,
            description=service.description,
            price=service.price,
            duration=service.duration,
        )


class AppointmentCreate(BaseModel):
    start_time: datetime
    service_ids: List[int]
    status: Optional[AppointmentStatusLiteral] = "scheduled"


class AppointmentUpdate(BaseModel):
    status: AppointmentStatusLiteral


class AppointmentResponse(BaseModel):
    id: int
    medspa_id: int
    start_time: datetime
    status: str
    services: List[ServiceResponse]
    total_duration: int
    total_price: Decimal

    @classmethod
    def from_model(cls, appointment):
        services_data = [ServiceResponse.from_model(service) for service in appointment.services]
        return cls(
            id=appointment.id,
            medspa_id=appointment.medspa_id,
            start_time=appointment.start_time,
            status=appointment.status,
            services=services_data,
            total_duration=appointment.total_duration,
            total_price=appointment.total_price,
        )
