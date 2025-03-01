from fastapi import APIRouter

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.post("/subscribe/{eventId}")
def subscribe_notifications(eventId: int):
    return {"message": f"Subscribed to notifications for event {eventId}"}

@router.delete("/unsubscribe/{eventId}")
def unsubscribe_notifications(eventId: int):
    return {"message": f"Unsubscribed from notifications for event {eventId}"}

@router.post("/test/{eventId}")
def send_test_notification(eventId: int):
    return {"message": f"Test notification sent for event {eventId}"}

@router.get("/history/{eventId}")
def get_notification_history(eventId: int):
    return {"message": f"Notification history for event {eventId}"}
