from fastapi import Header, HTTPException
from models import Medspa


async def get_medspa_id(x_medspa_id: int = Header(alias="X-Medspa-ID")):
    """Extract and validate medspa_id from X-Medspa-ID header"""
    try:
        # Verify the medspa exists
        Medspa.get_by_id(x_medspa_id)
        return x_medspa_id
    except Medspa.DoesNotExist:
        raise HTTPException(status_code=404, detail="Medspa not found")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid medspa ID")
