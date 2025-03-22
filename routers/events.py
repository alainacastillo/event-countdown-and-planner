from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel
from typing import Dict

router = APIRouter(prefix="/events", tags=["Events"])

events_db: Dict[int, Dict] = {}
event_counter = 1

class Event(BaseModel):
    name: str
    date: str  
    description: str

@router.post("/")
async def create_event(event: Event):
    global event_counter
    event_id = event_counter
    events_db[event_id] = event.dict()
    event_counter += 1
    return {"eventId": event_id, "message": "Event created successfully"}

@router.put("/{eventId}")
async def edit_event(eventId: int, event: Event):
    if eventId not in events_db:
        raise HTTPException(status_code=404, detail="Event not found")
    
    events_db[eventId] = event.dict()
    return {"eventId": eventId, "message": "Event updated successfully"}

@router.delete("/{eventId}")
async def delete_event(eventId: int):
    if eventId not in events_db:
        raise HTTPException(status_code=404, detail="Event not found")
    
    del events_db[eventId]
    return {"eventId": eventId, "message": "Event deleted successfully"}
