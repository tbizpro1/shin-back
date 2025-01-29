from enum import Enum
from typing import Optional,List
from ninja import Schema, Field,FilterSchema
from datetime import datetime
from pydantic import EmailStr, HttpUrl,BaseModel

# Enum para filtrar por estado de investimento
class InvestedFilterEnum(str, Enum):
    yes = "yes"
    no = "no"

# Schema para criação (POST)
class EnterprisePostSchema(BaseModel):
    name: str
    email: Optional[EmailStr] = Field(None, title="Email")
    linkedin: Optional[HttpUrl] = Field(None, title="LinkedIn")
    instagram: Optional[HttpUrl] = Field(None, title="Instagram")
    whatsapp: Optional[str] = Field(None, title="WhatsApp")
    website: Optional[HttpUrl] = Field(None, title="Website")
    summary: Optional[str] = Field(None, title="Resumo")
    cnpj: Optional[str] = Field(None, title="CNPJ")
    foundation_year: Optional[int] = Field(None, title="Ano de Fundação")
    city: Optional[str] = Field(None, title="Cidade")
    state: Optional[str] = Field(None, title="Estado")
    market: Optional[str] = Field(None, title="Mercado")
    segment: Optional[str] = Field(None, title="Segmento Inicial de Atuação")
    problem: str
    solution: str
    client_type: Optional[str] = Field(None, title="Tipo de Cliente da Solução")
    product: str
    product_stage: Optional[str] = Field(None, title="Estágio de Maturidade do Produto")
    value_proposition: str
    differential: str
    competitors: str
    business_model: Optional[str] = Field(None, title="Modelo de Negócio")
    revenue_model: Optional[str] = Field(None, title="Modelo de Receita")
    invested: Optional[bool] = Field(False, title="Já foi investida?")
    investment_value: Optional[float] = Field(None, title="Valor Investido")
    boosting: Optional[bool] = Field(False, title="Recebeu Fomento?")
    funding_value: Optional[float] = Field(None, title="Valor de Fomento")
    funding_program: Optional[str] = Field(None, title="Programa de Fomento")
    accelerated: Optional[bool] = Field(False, title="Já foi Acelerada?")
    accelerator_name: Optional[str] = Field(None, title="Nome da Aceleradora")
    discovered_startup: Optional[str] = Field(None, title="Onde conheceu a Startup Piauí?")
    other_projects: Optional[str] = Field(None, title="Outros Projetos no Startup Piauí")

# Schema para atualização (PUT)
class EnterprisePutSchema(BaseModel):
    name: Optional[str] = Field(None, alias="name", title="Nome da empresa")
    email: Optional[EmailStr] = Field(None, alias="email", title="Email")
    linkedin: Optional[HttpUrl] = Field(None, alias="linkedin", title="LinkedIn")
    instagram: Optional[HttpUrl] = Field(None, alias="instagram", title="Instagram")
    whatsapp: Optional[str] = Field(None, alias="whatsapp", title="WhatsApp")
    website: Optional[HttpUrl] = Field(None, alias="website", title="Website")
    summary: Optional[str] = Field(None, alias="summary", title="Resumo")
    cnpj: Optional[str] = Field(None, alias="cnpj", title="CNPJ")
    foundation_year: Optional[int] = Field(None, alias="foundation_year", title="Ano de Fundação")
    city: Optional[str] = Field(None, alias="city", title="Cidade")
    state: Optional[str] = Field(None, alias="state", title="Estado")
    market: Optional[str] = Field(None, alias="market", title="Mercado")
    segment: Optional[str] = Field(None, alias="segment", title="Segmento Inicial de Atuação")
    problem: Optional[str] = Field(None, alias="problem", title="Problema")
    solution: Optional[str] = Field(None, alias="solution", title="Solução")
    client_type: Optional[str] = Field(None, alias="client_type", title="Tipo de Cliente da Solução")
    product: Optional[str] = Field(None, alias="product", title="Produto")
    product_stage: Optional[str] = Field(None, alias="product_stage", title="Estágio de Maturidade do Produto")
    value_proposition: Optional[str] = Field(None, alias="value_proposition", title="Proposta de Valor")
    differential: Optional[str] = Field(None, alias="differential", title="Diferencial")
    competitors: Optional[str] = Field(None, alias="competitors", title="Concorrentes")
    business_model: Optional[str] = Field(None, alias="business_model", title="Modelo de Negócio")
    revenue_model: Optional[str] = Field(None, alias="revenue_model", title="Modelo de Receita")
    invested: Optional[bool] = Field(None, alias="invested", title="Já foi investida?")
    investment_value: Optional[float] = Field(None, alias="investment_value", title="Valor Investido")
    boosting: Optional[bool] = Field(None, alias="boosting", title="Recebeu Fomento?")
    funding_value: Optional[float] = Field(None, alias="funding_value", title="Valor de Fomento")
    funding_program: Optional[str] = Field(None, alias="funding_program", title="Programa de Fomento")
    accelerated: Optional[bool] = Field(None, alias="accelerated", title="Já foi Acelerada?")
    accelerator_name: Optional[str] = Field(None, alias="accelerator_name", title="Nome da Aceleradora")
    discovered_startup: Optional[str] = Field(None, alias="discovered_startup", title="Onde conheceu a Startup Piauí?")
    other_projects: Optional[str] = Field(None, alias="other_projects", title="Outros Projetos no Startup Piauí")

