from enum import Enum
from typing import Optional,List, Union
from ninja import Schema, Field,FilterSchema
from datetime import datetime,date
from pydantic import EmailStr, HttpUrl,BaseModel
from enum import Enum
from typing import Optional, List
from datetime import  date, datetime
from ninja import FilterSchema, Schema, Field
from pydantic import BaseModel, EmailStr
class BusinessModelEnum(str, Enum):
    NAO_SEI = "Não sei"
    AFILIADOS = "Afiliados / Marketing de influência"
    CONTEUDO_PREMIUM = "Conteúdo premium / Licenciamento de conteúdo / Educação on-line"
    COOPERATIVA = "Cooperativa"
    SOFTWARE_HOUSE = "Software house"
    ECOMMERCE = "E-commerce"
    MARKETPLACE = "Marketplace"
    SAAS = "SAAS - Software como serviço"
    HAAS = "HAAS - Hardware como serviço"
    INDUSTRIA = "Indústria: Fabricação e venda direta online ou offline"
    EDUCACAO_ONLINE = "Educação on-line"
    COMERCIO_OFFLINE = "Comércio Offline"
    SERVICO_OFFLINE = "Serviço Offline"
    EDUCACAO_OFFLINE = "Educação off-line"
    INTERMEDIACAO = "Intermediação de negócios"
    NEGOCIO_SOCIAL = "Negócio social"
    PUBLICIDADE = "Publicidade"
    OUTROS = "Outros"



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

class RevenueModelEnum(str, Enum):
    NAO_SEI = "Não sei"
    AFILIADOS = "Afiliados"
    ANUNCIO = "Anúncio"
    ASSINATURA = "Assinatura"
    FREEMIUM = "Freemium"
    LICENCIAMENTO = "Licenciamento"
    INTERMEDIACAO = "Intermediação de Negócios"
    PAY_PER_USE = "Pay per Use"
    VENDA_HARDWARE = "Venda de Hardware ou produto físico"
    VENDA_DIRETA = "Venda Direta"
    TRANSACIONAL = "Transacional"
    OUTRO = "Outro"

class CycleEnum(str, Enum):
    STARTUP_PIAUI_1 = "Startup Piaui 1"
    STARTUP_PIAUI_2 = "Startup Piaui 2"
    STARTUP_PIAUI_3 = "Startup Piaui 3"
    STARTUP_PIAUI_4 = "Startup Piaui 4"
    STARTUP_PIAUI_5 = "Startup Piaui 5"
    STARTUP_PIAUI_6 = "Startup Piaui 6"
    STARTUP_PIAUI_7 = "Startup Piaui 7"
    BATALHA_DO_CONHECIMENTO_1 = "Batalha do Conhecimento 1"
    MARATONA_DE_NEGOCIOS_1 = "Maratona de Negócios 1"
    BATALHA_DE_STARTUPS_1 = "Batalha de Startups 1"
    INVESTE_NELAS_1 = "Investe Nelas 1"
    INVESTE_NELAS_2 = "Investe Nelas 2"
    EXPO_FAVELA_2024 = "Expo Favela 2024"
    EXPO_FAVELA_2023 = "Expo Favela 2023"

class DiscoverySourceEnum(str, Enum):
    IMMERSION = 'Fui numa imersão do Programa'
    CAMPUS_PARTY = 'Campus Party'
    INVESTE_NELAS_1 = 'Investe Nelas 1'
    INVESTE_NELAS_2 = 'Investe Nelas 2'
    EXPO_FAVELA_2023 = 'Expo Favela 2023'
    EXPO_FAVELA_2024 = 'Expo Favela 2024'
    GOOGLE_SEARCH = 'Achei no Google'
    SOCIAL_MEDIA = 'Mídias Sociais'
    REFERRAL = 'Indicação'
    STARTUP_PIAUI_EVENT = 'Evento do Startup Piauí'
    OTHER = 'Outros'

