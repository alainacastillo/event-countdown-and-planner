from fastapi import APIRouter

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/popular-events")
def get_popular_events():
    return {"message": "Most viewed countdown timers"}

@router.get("/event/{eventId}")
def get_event_statistics(eventId: int):
    return {"message": f"Engagement statistics for event {eventId}"}

@router.get("/user/{userId}")
def get_user_statistics(userId: int):
    return {"message": f"Countdown usage statistics for user {userId}"}
