from pydantic import BaseModel
from decimal import Decimal
from typing import Optional


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
