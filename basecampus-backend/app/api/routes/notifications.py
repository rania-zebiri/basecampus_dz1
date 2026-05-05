from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.database import get_supabase_admin
from app.core.security import decode_token
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

router = APIRouter(prefix="/notifications", tags=["Notifications"])
security = HTTPBearer()

# ── Schema ────────────────────────────────────────────
class NotificationResponse(BaseModel):
    id: UUID
    title: str
    message: str
    type: str
    is_read: bool
    created_at: datetime

# ── Helper: verify token ──────────────────────────────
def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security)
):
    payload = decode_token(credentials.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    return payload

# ── GET all notifications ─────────────────────────────
@router.get("/", response_model=list[NotificationResponse])
async def get_notifications(
        user=Depends(get_current_user)
):
    db = get_supabase_admin()
    result = db.table("notifications").select("*").order(
        "created_at", desc=True
    ).execute()
    return result.data

# ── Mark as read ──────────────────────────────────────
@router.put("/{notification_id}/read")
async def mark_as_read(
        notification_id: str,
        user=Depends(get_current_user)
):
    db = get_supabase_admin()
    result = db.table("notifications").update(
        {"is_read": True}
    ).eq("id", notification_id).execute()

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    return {"message": "Notification marked as read"}

# ── Mark all as read ──────────────────────────────────
@router.put("/read-all")
async def mark_all_as_read(
        user=Depends(get_current_user)
):
    db = get_supabase_admin()
    db.table("notifications").update(
        {"is_read": True}
    ).eq("is_read", False).execute()
    return {"message": "All notifications marked as read"}