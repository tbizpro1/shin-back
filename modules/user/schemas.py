from enum import Enum
from typing import Optional
from ninja import Schema, Field
from datetime import datetime


class RoleFilterEnum(str, Enum):
    admin = "admin"
    user = "user"


class UserPostSchema(Schema):
    username: str
    email: str
    password: str
    phone: str  
    linkedin: Optional[str] 
    profession: Optional[str]  
    role: RoleFilterEnum


# Schema para PUT (atualização de usuário)
class UserPutSchema(Schema):
    username: Optional[str] = Field(None, alias="username", title="Nome de usuário")
    email: Optional[str] = Field(None, alias="email", title="Email")
    password: Optional[str] = Field(None, alias="password", title="Senha")
    phone: Optional[str] = Field(None, alias="phone", title="Telefone")  
    linkedin: Optional[str] = Field(None, alias="linkedin", title="LinkedIn")  
    profession: Optional[str] = Field(None, alias="profession", title="Profissão")  
    role: Optional[RoleFilterEnum] = None


class UserListSchema(Schema):
    id: int
    username: str
    email: str
    phone: Optional[str] = None  
    linkedin: Optional[str] = None  
    profession: Optional[str] = None  
    role: str
    profile_picture: Optional[str] = None
    date_joined: datetime
    last_login: datetime
    is_active: bool


# Schema de resposta para registro
class RegisterSchema(Schema):
    username: str
    email: str
    password: str
    phone: str  
    linkedin: Optional[str]  
    profession: Optional[str]  
    role: RoleFilterEnum


class RegisterResponseSchema(Schema):
    id: int
    username: str
    email: str
    phone: Optional[str] = None  
    linkedin: Optional[str] = None  
    profession: Optional[str] = None  

class ErrorResponse(Schema):
    message: str