# Schema para listagem (GET)
class EnterpriseListSchema(BaseModel):
    enterprise_id: int
    name: str
    email: Optional[EmailStr] = None
    linkedin: Optional[HttpUrl] = None
    instagram: Optional[HttpUrl] = None
    whatsapp: Optional[str] = None
    website: Optional[HttpUrl] = None
    summary: Optional[str] = None
    cnpj: Optional[str] = None
    foundation_year: Optional[int] = None
    city: Optional[str] = None
    state: Optional[str] = None
    market: Optional[str] = None
    segment: Optional[str] = None
    problem: str
    solution: str
    client_type: Optional[str] = None
    product: str
    product_stage: Optional[str] = None
    value_proposition: str
    differential: str
    competitors: str
    business_model: Optional[str] = None
    revenue_model: Optional[str] = None
    invested: Optional[bool] = False
    investment_value: Optional[float] = None
    boosting: Optional[bool] = False
    funding_value: Optional[float] = None
    funding_program: Optional[str] = None
    accelerated: Optional[bool] = False
    accelerator_name: Optional[str] = None
    discovered_startup: Optional[str] = None
    other_projects: Optional[str] = None
    
class CompanyMetricsPostSchema(Schema):
    enterprise: int =  Field(None, alias="enterprise", title="ID da empresa")
    team_size:int = Field(None, alias="team_size", title="Tamanho do time")
    revenue_period: float = Field(None, alias="revenue_period", title="periodo de revenda")
    total_clients:int = Field(None, alias="total_clients", title="total de clientes")
    new_clients:int = Field(None, alias="new_clients", title="Número de novos clientes durante o período")
    investment_round_open:bool = Field(None, alias="investment_round_open", title="A empresa está com rodada de investimento aberta?") 
    capital_needed:float =Field(None, alias="capital_needed", title="Necessidade de capital caso a rodada esteja aberta")  
    value_invested:float = Field(None, alias="value_invested", title="Valor investido")  
    value_foment:float = Field(None, alias="value_foment", title="Valor do fomento")  
    valuation:str = Field(None, alias="valuation", title="Valor estimado do negócio (ou escreva NÃO SEI)") 

class CompanyMetricsGetSchema(Schema):
    enterprise: int =  Field(None, alias="enterprise", title="ID da empresa")
    team_size:int = Field(None, alias="team_size", title="Tamanho do time")
    revenue_period: float = Field(None, alias="revenue_period", title="periodo de revenda")
    total_clients:int = Field(None, alias="total_clients", title="total de clientes")
    new_clients:int = Field(None, alias="new_clients", title="Número de novos clientes durante o período")
    investment_round_open:bool = Field(None, alias="investment_round_open", title="A empresa está com rodada de investimento aberta?") 
    capital_needed:float =Field(None, alias="capital_needed", title="Necessidade de capital caso a rodada esteja aberta")  
    value_invested:float = Field(None, alias="value_invested", title="Valor investido")  
    value_foment:float = Field(None, alias="value_foment", title="Valor do fomento")  
    valuation:str = Field(None, alias="valuation", title="Valor estimado do negócio (ou escreva NÃO SEI)")

class CompanyMetricsListSchema(Schema):
    enterprises_metrics: List[CompanyMetricsGetSchema]

class CompanyMetricsPutSchema(Schema):
    team_size: Optional[int]  = Field(None, alias="team_size", title="Tamanho do time")
    revenue_period: Optional[float]  = Field(None, alias="revenue_period", title="periodo de revenda")
    total_clients: Optional[int] = Field(None, alias="total_clients", title="total de clientes")
    new_clients: Optional[int] = Field(None, alias="new_clients", title="Número de novos clientes durante o período")
    investment_round_open: Optional[bool] = Field(None, alias="investment_round_open", title="A empresa está com rodada de investimento aberta?") 
    capital_needed: Optional[float] =Field(None, alias="capital_needed", title="Necessidade de capital caso a rodada esteja aberta")  
    value_invested: Optional[float] = Field(None, alias="value_invested", title="Valor investido")  
    value_foment: Optional[float] = Field(None, alias="value_foment", title="Valor do fomento")  
    valuation: Optional[str] = Field(None, alias="valuation", title="Valor estimado do negócio (ou escreva NÃO SEI)") 

class CompanyMetricsFilterSchema(FilterSchema):
    team_size: Optional[int]  = None
    revenue_period: Optional[float]  = None
    total_clients: Optional[int] = None
    new_clients: Optional[int] = None
    investment_round_open: Optional[bool] = None
    capital_needed: Optional[float] = None  
    value_invested: Optional[float] = None 
    value_foment: Optional[float] = None
    valuation: Optional[str] = None



# Schema de resposta para erros
class ErrorResponse(Schema):
    message: str
