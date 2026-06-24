
import hmac
import hashlib
from fastapi import APIRouter, Request, HTTPException, Depends
from app.core.config import get_settings

settings = get_settings()
router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


@router.post("/{crm_type}")
async def receive_webhook(crm_type: str, request: Request):
    body = await request.body()
    signature = request.headers.get("X-Webhook-Signature", "")
    expected = hmac.new(
        settings.JWT_SECRET.encode(), body, hashlib.sha256
    ).hexdigest()
    if not hmac.compare_digest(f"sha256={expected}", signature):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")
    payload = await request.json()
    return {"status": "received", "crm": crm_type, "event_type": payload.get("event")}
