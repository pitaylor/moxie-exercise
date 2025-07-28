from pydantic import BaseModel
from decimal import Decimal
from typing import Optional, List, Literal
from datetime import datetime

AppointmentStatusLiteral = Literal["scheduled", "completed", "canceled"]


class ServiceCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal
    duration_minutes: int


class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    duration_minutes: Optional[int] = None


class ServiceResponse(BaseModel):
    id: int
    medspa_id: int
    name: str
    description: Optional[str]
    price: Decimal
    duration_minutes: int

    class Config:
        from_attributes = True


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

    class Config:
        from_attributes = True
