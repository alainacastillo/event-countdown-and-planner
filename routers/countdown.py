from fastapi import APIRouter
from datetime import datetime, timedelta

router = APIRouter(prefix="/countdown", tags=["Countdown"])

events = {
    1: {"name": "New Year", "start_time": datetime(2025, 1, 1, 0, 0), "paused": False},
    2: {"name": "Conference", "start_time": datetime(2025, 5, 20, 10, 0), "paused": False},
}

@router.get("/{eventId}")
def get_remaining_time(eventId: int):
    event = events.get(eventId)
    if not event:
        return {"error": "Event not found"}
    remaining = event["start_time"] - datetime.now()
    return {"event": event["name"], "remaining_time": str(remaining)}

@router.post("/pause/{eventId}")
def pause_countdown(eventId: int):
    if eventId in events:
        events[eventId]["paused"] = True
        return {"message": "Countdown paused"}
    return {"error": "Event not found"}

@router.post("/resume/{eventId}")
def resume_countdown(eventId: int):
    if eventId in events:
        events[eventId]["paused"] = False
        return {"message": "Countdown resumed"}
    return {"error": "Event not found"}
