from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    student_id: str
    department: str
    year: int

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: UUID
    email: str
    full_name: str
    student_id: Optional[str] = None
    department: Optional[str] = None
    year: Optional[int] = None
    role: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse