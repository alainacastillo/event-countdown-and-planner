from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
from pydantic import BaseModel
from pytz import timezone, all_timezones

router = APIRouter(prefix="/countdown", tags=["Countdown"])

events = {
    1: {"start_time": datetime(2025, 3, 1, 12, 0, 0), "end_time": datetime(2025, 3, 2, 12, 0, 0)}
}

event_statuses = {
    1: "active",
    2: "paused",
    3: "completed"  
}

class SmartPauseRequest(BaseModel):
    condition: str

class Customization(BaseModel):
    theme: str
    colors: dict
    font: str

class SoundRequest(BaseModel):
    sound_url: str

event_customizations = {
    1: {"theme": "dark", "colors": {"background": "#000000", "text": "#FFFFFF"}, "font": "Arial"}
}

event_sounds = {}

@router.get("/{eventId}/progress")
def get_event_progress(eventId: int):
    if eventId not in events:
        raise HTTPException(status_code=404, detail="Event not found")

    event = events[eventId]
    now = datetime.now()
    start_time = event["start_time"]
    end_time = event["end_time"]

    if now < start_time:
        return {"message": "Event has not started yet"}
    elif now > end_time:
        return {"message": "Event has ended"}

    elapsed_time = now - start_time
    total_duration = end_time - start_time
    progress_percentage = (elapsed_time.total_seconds() / total_duration.total_seconds()) * 100

    return {"eventId": eventId, "progress": f"{progress_percentage:.2f}%"}

@router.get("/{eventId}/timezone/{tz}")
async def get_event_time_in_timezone(eventId: int, tz: str):
    """Returns the event start time adjusted for a specific timezone."""
    if eventId not in events:
        raise HTTPException(status_code=404, detail="Event not found")

    # Validate timezone
    if tz not in all_timezones:
        raise HTTPException(status_code=400, detail="Invalid timezone")

    event = events[eventId]
    event_time = event["start_time"]
    
    # Convert to the requested timezone
    tz_obj = timezone(tz)
    localized_time = event_time.astimezone(tz_obj)

    return {"eventId": eventId, "timezone": tz, "localized_time": localized_time.isoformat()}

@router.post("/sync/{eventId}")
async def sync_countdown(eventId: int):
    return {"message": f"Countdown {eventId} synchronized successfully"}

@router.get("/share/{eventId}")
async def share_countdown(eventId: int):
    shareable_link = f"http://127.0.0.1:8000/countdown/view/{eventId}"
    return {"message": "Shareable link generated", "link": shareable_link}

@router.get("/embed/{eventId}")
async def embed_countdown(eventId: int):
    embed_code = f'<iframe src="http://127.0.0.1:8000/countdown/view/{eventId}" width="600" height="400"></iframe>'
    return {"message": "Embed code generated", "embed_code": embed_code}

@router.get("/status/{eventId}")
async def get_countdown_status(eventId: int):
    status = event_statuses.get(eventId, "not found")
    if status == "not found":
        return {"error": "Event not found"}
    return {"eventId": eventId, "status": status}

@router.post("/customize/{eventId}")
async def customize_countdown(eventId: int, customization: Customization):
    event_customizations[eventId] = customization.dict()
    return {"eventId": eventId, "customization": event_customizations[eventId]}

@router.get("/customizations/{eventId}")
async def get_customizations(eventId: int):
    if eventId not in event_customizations:
        raise HTTPException(status_code=404, detail="Customization not found")
    return {"eventId": eventId, "customization": event_customizations[eventId]}

@router.post("/sound/{eventId}")
async def set_event_sound(eventId: int, request: SoundRequest):
    event_sounds[eventId] = request.sound_url
    return {"message": "Sound set successfully", "eventId": eventId, "sound_url": request.sound_url}

@router.get("/sound/{eventId}")
async def get_event_sound(eventId: int):
    if eventId not in event_sounds:
        raise HTTPException(status_code=404, detail="No sound set for this event.")
    return {"eventId": eventId, "sound_url": event_sounds[eventId]}

@router.post("/smart-pause/{eventId}")
async def smart_pause_event(eventId: int, request: SmartPauseRequest):
    if eventId not in event_statuses:
        raise HTTPException(status_code=404, detail="Event not found")
    
    if request.condition == "user_inactive":
        event_statuses[eventId] = "paused"
        return {"message": "Event paused due to user inactivity", "eventId": eventId}
    
    return {"message": "Condition not met for smart pause", "eventId": eventId}