class MaturityStageBusinessEnum(str, Enum):
    LOOKING_FOR_TEAM = 'Procurando Equipe'
    IDEATION = 'Ideação (Modelando produto, sem MVP)'
    MVP = 'MVP'
    INITIAL_TESTS = 'Primeiros testes (até 5 clientes)'
    BETA_PHASE = 'Fase Beta de Negócio (menos que 20 clientes)'
    MONETIZATION = 'Monetização (Faturamento > 10k, mais que 20 clientes, 1 recompra)'
    CLIENT_CREATION = 'Criação de clientes (Faturamento > 30k em 3 meses)'
    COMPANY_BUILDING = 'Construção de empresa (Faturamento > 1mi / 12 meses OU > 100k 3 meses OU investimento > 1mi)'
    SCALE_UP = 'Scale Up'

class MaturityLevelEnum(str, Enum):
    TRL_0 = 'TRL 0 - Não iniciado'
    TRL_1 = 'TRL 1 - Princípios básicos observados e documentados'
    TRL_2 = 'TRL 2 - Formulação do conceito da tecnologia'
    TRL_3 = 'TRL 3 - Prova de conceito experimental'
    TRL_4 = 'TRL 4 - Validação do conceito em laboratório'
    TRL_5 = 'TRL 5 - Validação do conceito em ambiente relevante'
    TRL_6 = 'TRL 6 - Demonstração em ambiente relevante'
    TRL_7 = 'TRL 7 - Demonstração em ambiente operacional'
    TRL_8 = 'TRL 8 - Sistema completo e qualificado'
    TRL_9 = 'TRL 9 - Sistema comprovado em ambiente operacional'

class RecordTypeEnum(str, Enum):
    HOMEWORK = 'Dever de casa'
    INTEL = 'Intel'
    RECEIVED_REQUEST = 'Recebemos pedido'
    FOLLOW_UP = 'Follow'
    BOARD_MEETING = 'Reunião de Conselho'
    MONITORING_MEETING = 'Reunião de Acompanhamento'

class MITPhaseEnum(str, Enum):
    PHASE_1 = 'Fase 1'
    PHASE_2 = 'Fase 2'
    PHASE_3 = 'Fase 3'

class BusinessLevelEnum(str, Enum):
    LOOKING_FOR_TEAM = 'Procurando Equipe'
    IDEATION = 'Ideação'
    MVP = 'MVP'
    TESTING = 'Primeiros Testes'
    BETA_PHASE = 'Fase Beta'
    MONETIZATION = 'Monetização'
    CLIENT_CREATION = 'Criação de Clientes'
    BUILDING_COMPANY = 'Construção de Empresa'
    SCALE_UP = 'Scale Up'


class MarketEnum(str, Enum):
    AGRICULTURE_LIVESTOCK = "Agricultura e Pecuária"
    FOOD_BEVERAGES = "Alimentos e Bebidas"
    AUTOMOTIVE_MOBILITY = "Automotivo e Mobilidade"
    CAPITAL_INVESTMENTS = "Capital e Investimentos"
    ECOMMERCE = "Comércio eletrônico"
    COMMUNICATION_MEDIA = "Comunicação e Mídia"
    CONSTRUCTION_REAL_ESTATE = "Construção e Imóveis"
    CREDIT_FINANCE = "Crédito e Finanças"
    EDUCATION = "Educação"
    ENERGY = "Energia"
    SPORTS_LEISURE = "Esportes e Lazer"
    MANAGEMENT_CONSULTING = "Gestão e Consultoria"
    GOVERNMENT_PUBLIC_SECTOR = "Governo e Poder Público"
    HOSPITALITY_TOURISM = "Hotelaria e Turismo"
    INDUSTRY_MANUFACTURING = "Indústria e Transformação"
    GAMES_ENTERTAINMENT = "Jogos e Entretenimento"
    LOGISTICS_TRANSPORT = "Logística e Transportes"
    FASHION_CLOTHING = "Moda e Vestuário"
    ENGINES_EQUIPMENT = "Motores e Equipamentos"
    OIL_GAS = "Óleo e Gás"
    HEALTHCARE = "Saúde"
    WELLNESS = "Bem Estar"
    SECURITY_DEFENSE = "Segurança e Defesa"
    INSURANCE = "Seguros"
    PROFESSIONAL_SERVICES = "Serviços profissionais"
    ENVIRONMENT = "Meio ambiente"
    SUSTAINABILITY = "Sustentabilidade"
    INFORMATION_TECHNOLOGY = "Tecnologia da Informação"
    TELECOMMUNICATIONS = "Telecomunicações"
    RETAIL_WHOLESALE = "Varejo e Atacado"
    OTHER = "Outro"

