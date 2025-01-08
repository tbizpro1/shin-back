from enum import Enum
from typing import Optional
from ninja import Schema, Field
from datetime import datetime
import uuid

class RoleEnum(str, Enum):
    owner = "owner"
    partner = "partner"

class StatusEnum(str, Enum):
    pending = "pending"
    accepted = "accepted"
    declined = "declined"

class UserEnterprisePostSchema(Schema):
    user_id: int = Field(..., alias="user_id", title="ID do usuário")
    enterprise_id: int = Field(..., alias="enterprise_id", title="ID da empresa")
    role: RoleEnum = Field(..., alias="role", title="Papel do usuário na empresa")

class UserEnterprisePutSchema(Schema):
    user_id: Optional[int] = Field(None, alias="user_id", title="ID do usuário")
    enterprise_id: Optional[int] = Field(None, alias="enterprise_id", title="ID da empresa")
    role: Optional[RoleEnum] = Field(None, alias="role", title="Papel do usuário na empresa")
    status: Optional[StatusEnum] = Field(None, alias="status", title="Status do convite")
    
    send_at: Optional[datetime] = None  
    accept_at: Optional[datetime] = None  

class UserEnterpriseListSchema(Schema):
    ue_id: int = Field(..., alias="ue_id", title="ID da relação")
    user_id: int = Field(..., alias="user_id", title="ID do usuário")
    username: str = Field(..., alias="username", title="Nome do usuário")
    enterprise_id: int = Field(..., alias="enterprise_id", title="ID da empresa")
    enterprise_name: str = Field(..., alias="enterprise_name", title="Nome da empresa")
    role: str = Field(..., alias="role", title="Papel do usuário na empresa")
    status: str = Field(..., alias="status", title="Status do convite")
    send_at: Optional[datetime] = Field(None, alias="send_at", title="Data e hora do envio do convite")
    accept_at: Optional[datetime] = Field(None, alias="accept_at", title="Data e hora do aceite do convite")
    token: uuid.UUID = Field(..., alias="token", title="Token único")


class ErrorResponse(Schema):
    message: str
