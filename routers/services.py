from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models import Service
from schemas import ServiceCreate, ServiceUpdate, ServiceResponse
from dependencies import get_medspa_id

router = APIRouter(prefix="/services", tags=["services"])


@router.post("/", response_model=ServiceResponse)
def create_service(service: ServiceCreate, medspa_id: int = Depends(get_medspa_id)):
    try:
        new_service = Service.create(
            medspa_id=medspa_id,
            name=service.name,
            description=service.description,
            price=service.price,
            duration_minutes=service.duration_minutes,
        )
        return ServiceResponse.model_validate(new_service)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{service_id}", response_model=ServiceResponse)
def update_service(service_id: int, service_update: ServiceUpdate, medspa_id: int = Depends(get_medspa_id)):
    try:
        service = Service.get((Service.id == service_id) & (Service.medspa_id == medspa_id))

        update_data = service_update.model_dump(exclude_unset=True)
        if update_data:
            Service.update(**update_data).where((Service.id == service_id) & (Service.medspa_id == medspa_id)).execute()
            service = Service.get((Service.id == service_id) & (Service.medspa_id == medspa_id))

        return ServiceResponse.model_validate(service)
    except Service.DoesNotExist:
        raise HTTPException(status_code=404, detail="Service not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{service_id}", response_model=ServiceResponse)
def get_service(service_id: int, medspa_id: int = Depends(get_medspa_id)):
    try:
        service = Service.get((Service.id == service_id) & (Service.medspa_id == medspa_id))
        return ServiceResponse.model_validate(service)
    except Service.DoesNotExist:
        raise HTTPException(status_code=404, detail="Service not found")


@router.get("/", response_model=List[ServiceResponse])
def get_all_services(medspa_id: int = Depends(get_medspa_id)):
    services = Service.select().where(Service.medspa_id == medspa_id)
    return [ServiceResponse.model_validate(service) for service in services]
