# from enum import Enum
# from typing import Optional
# from ninja import Schema, Field
# from datetime import datetime
# from pydantic import validator
# from datetime import datetime, date

# from ..utils.validator_cpf import validar_cpf
# class RoleFilterEnum(str, Enum):
#     user = "user"

# class StateEnum(str, Enum):
#     AC = "AC"
#     AL = "AL"
#     AP = "AP"
#     AM = "AM"
#     BA = "BA"
#     CE = "CE"
#     DF = "DF"
#     ES = "ES"
#     GO = "GO"
#     MA = "MA"
#     MT = "MT"
#     MS = "MS"
#     MG = "MG"
#     PA = "PA"
#     PB = "PB"
#     PR = "PR"
#     PE = "PE"
#     PI = "PI"
#     RJ = "RJ"
#     RN = "RN"
#     RS = "RS"
#     RO = "RO"
#     RR = "RR"
#     SC = "SC"
#     SP = "SP"
#     SE = "SE"
#     TO = "TO"

# class EducationLevelEnum(str, Enum):
#     SEM_ESCOLARIDADE = "Sem escolaridade"
#     ENSINO_FUNDAMENTAL = "Ensino Fundamental"
#     ENSINO_MEDIO = "Ensino Médio"
#     GRADUACAO = "Graduação"
#     ESPECIALIZACAO = "Especialização"
#     MESTRADO = "Mestrado"
#     DOUTORADO = "Doutorado"
#     POS_DOUTORADO = "Pós-Doutorado"

# class GenderEnum(str, Enum):
#     m = "m"
#     f = "f"
#     n = "p"

# class EthnicityEnum(str, Enum):
#     BRANCA = "Branca"
#     PRETA = "Preta"
#     PARDA = "Parda"
#     AMARELA = "Amarela"
#     INDIGENA = "Indígena"


# class UserPostSchema(Schema):
#     username: str
#     email: str
#     password: str
#     phone: Optional[str] = None
#     linkedin: Optional[str] = None
#     profession: Optional[str] = None
#     role: RoleFilterEnum
#     state: StateEnum = None
#     gender: GenderEnum = None
#     institution: Optional[str] = None
#     education_level: EducationLevelEnum = None
#     ethnicity: EthnicityEnum = None
#     city: Optional[str] = None
#     whatsapp_number: Optional[str] = None
#     weekly_hours_worked: Optional[int] = None
#     date_of_birth: Optional[datetime] = None
#     country: Optional[str] = None
#     cep: Optional[str] = None
#     # street: Optional[str] = None
#     # neighborhood: Optional[str] = None
#     # number: Optional[str] = None
#     cpf: Optional[str] = None


#     @validator("cpf")
#     def validar_cpf(cls, cpf):
#         if not validar_cpf(cpf):
#             raise ValueError("CPF inválido")
#         return cpf


# class UserPutSchema(Schema):
#     username: Optional[str] = Field(None, alias="username", title="Nome de usuário")
#     email: Optional[str] = Field(None, alias="email", title="Email")
#     password: Optional[str] = Field(None, alias="password", title="Senha")
#     phone: Optional[str] = Field(None, alias="phone", title="Telefone")
#     linkedin: Optional[str] = Field(None, alias="linkedin", title="LinkedIn")
#     profession: Optional[str] = Field(None, alias="profession", title="Profissão")
#     role: Optional[RoleFilterEnum] = None
#     state: StateEnum = None
#     gender: Optional[GenderEnum] = None
#     institution: Optional[str] = None
#     education_level: Optional[EducationLevelEnum] = None
#     ethnicity: EthnicityEnum = None
#     city: Optional[str] = None
#     whatsapp_number: Optional[str] = None
#     weekly_hours_worked: Optional[int] = None
#     date_of_birth: Optional[datetime] = None
#     country: Optional[str] = None
#     cep: Optional[str] = None
#     # street: Optional[str] = None
#     # neighborhood: Optional[str] = None
#     # number: Optional[str] = None
#     cpf: Optional[str] = None