class MetricMonthEnum(str, Enum):
    JANUARY = 'JAN'
    FEBRUARY = 'FEV'
    MARCH = 'MAR'
    APRIL = 'ABR'
    MAY = 'MAI'
    JUNE = 'JUN'
    JULY = 'JUL'
    AUGUST = 'AGO'
    SEPTEMBER = 'SET'
    OCTOBER = 'OUT'
    NOVEMBER = 'NOV'
    DECEMBER = 'DEZ'

class EnterprisePutSchema(BaseModel):
    name: Optional[str] = Field(None, alias="name", title="Nome da empresa")
    email: Optional[EmailStr] = Field(None, alias="email", title="Email")
    linkedin: Optional[str] = Field(None, alias="linkedin", title="LinkedIn")
    instagram: Optional[str] = Field(None, alias="instagram", title="Instagram")
    whatsapp: Optional[str] = Field(None, alias="whatsapp", title="WhatsApp")
    website: Optional[str] = Field(None, alias="website", title="Website")
    summary: Optional[str] = Field(None, alias="summary", title="Resumo")
    cnpj: Optional[str] = Field(None, alias="cnpj", title="CNPJ")
    foundation_year: Optional[int] = Field(None, alias="foundation_year", title="Ano de Fundação")
    city: Optional[str] = Field(None, alias="city", title="Cidade")
    state: Optional[StateEnum] = Field(None, alias="state", title="Estado")
    market: Optional[MarketEnum] = Field(None, alias="market", title="Mercado")
    segment: Optional[str] = Field(None, alias="segment", title="Segmento Inicial de Atuação")
    problem: Optional[str] = Field(None, alias="problem", title="Problema")
    solution: Optional[str] = Field(None, alias="solution", title="Solução")
    client_type: Optional[str] = Field(None, alias="client_type", title="Tipo de Cliente da Solução")
    product: Optional[str] = Field(None, alias="product", title="Produto")
    product_stage: Optional[MaturityLevelEnum] = Field(None, title="Estágio de Maturidade do Produto")
    value_proposition: Optional[str] = Field(None, alias="value_proposition", title="Proposta de Valor")
    differential: Optional[str] = Field(None, alias="differential", title="Diferencial")
    competitors: Optional[str] = Field(None, alias="competitors", title="Concorrentes")
    business_model: Optional[BusinessModelEnum] = Field(None, alias="business_model", title="Modelo de Negócio")
    revenue_model: Optional[RevenueModelEnum] = Field(None, alias="revenue_model", title="Modelo de Receita")
    invested: Optional[bool] = Field(None, alias="invested", title="Já foi investida?")
    investment_value: Optional[float] = Field(None, alias="investment_value", title="Valor Investido")
    boosting: Optional[bool] = Field(None, alias="boosting", title="Recebeu Fomento?")
    funding_value: Optional[float] = Field(None, alias="funding_value", title="Valor de Fomento")
    funding_program: Optional[str] = Field(None, alias="funding_program", title="Programa de Fomento")
    accelerated: Optional[bool] = Field(None, alias="accelerated", title="Já foi Acelerada?")
    accelerator_name: Optional[str] = Field(None, alias="accelerator_name", title="Nome da Aceleradora")
    other_projects: Optional[str] = Field(None, alias="other_projects", title="Outros Projetos no Startup Piauí")
    initial_maturity: Optional[MaturityStageBusinessEnum] = Field(None, alias="initial_maturity", title="Estágio Inicial")
    discovered_startup: Optional[DiscoverySourceEnum] = Field(None, alias="discovered_startup", title="Onde conheceu a Startup Piauí?")
    cycle: Optional[CycleEnum] = Field(None, alias="cycle", title="Ciclo")

