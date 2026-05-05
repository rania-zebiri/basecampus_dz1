from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.database import get_supabase_admin
from app.core.security import decode_token
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

router = APIRouter(prefix="/announcements", tags=["Announcements"])
security = HTTPBearer()

# ── Schemas ───────────────────────────────────────────
class AnnouncementResponse(BaseModel):
    id: UUID
    title: str
    description: str
    category: str
    author: str
    created_at: datetime
    updated_at: datetime

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

# ── GET all announcements ─────────────────────────────
@router.get("/", response_model=list[AnnouncementResponse])
async def get_announcements(
        category: Optional[str] = None,
        user=Depends(get_current_user)
):
    db = get_supabase_admin()

    query = db.table("announcements").select("*").order(
        "created_at", desc=True
    )

    if category and category != "All":
        query = query.eq("category", category)

    result = query.execute()

    return result.data

# ── GET single announcement ───────────────────────────
@router.get("/{announcement_id}", response_model=AnnouncementResponse)
async def get_announcement(
        announcement_id: str,
        user=Depends(get_current_user)
):
    db = get_supabase_admin()

    result = db.table("announcements").select("*").eq(
        "id", announcement_id
    ).execute()

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Announcement not found"
        )

    return result.data[0]

# ── Create announcement (for testing) ────────────────
class AnnouncementCreate(BaseModel):
    title: str
    description: str
    category: str
    author: str

@router.post("/", response_model=AnnouncementResponse, status_code=201)
async def create_announcement(
        data: AnnouncementCreate,
        user=Depends(get_current_user)
):
    db = get_supabase_admin()

    result = db.table("announcements").insert({
        "title":       data.title,
        "description": data.description,
        "category":    data.category,
        "author":      data.author,
    }).execute()

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create announcement"
        )

    return result.data[0]

# ── Delete announcement ───────────────────────────────
@router.delete("/{announcement_id}", status_code=204)
async def delete_announcement(
        announcement_id: str,
        user=Depends(get_current_user)
):
    db = get_supabase_admin()

    result = db.table("announcements").delete().eq(
        "id", announcement_id
    ).execute()

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Announcement not found"
        )

# ── Update announcement ───────────────────────────────
class AnnouncementUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    author: Optional[str] = None

@router.put("/{announcement_id}", response_model=AnnouncementResponse)
async def update_announcement(
        announcement_id: str,
        data: AnnouncementUpdate,
        user=Depends(get_current_user)
):
    db = get_supabase_admin()

    # Only update provided fields
    update_data = {k: v for k, v in data.dict().items() if v is not None}

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )

    result = db.table("announcements").update(update_data).eq(
        "id", announcement_id
    ).execute()

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Announcement not found"
        )

    return result.data[0]