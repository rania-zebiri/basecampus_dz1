from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    UserResponse,
)
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_token,
)
from app.core.database import get_supabase_admin

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()

# ── Register ──────────────────────────────────────────
@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(data: RegisterRequest):
    db = get_supabase_admin()

    # Check if email exists
    existing = db.table("users").select("id").eq(
        "email", data.email
    ).execute()

    if existing.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Check if student_id exists
    existing_id = db.table("users").select("id").eq(
        "student_id", data.student_id
    ).execute()

    if existing_id.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student ID already registered"
        )

    # Hash password and insert user
    hashed = hash_password(data.password)
    result = db.table("users").insert({
        "email": data.email,
        "password_hash": hashed,
        "full_name": data.full_name,
        "student_id": data.student_id,
        "department": data.department,
        "year": data.year,
        "role": "student",
    }).execute()

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )

    user = result.data[0]
    token = create_access_token({"sub": user["id"], "role": user["role"]})

    return TokenResponse(
        access_token=token,
        user=UserResponse(**user)
    )

# ── Login ─────────────────────────────────────────────
@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest):
    db = get_supabase_admin()

    # Find user
    result = db.table("users").select("*").eq(
        "email", data.email
    ).execute()

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    user = result.data[0]

    # Verify password
    if not verify_password(data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Check active
    if not user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated"
        )

    token = create_access_token({"sub": user["id"], "role": user["role"]})

    return TokenResponse(
        access_token=token,
        user=UserResponse(**user)
    )

# ── Get current user ──────────────────────────────────
@router.get("/me", response_model=UserResponse)
async def get_me(
        credentials: HTTPAuthorizationCredentials = Depends(security)
):
    payload = decode_token(credentials.credentials)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    db = get_supabase_admin()
    result = db.table("users").select("*").eq(
        "id", payload["sub"]
    ).execute()

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserResponse(**result.data[0])