class EnterpriseListSchema(BaseModel):
    enterprise_id: int
    name: str
    email: Optional[EmailStr] = None
    linkedin: Optional[str] = None
    instagram: Optional[str] = None
    whatsapp: Optional[str] = None
    website: Optional[str] = None
    summary: Optional[str] = None
    cnpj: Optional[str] = None
    foundation_year: Optional[int] = None
    city: Optional[str] = None
    state: Optional[StateEnum] = None
    market: Optional[MarketEnum] = None
    segment: Optional[str] = None
    problem: Optional[str] = None
    solution: Optional[str] = None
    differential: Optional[str] = None
    client_type: Optional[str] = None
    product: Optional[str] = None
    product_stage: Optional[MaturityLevelEnum] = None
    value_proposition: Optional[str] = None
    differential: Optional[str] = None
    competitors: Optional[str] = None
    business_model: Optional[BusinessModelEnum] = None
    revenue_model: RevenueModelEnum = None
    invested: Optional[bool] = False
    investment_value: Optional[float] = None
    boosting: Optional[bool] = False
    funding_value: Optional[float] = None
    funding_program: Optional[str] = None
    accelerated: Optional[bool] = False
    accelerator_name: Optional[str] = None
    discovered_startup: Optional[str] = None
    other_projects: Optional[str] = None
    profile_picture: Optional[str] = None
    initial_maturity: Optional[MaturityStageBusinessEnum] = None
    discovered_startup: Optional[DiscoverySourceEnum] = None
    cycle: Optional[CycleEnum] = None


class CompanyMetricsPostSchema(Schema):
    enterprise: int =  Field(None, alias="enterprise", title="ID da empresa")
    team_size:int = Field(None, alias="team_size", title="Tamanho do time")
    revenue_period: float = Field(None, alias="revenue_period", title="periodo de revenda")
    total_clients:int = Field(None, alias="total_clients", title="total de clientes")
    new_clients:int = Field(None, alias="new_clients", title="Número de novos clientes durante o período")
    investment_round_open:bool = Field(None, alias="investment_round_open", title="A empresa está com rodada de investimento aberta?") 
    capital_needed:float =Field(None, alias="capital_needed", title="Necessidade de capital caso a rodada esteja aberta")  
    value_foment:float = Field(None, alias="value_foment", title="Valor do fomento")  
    valuation:str = Field(None, alias="valuation", title="Valor estimado do negócio (ou escreva NÃO SEI)")
    current_capital:Optional[float] = Field(None, alias="current_capital", title="Capital atual") 
    captable:Optional[float] = Field(None, alias="captable", title="Captable")
    partners_count:Optional[int] = Field(None, alias="partners_count", title="Quantidade de sócios")

