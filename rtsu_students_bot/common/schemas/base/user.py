from .base_model import BaseModel


class UserRole(BaseModel):
    USER = "USER"
    ADMIN = "ADMIN"
    CREATOR = "CREATOR"


class User(BaseModel):
    telegram_id: int
    role: UserRole
