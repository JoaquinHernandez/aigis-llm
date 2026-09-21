from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from pydantic import BaseModel
from app.db.session import get_db
from app.db.models import Alert
from datetime import datetime

router = APIRouter(prefix="/v1/alerts", tags=["Alert Queue"])

class AlertResponse(BaseModel):
    id: str
    source: str
    severity: str
    raw_log: dict
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

@router.get("/", response_model=List[AlertResponse])
async def get_open_alerts(db: AsyncSession = Depends(get_db)):
    """Fetch the latest open alerts for the Triage Console."""
    result = await db.execute(
        select(Alert).where(Alert.status == "Open").order_by(Alert.created_at.desc()).limit(50)
    )
    alerts = result.scalars().all()
    
    # Convert UUIDs to strings for JSON serialization
    return [
        AlertResponse(
            id=str(a.id),
            source=a.source,
            severity=a.severity,
            raw_log=a.raw_log,
            status=a.status,
            created_at=a.created_at
        ) for a in alerts
    ]