class CompanyMetricsGetSchema(Schema):
    id: Optional[int] = Field(None, alias="id", title="ID da empresa")  # Adicionando o id
    enterprise_id: int =  Field(None, alias="enterprise_id", title="ID da empresa")
    team_size:int = Field(None, alias="team_size", title="Tamanho do time")
    revenue_period: float = Field(None, alias="revenue_period", title="periodo de revenda")
    total_clients:int = Field(None, alias="total_clients", title="total de clientes")
    new_clients:int = Field(None, alias="new_clients", title="Número de novos clientes durante o período")
    investment_round_open:bool = Field(None, alias="investment_round_open", title="A empresa está com rodada de investimento aberta?") 
    capital_needed:float =Field(None, alias="capital_needed", title="Necessidade de capital caso a rodada esteja aberta")  
    value_foment:float = Field(None, alias="value_foment", title="Valor do fomento")  
    valuation:str = Field(None, alias="valuation", title="Valor estimado do negócio (ou escreva NÃO SEI)")
    date_recorded: Optional[datetime] = Field(None, alias="date_recorded", title="Data de criação")
    current_capital:Optional[float] = Field(None, alias="current_capital", title="Capital atual") 
    captable:Optional[float] = Field(None, alias="captable", title="Captable")
    partners_count:Optional[int] = Field(None, alias="partners_count", title="Quantidade de sócios")
    metric_month:Optional[str] = Field(None, alias="metric_month", title="Mês da métrica")
    metric_year:Optional[int] = Field(None, alias="metric_year", title="Ano da métrica")

    class Config:
        # Isso garante que ao fazer a conversão com from_orm, ele consiga mapear o valor correto
        orm_mode = True

class CompanyMetricsPutSchema(Schema):
    team_size: Optional[int]  = Field(None, alias="team_size", title="Tamanho do time")
    revenue_period: Optional[float]  = Field(None, alias="revenue_period", title="periodo de revenda")
    total_clients: Optional[int] = Field(None, alias="total_clients", title="total de clientes")
    new_clients: Optional[int] = Field(None, alias="new_clients", title="Número de novos clientes durante o período")
    investment_round_open: Optional[bool] = Field(None, alias="investment_round_open", title="A empresa está com rodada de investimento aberta?") 
    capital_needed: Optional[float] =Field(None, alias="capital_needed", title="Necessidade de capital caso a rodada esteja aberta")  
    value_foment: Optional[float] = Field(None, alias="value_foment", title="Valor do fomento")  
    valuation: Optional[str] = Field(None, alias="valuation", title="Valor estimado do negócio (ou escreva NÃO SEI)") 
    current_capital: Optional[float] = Field(None, alias="current_capital", title="Capital atual")
    captable:Optional[float] = Field(None, alias="captable", title="Captable")
    date_recorded: Optional[datetime] = Field(None, alias="date_recorded", title="Data de criação")
    metric_month:Optional[MetricMonthEnum] = Field(None, alias="metric_month", title="Mês da métrica")
    metric_year:Optional[int] = Field(None, alias="metric_year", title="Ano da métrica")
    partners_count:Optional[int] = Field(None, alias="partners_count", title="Quantidade de sócios")


class RecordInSchema(BaseModel):
    enterprise: int
    date_collected: date
    responsible_person: str = Field(..., min_length=3, max_length=255)
    mit_phase: MITPhaseEnum
    product_status: MaturityLevelEnum
    initial_maturity: BusinessLevelEnum
    how_we_can_help: Optional[str] = Field(None, max_length=500)
    next_steps: Optional[str] = Field(None, max_length=500)
    next_meeting_date: Optional[date] = None
    observations: Optional[str] = Field(None, max_length=500)
    data_type: RecordTypeEnum
    cycle: CycleEnum
    market: MarketEnum

class RecordMinimalSchema(Schema):
    id: int
    enterprise: int

class RecordOutSchema(Schema):
    enterprise: int 
    id: int
    date_collected: date
    responsible_person: str
    mit_phase: MITPhaseEnum
    product_status: MaturityLevelEnum
    initial_maturity: BusinessLevelEnum
    how_we_can_help: Optional[str]
    next_steps: Optional[str]
    next_meeting_date: Optional[date]
    observations: Optional[str]
    data_type: RecordTypeEnum
    cycle: Optional[CycleEnum]

class ErrorResponse(Schema):
    message: str

