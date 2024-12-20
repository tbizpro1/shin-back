from enum import Enum
from typing import Optional
from ninja import Schema, Field

# Enum para o campo `role`
class RoleEnum(str, Enum):
    owner = "owner"
    partner = "partner"

# Schema para criação (POST)
class UserEnterprisePostSchema(Schema):
    user_id: int = Field(..., alias="user_id", title="ID do usuário")
    enterprise_id: int = Field(..., alias="enterprise_id", title="ID da empresa")
    role: RoleEnum = Field(..., alias="role", title="Papel do usuário na empresa")

# Schema para atualização (PUT)
class UserEnterprisePutSchema(Schema):
    user_id: Optional[int] = Field(None, alias="user_id", title="ID do usuário")
    enterprise_id: Optional[int] = Field(None, alias="enterprise_id", title="ID da empresa")
    role: Optional[RoleEnum] = Field(None, alias="role", title="Papel do usuário na empresa")

# Schema para listagem (GET)
class UserEnterpriseListSchema(Schema):
    ue_id: int = Field(..., alias="ue_id", title="ID da relação")
    user_id: int = Field(..., alias="user_id", title="ID do usuário")
    username: str = Field(..., alias="username", title="Nome do usuário")
    enterprise_id: int = Field(..., alias="enterprise_id", title="ID da empresa")
    enterprise_name: str = Field(..., alias="enterprise_name", title="Nome da empresa")
    role: str = Field(..., alias="role", title="Papel do usuário na empresa")

# Schema de resposta para erros
class ErrorResponse(Schema):
    message: str
