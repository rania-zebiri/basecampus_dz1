from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.database import get_supabase_admin
from app.core.security import decode_token
from pydantic import BaseModel
from typing import Optional
from uuid import UUID

router = APIRouter(prefix="/timetable", tags=["Timetable"])
security = HTTPBearer()

# ── Schema ────────────────────────────────────────────
class TimetableResponse(BaseModel):
    id: UUID
    subject: str
    subject_code: str
    type: str
    location: str
    day: str
    start_time: str
    end_time: str

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

# ── GET all timetable ─────────────────────────────────
@router.get("/", response_model=list[TimetableResponse])
async def get_timetable(
        day: Optional[str] = None,
        user=Depends(get_current_user)
):
    db = get_supabase_admin()

    query = db.table("timetable").select("*").order(
        "start_time", desc=False
    )

    if day:
        query = query.eq("day", day)

    result = query.execute()
    return result.data

# ── GET today's timetable ─────────────────────────────
@router.get("/today", response_model=list[TimetableResponse])
async def get_today_timetable(
        user=Depends(get_current_user)
):
    from datetime import datetime
    db = get_supabase_admin()

    # Get today's day name
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    today = days[datetime.now().weekday()]

    result = db.table("timetable").select("*").eq(
        "day", today
    ).order("start_time", desc=False).execute()

    return result.data