class RecordFilterSchema(FilterSchema):
    enterprise: Optional[int] = None
    date_collected_start: Optional[date] = None
    date_collected_end: Optional[date] = None
    mit_phase: Optional[MITPhaseEnum] = None
    product_status: Optional[MaturityLevelEnum] = None
    initial_maturity: Optional[BusinessLevelEnum] = None
    data_type: Optional[RecordTypeEnum] = None
    cycle: Optional[CycleEnum] = None

class RecordPutSchema(BaseModel):
    enterprise: Optional[int] = None
    date_collected: Optional[date] = None
    responsible_person: Optional[str] = Field(None, min_length=3, max_length=255)
    mit_phase: Optional[MITPhaseEnum] = None
    product_status: Optional[MaturityLevelEnum] = None
    initial_maturity: Optional[BusinessLevelEnum] = None
    how_we_can_help: Optional[str] = Field(None, max_length=500)
    next_steps: Optional[str] = Field(None, max_length=500)
    next_meeting_date: Optional[date] = None
    observations: Optional[str] = Field(None, max_length=500)
    data_type: Optional[RecordTypeEnum] = None
    cycle: Optional[CycleEnum]



class EnterprisePostSchema(Schema):
    name: str
    email: Optional[str] = Field(None, title="Email")
    linkedin: Optional[str] = Field(None, title="LinkedIn")
    instagram: Optional[str] = Field(None, title="Instagram")
    whatsapp: Optional[str] = Field(None, title="WhatsApp")
    website: Optional[str] = Field(None, title="Website")
    summary: Optional[str] = Field(None, title="Resumo")
    cnpj: Optional[str] = Field(None, title="CNPJ")
    foundation_year: Optional[int] = Field(None, title="Ano de Fundação")
    city: Optional[str] = Field(None, title="Cidade")
    state: StateEnum = Field(None, title="Estado")
    market:MarketEnum = Field(None, title="Mercado")
    segment: Optional[str] = Field(None, title="Segmento Inicial")
    problem: Optional[str] = Field(None, title="Problema Resolvido")
    solution: Optional[str] = Field(None, title="Solução")
    client_type: Optional[str] = Field(None, title="Tipo de Cliente")
    product: Optional[str] = Field(None, title="Produto")
    product_stage: MaturityLevelEnum = Field(..., title="Estágio do Produto")
    value_proposition: str
    differential: str
    competitors: str
    business_model: BusinessModelEnum = Field(None, title="Modelo de Negócio")
    revenue_model:RevenueModelEnum = Field(None, title="Modelo de Receita")
    invested: Optional[bool] = Field(False, title="Já recebeu investimento?")
    investment_value: Optional[float] = Field(None, title="Valor Investido")
    boosting: Optional[bool] = Field(False, title="Recebeu fomento?")
    funding_value: Optional[float] = Field(None, title="Valor de Fomento")
    funding_program: Optional[str] = Field(None, title="Programa de Fomento")
    accelerated: Optional[bool] = Field(False, title="Já foi acelerada?")
    accelerator_name: Optional[str] = Field(None, title="Nome da Aceleradora")
    discovered_startup: DiscoverySourceEnum = Field(None, title="Como conheceu o programa?")
    initial_maturity: MaturityStageBusinessEnum = Field(None, title="Estágio Inicial")
    cycle: CycleEnum = Field(None, title="Ciclo")
    owner_percentage: Union[str] = None

    
class ErrorResponse(Schema):
    message: str

class CompanyMetricsFilterSchema(FilterSchema):
    team_size: Optional[int]  = None
    revenue_period: Optional[float]  = None
    total_clients: Optional[int] = None
    new_clients: Optional[int] = None
    investment_round_open: Optional[bool] = None
    capital_needed: Optional[float] = None  
    value_foment: Optional[float] = None
    valuation: Optional[str] = None
    enterprise_id: Optional[int] = None

    
class CompanyMetricsListSchema(Schema):
    enterprises_metrics: List[CompanyMetricsGetSchema]

    class Config:
        orm_mode = True
        