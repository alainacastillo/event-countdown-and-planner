from fastapi import APIRouter

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/popular-events")
async def get_popular_events():
    return {"popular_events": ["Event 1", "Event 2", "Event 3"]}

@router.get("/event/{eventId}")
async def event_analytics(eventId: int):
    return {"eventId": eventId, "views": 100, "shares": 10}

@router.get("/user/{userId}")
async def user_analytics(userId: int):
    return {"userId": userId, "events_created": 5, "events_joined": 10}
