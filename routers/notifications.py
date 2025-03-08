from fastapi import APIRouter, HTTPException, Path
from typing import Dict

router = APIRouter(prefix="/notifications", tags=["Notifications"])

subscriptions: Dict[int, bool] = {}

@router.post("/subscribe/{eventId}")
async def subscribe_to_notifications(eventId: int = Path(..., title="Event ID")):
    """Subscribe to event countdown notifications"""
    if eventId in subscriptions:
        raise HTTPException(status_code=400, detail="Already subscribed")

    subscriptions[eventId] = True
    return {"eventId": eventId, "message": "Subscribed to event notifications"}

@router.post("/subscribe/{eventId}")
async def subscribe_notifications(eventId: int):
    return {"eventId": eventId, "subscription": "successful"}

@router.delete("/unsubscribe/{eventId}")
async def unsubscribe_notifications(eventId: int):
    return {"eventId": eventId, "subscription": "canceled"}

@router.post("/test/{eventId}")
async def test_notification(eventId: int):
    return {"eventId": eventId, "notification": "sent"}

@router.get("/history/{eventId}")
async def notification_history(eventId: int):
    return {"eventId": eventId, "history": ["Notified 1 day ago", "Notified 2 hours ago"]}