# class UserListSchema(Schema):
#     id: int
#     username: str
#     email: str
#     phone: Optional[str] = None
#     linkedin: Optional[str] = None
#     profession: Optional[str] = None
#     role: str
#     profile_picture: Optional[str] = None
#     state: StateEnum = None
#     gender: Optional[GenderEnum] = None
#     institution: Optional[str] = None
#     education_level: Optional[EducationLevelEnum] = None
#     ethnicity: EthnicityEnum = None
#     city: Optional[str] = None
#     whatsapp_number: Optional[str] = None
#     weekly_hours_worked: Optional[int] = None
#     date_of_birth: Optional[datetime] = None
#     country: Optional[str] = None
#     date_joined: datetime
#     last_login: datetime
#     age: Optional[int] = None  
#     is_active: bool
#     cep: Optional[str] = None
#     # street: Optional[str] = None
#     # neighborhood: Optional[str] = None
#     # number: Optional[str] = None
#     cpf: Optional[str] = None

#     @validator("age", pre=True, always=True)
#     def calcular_idade(cls, _, values):
#         date_of_birth = values.get("date_of_birth")
#         if date_of_birth:
#             today = date.today()
#             return (
#                 today.year
#                 - date_of_birth.year
#                 - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
#             )
#         return None

# # Schema de resposta para registro
# class RegisterSchema(Schema):
#     username: str
#     email: str
#     password: str
#     phone: Optional[str] = None
#     linkedin: Optional[str] = None
#     profession: Optional[str] = None
#     role: RoleFilterEnum
#     state: StateEnum = None
#     gender: Optional[GenderEnum] = None
#     institution: Optional[str] = None
#     education_level: Optional[EducationLevelEnum] = None
#     ethnicity: EthnicityEnum = None
#     city: Optional[str] = None
#     whatsapp_number: Optional[str] = None
#     weekly_hours_worked: Optional[int] = None
#     date_of_birth: Optional[datetime] = None
#     country: Optional[str] = None
#     cep: Optional[str] = None
#     # street: Optional[str] = None
#     # neighborhood: Optional[str] = None
#     # number: Optional[str] = None
#     cpf: Optional[str] = None


# class RegisterResponseSchema(Schema):
#     id: int
#     username: str
#     email: str
#     phone: Optional[str] = None
#     linkedin: Optional[str] = None
#     profession: Optional[str] = None
#     state: StateEnum = None
#     gender: Optional[GenderEnum] = None
#     institution: Optional[str] = None
#     education_level: Optional[EducationLevelEnum] = None
#     ethnicity: EthnicityEnum = None
#     city: Optional[str] = None
#     whatsapp_number: Optional[str] = None
#     weekly_hours_worked: Optional[int] = None
#     date_of_birth: Optional[datetime] = None
#     country: Optional[str] = None
#     cep: Optional[str] = None
#     # street: Optional[str] = None
#     # neighborhood: Optional[str] = None
#     # number: Optional[str] = None
#     cpf: Optional[str] = None


# class ErrorResponse(Schema):
#     message: str
from enum import Enum
from typing import Optional
from ninja import Schema, Field
from datetime import datetime
from pydantic import validator,conint


class RoleFilterEnum(str, Enum):
    user = "user"


class StateEnum(str, Enum):
    AC = "AC"
    AL = "AL"
    AP = "AP"
    AM = "AM"
    BA = "BA"
    CE = "CE"
    DF = "DF"
    ES = "ES"
    GO = "GO"
    MA = "MA"
    MT = "MT"
    MS = "MS"
    MG = "MG"
    PA = "PA"
    PB = "PB"
    PR = "PR"
    PE = "PE"
    PI = "PI"
    RJ = "RJ"
    RN = "RN"
    RS = "RS"
    RO = "RO"
    RR = "RR"
    SC = "SC"
    SP = "SP"
    SE = "SE"
    TO = "TO"


