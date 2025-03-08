from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel

router = APIRouter(prefix="/countdown", tags=["Countdown"])

# Mock database
events = {1: {"remaining_time": "2 days 5 hours", "status": "active"}}

# Pydantic model for customization
class CountdownSettings(BaseModel):
    theme: str
    font: str

@router.get("/{eventId}")
async def get_countdown(eventId: int = Path(..., gt=0)):
    if eventId not in events:
        raise HTTPException(status_code=404, detail="Event not found")
    return events[eventId]

@router.get("/{eventId}/progress")
async def get_countdown_progress(eventId: int):
    if eventId not in events:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"eventId": eventId, "progress": "75%"}

@router.get("/{eventId}/timezone/{timezone}")
async def get_countdown_with_timezone(eventId: int, timezone: str):
    if eventId not in events:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"eventId": eventId, "adjusted_time": f"Event time in {timezone}"}

@router.post("/pause/{eventId}")
async def pause_countdown(eventId: int):
    if eventId not in events:
        raise HTTPException(status_code=404, detail="Event not found")
    events[eventId]["status"] = "paused"
    return {"eventId": eventId, "status": "paused"}

@router.post("/resume/{eventId}")
async def resume_countdown(eventId: int):
    if eventId not in events:
        raise HTTPException(status_code=404, detail="Event not found")
    events[eventId]["status"] = "active"
    return {"eventId": eventId, "status": "resumed"}

@router.post("/sync/{eventId}")
async def sync_countdown(eventId: int):
    return {"eventId": eventId, "sync_status": "synced"}

@router.get("/share/{eventId}")
async def share_countdown(eventId: int):
    return {"eventId": eventId, "shareable_link": f"http://example.com/countdown/{eventId}"}

@router.get("/embed/{eventId}")
async def embed_countdown(eventId: int):
    return {"eventId": eventId, "embed_code": f"<iframe src='http://example.com/countdown/{eventId}'></iframe>"}

@router.get("/status/{eventId}")
async def countdown_status(eventId: int):
    if eventId not in events:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"eventId": eventId, "status": events[eventId]["status"]}

@router.post("/customize/{eventId}")
async def customize_countdown(eventId: int, settings: CountdownSettings):
    if eventId not in events:
        raise HTTPException(status_code=404, detail="Event not found")
    events[eventId]["customization"] = settings.dict()
    return {"eventId": eventId, "customization": "updated"}

@router.get("/customizations/{eventId}")
async def get_customizations(eventId: int):
    if eventId not in events:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"eventId": eventId, "theme": "dark"}

@router.post("/sound/{eventId}")
async def set_alert_sound(eventId: int):
    return {"eventId": eventId, "alert_sound": "set"}

@router.post("/smart-pause/{eventId}")
async def smart_pause_countdown(eventId: int):
    return {"eventId": eventId, "smart_pause": "activated"}
