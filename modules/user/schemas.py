from enum import Enum
from typing import Optional
from ninja import Schema, UploadedFile, Field
from datetime import datetime


class RoleFilterEnum(str, Enum):
    admin = "admin"
    user = "user"

class UserPostSchema(Schema):
    username: str
    email: str
    password: str
    role: RoleFilterEnum
    
class UserPutSchema(Schema):
    username: str = Field(None, alias="username", required=False, title="Nome de usuário")
    email: str = Field(None, alias="email", required=False, title="Email")
    password: str = Field(None, alias="password", required=False, title="Senha")
    role: RoleFilterEnum = None
    
class UserListSchema(Schema):
    id: int
    username: str
    email: str
    phone: str
    linkedin: str
    profession: str
    role: str
    profile_picture: Optional[str] = None
    date_joined: datetime
    last_login: datetime
    is_active: bool
    
    
class ErrorResponse(Schema):
    message: str

class RegisterSchema(Schema):
    username: str
    email: str
    password: str
    role: RoleFilterEnum

class RegisterResponseSchema(Schema):
    id: int
    username: str
    email: str