class EducationLevelEnum(str, Enum):
    SEM_ESCOLARIDADE = "Sem escolaridade"
    ENSINO_FUNDAMENTAL = "Ensino Fundamental"
    ENSINO_MEDIO = "Ensino Médio"
    GRADUACAO = "Graduação"
    ESPECIALIZACAO = "Especialização"
    MESTRADO = "Mestrado"
    DOUTORADO = "Doutorado"
    POS_DOUTORADO = "Pós-Doutorado"


class GenderEnum(str, Enum):
    m = "m"
    f = "f"
    n = "p"


class EthnicityEnum(str, Enum):
    BRANCA = "Branca"
    PRETA = "Preta"
    PARDA = "Parda"
    AMARELA = "Amarela"
    INDIGENA = "Indígena"


class UserPostSchema(Schema):
    username: str
    email: str
    password: str
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    profession: Optional[str] = None
    role: Optional[str] = None
    state: Optional[str] = None
    gender: Optional[str] = None
    institution: Optional[str] = None
    education_level: Optional[str] = None
    ethnicity: Optional[str] = None
    city: Optional[str] = None
    whatsapp_number: Optional[str] = None
    # weekly_hours_worked: Optional[conint(ge=0)] = None
    # date_of_birth: Optional[str] = None
    country: Optional[str] = None
    cep: Optional[str] = None
    cpf: Optional[str] = None


class UserPutSchema(Schema):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    profession: Optional[str] = None
    role: Optional[str] = None
    state: Optional[str] = None
    gender: Optional[str] = None
    institution: Optional[str] = None
    education_level: Optional[str] = None
    ethnicity: Optional[str] = None
    city: Optional[str] = None
    whatsapp_number: Optional[str] = None
    # weekly_hours_worked: Optional[conint(ge=0)] = None
    # date_of_birth: Optional[str] = None
    country: Optional[str] = None
    cep: Optional[str] = None
    cpf: Optional[str] = None


class UserListSchema(Schema):
    id: int
    username: str
    email: str
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    profession: Optional[str] = None
    role: Optional[str] = None
    profile_picture: Optional[str] = None
    state: Optional[str] = None
    gender: Optional[str] = None
    institution: Optional[str] = None
    education_level: Optional[str] = None
    ethnicity: Optional[str] = None
    city: Optional[str] = None
    whatsapp_number: Optional[str] = None
    # weekly_hours_worked: Optional[conint(ge=0)] = None
    # date_of_birth: Optional[str] = None
    country: Optional[str] = None
    date_joined: datetime
    last_login: datetime
    is_active: bool
    cep: Optional[str] = None
    cpf: Optional[str] = None


class RegisterSchema(Schema):
    username: str
    email: str
    password: str
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    profession: Optional[str] = None
    role: Optional[str] = None
    state: Optional[str] = None
    gender: Optional[str] = None
    institution: Optional[str] = None
    education_level: Optional[str] = None
    ethnicity: Optional[str] = None
    city: Optional[str] = None
    whatsapp_number: Optional[str] = None
    # weekly_hours_worked: Optional[conint(ge=0)] = None
    # date_of_birth: Optional[str] = None
    country: Optional[str] = None
    cep: Optional[str] = None
    cpf: Optional[str] = None


class RegisterResponseSchema(Schema):
    id: int
    username: str
    email: str
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    profession: Optional[str] = None
    state: Optional[str] = None
    gender: Optional[str] = None
    institution: Optional[str] = None
    education_level: Optional[str] = None
    ethnicity: Optional[str] = None
    city: Optional[str] = None
    whatsapp_number: Optional[str] = None
    # weekly_hours_worked: Optional[conint(ge=0)] = None
    # date_of_birth: Optional[str] = None
    country: Optional[str] = None
    cep: Optional[str] = None
    cpf: Optional[str] = None


class ErrorResponse(Schema):
    message: str
