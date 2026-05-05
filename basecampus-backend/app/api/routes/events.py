from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.database import get_supabase_admin
from app.core.security import decode_token
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

router = APIRouter(prefix="/events", tags=["Events"])
security = HTTPBearer()

# ── Schemas ───────────────────────────────────────────
class EventResponse(BaseModel):
    id: UUID
    title: str
    location: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    attendees_count: int
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class EventCreate(BaseModel):
    title: str
    location: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    attendees_count: Optional[int] = 0
    image_url: Optional[str] = None

class EventUpdate(BaseModel):
    title: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    attendees_count: Optional[int] = None
    image_url: Optional[str] = None

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

# ── GET all events ────────────────────────────────────
@router.get("/", response_model=list[EventResponse])
async def get_events(
        date: Optional[str] = None,
        user=Depends(get_current_user)
):
    db = get_supabase_admin()

    query = db.table("events").select("*").order(
        "start_time", desc=False
    )

    if date:
        # Filter by date (YYYY-MM-DD)
        query = query.gte("start_time", f"{date}T00:00:00") \
            .lte("start_time", f"{date}T23:59:59")

    result = query.execute()
    return result.data

# ── GET single event ──────────────────────────────────
@router.get("/{event_id}", response_model=EventResponse)
async def get_event(
        event_id: str,
        user=Depends(get_current_user)
):
    db = get_supabase_admin()

    result = db.table("events").select("*").eq(
        "id", event_id
    ).execute()

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    return result.data[0]

# ── CREATE event ──────────────────────────────────────
@router.post("/", response_model=EventResponse, status_code=201)
async def create_event(
        data: EventCreate,
        user=Depends(get_current_user)
):
    db = get_supabase_admin()

    result = db.table("events").insert({
        "title":           data.title,
        "location":        data.location,
        "description":     data.description,
        "start_time":      data.start_time.isoformat(),
        "end_time":        data.end_time.isoformat(),
        "attendees_count": data.attendees_count,
        "image_url":       data.image_url,
    }).execute()

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create event"
        )

    return result.data[0]

# ── UPDATE event ──────────────────────────────────────
@router.put("/{event_id}", response_model=EventResponse)
async def update_event(
        event_id: str,
        data: EventUpdate,
        user=Depends(get_current_user)
):
    db = get_supabase_admin()

    update_data = {k: v for k, v in data.dict().items() if v is not None}

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )

    result = db.table("events").update(update_data).eq(
        "id", event_id
    ).execute()

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    return result.data[0]

# ── DELETE event ──────────────────────────────────────
@router.delete("/{event_id}", status_code=204)
async def delete_event(
        event_id: str,
        user=Depends(get_current_user)
):
    db = get_supabase_admin()

    result = db.table("events").delete().eq(
        "id", event_id
    ).execute()

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )