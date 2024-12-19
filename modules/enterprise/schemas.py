from enum import Enum
from typing import Optional
from ninja import Schema, Field
from datetime import datetime
from pydantic import EmailStr, HttpUrl

# Enum para filtrar por estado de investimento
class InvestedFilterEnum(str, Enum):
    yes = "yes"
    no = "no"

# Schema para criação (POST)
class EnterprisePostSchema(Schema):
    name: str
    problem: str
    solution: str
    value_proposition: str
    differential: str
    competitors: str
    product: str
    description: str
    mail: Optional[EmailStr] = None
    linkedin: Optional[HttpUrl] = None
    name_foment: Optional[str] = None
    programm: Optional[str] = None
    invested: Optional[bool] = False
    boosting: Optional[bool] = False
    value_invested: Optional[float] = None
    value_foment: Optional[float] = None

# Schema para atualização (PUT)
class EnterprisePutSchema(Schema):
    name: Optional[str] = Field(None, alias="name", title="Nome da empresa")
    problem: Optional[str] = Field(None, alias="problem", title="Problema identificado")
    solution: Optional[str] = Field(None, alias="solution", title="Solução proposta")
    value_proposition: Optional[str] = Field(None, alias="value_proposition", title="Proposta de valor")
    differential: Optional[str] = Field(None, alias="differential", title="Diferencial")
    competitors: Optional[str] = Field(None, alias="competitors", title="Concorrentes")
    product: Optional[str] = Field(None, alias="product", title="Produto ou serviço")
    description: Optional[str] = Field(None, alias="description", title="Descrição")
    mail: Optional[EmailStr] = Field(None, alias="mail", title="Email")
    linkedin: Optional[HttpUrl] = Field(None, alias="linkedin", title="LinkedIn")
    name_foment: Optional[str] = Field(None, alias="name_foment", title="Nome do fomentador")
    programm: Optional[str] = Field(None, alias="programm", title="Programa associado")
    invested: Optional[bool] = Field(None, alias="invested", title="Investida")
    boosting: Optional[bool] = Field(None, alias="boosting", title="Acelerada")
    value_invested: Optional[float] = Field(None, alias="value_invested", title="Valor investido")
    value_foment: Optional[float] = Field(None, alias="value_foment", title="Valor de fomento")

# Schema para listagem (GET)
class EnterpriseListSchema(Schema):
    enterprise_id: int
    name: str
    value_proposition: str
    invested: bool
    boosting: bool
    value_invested: Optional[float] = None
    value_foment: Optional[float] = None

# Schema de resposta para erros
class ErrorResponse(Schema):
    message: str
