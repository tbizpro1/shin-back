from django.db import models

class Enterprise(models.Model):
    class state_choices(models.TextChoices):
        AC = "AC", "Acre"
        AL = "AL", "Alagoas"
        AP = "AP", "Amapá"
        AM = "AM", "Amazonas"
        BA = "BA", "Bahia"
        CE = "CE", "Ceará"
        DF = "DF", "Distrito Federal"
        ES = "ES", "Espírito Santo"
        GO = "GO", "Goiás"
        MA = "MA", "Maranhão"
        MT = "MT", "Mato Grosso"
        MS = "MS", "Mato Grosso do Sul"
        MG = "MG", "Minas Gerais"
        PA = "PA", "Pará"
        PB = "PB", "Paraíba"
        PR = "PR", "Paraná"
        PE = "PE", "Pernambuco"
        PI = "PI", "Piauí"
        RJ = "RJ", "Rio de Janeiro"
        RN = "RN", "Rio Grande do Norte"
        RS = "RS", "Rio Grande do Sul"
        RO = "RO", "Rondônia"
        RR = "RR", "Roraima"
        SC = "SC", "Santa Catarina"
        SP = "SP", "São Paulo"
        SE = "SE", "Sergipe"
        TO = "TO", "Tocantins"


    class BusinessModelChoices(models.TextChoices):
        NAO_SEI = "Não sei", "Não sei"
        AFILIADOS = "Afiliados / Marketing de influência", "Afiliados / Marketing de influência"
        CONTEUDO_PREMIUM = "Conteúdo premium / Licenciamento de conteúdo / Educação on-line", "Conteúdo premium / Licenciamento de conteúdo / Educação on-line"
        COOPERATIVA = "Cooperativa", "Cooperativa"
        SOFTWARE_HOUSE = "Software house", "Software house"
        ECOMMERCE = "E-commerce", "E-commerce"
        MARKETPLACE = "Marketplace", "Marketplace"
        SAAS = "SAAS - Software como serviço", "SAAS - Software como serviço"
        HAAS = "HAAS - Hardware como serviço", "HAAS - Hardware como serviço"
        INDUSTRIA = "Indústria: Fabricação e venda direta online ou offline", "Indústria: Fabricação e venda direta online ou offline"
        EDUCACAO_ONLINE = "Educação on-line", "Educação on-line"
        COMERCIO_OFFLINE = "Comércio Offline", "Comércio Offline"
        SERVICO_OFFLINE = "Serviço Offline", "Serviço Offline"
        EDUCACAO_OFFLINE = "Educação off-line", "Educação off-line"
        INTERMEDIACAO = "Intermediação de negócios", "Intermediação de negócios"
        NEGOCIO_SOCIAL = "Negócio social", "Negócio social"
        PUBLICIDADE = "Publicidade", "Publicidade"
        OUTROS = "Outros", "Outros"

    class revenue_model_choices(models.TextChoices):
        NAO_SEI = "Não sei", "Não sei"
        AFILIADOS = "Afiliados", "Afiliados"
        ANUNCIO = "Anúncio", "Anúncio"
        ASSINATURA = "Assinatura", "Assinatura"
        FREEMIUM = "Freemium", "Freemium"
        LICENCIAMENTO = "Licenciamento", "Licenciamento"
        INTERMEDIACAO = "Intermediação de Negócios", "Intermediação de Negócios"
        PAY_PER_USE = "Pay per Use", "Pay per Use"
        VENDA_HARDWARE = "Venda de Hardware ou produto físico", "Venda de Hardware ou produto físico"
        VENDA_DIRETA = "Venda Direta", "Venda Direta"
        TRANSACIONAL = "Transacional", "Transacional"
        OUTRO = "Outro", "Outro"

    class market_choices(models.TextChoices):
        AGRICULTURE_LIVESTOCK = "Agricultura e Pecuária", "Agricultura e Pecuária"
        FOOD_BEVERAGES = "Alimentos e Bebidas", "Alimentos e Bebidas"
        AUTOMOTIVE_MOBILITY = "Automotivo e Mobilidade", "Automotivo e Mobilidade"
        CAPITAL_INVESTMENTS = "Capital e Investimentos", "Capital e Investimentos"
        ECOMMERCE = "Comércio eletrônico", "Comércio eletrônico"
        COMMUNICATION_MEDIA = "Comunicação e Mídia", "Comunicação e Mídia"
        CONSTRUCTION_REAL_ESTATE = "Construção e Imóveis", "Construção e Imóveis"
        CREDIT_FINANCE = "Crédito e Finanças", "Crédito e Finanças"
        EDUCATION = "Educação", "Educação"
        ENERGY = "Energia", "Energia"
        SPORTS_LEISURE = "Esportes e Lazer", "Esportes e Lazer"
        MANAGEMENT_CONSULTING = "Gestão e Consultoria", "Gestão e Consultoria"
        GOVERNMENT_PUBLIC_SECTOR = "Governo e Poder Público", "Governo e Poder Público"
        HOSPITALITY_TOURISM = "Hotelaria e Turismo", "Hotelaria e Turismo"
        INDUSTRY_MANUFACTURING = "Indústria e Transformação", "Indústria e Transformação"
        GAMES_ENTERTAINMENT = "Jogos e Entretenimento", "Jogos e Entretenimento"
        LOGISTICS_TRANSPORT = "Logística e Transportes", "Logística e Transportes"
        FASHION_CLOTHING = "Moda e Vestuário", "Moda e Vestuário"
        ENGINES_EQUIPMENT = "Motores e Equipamentos", "Motores e Equipamentos"
        OIL_GAS = "Óleo e Gás", "Óleo e Gás"
        HEALTHCARE = "Saúde", "Saúde"
        WELLNESS = "Bem Estar", "Bem Estar"
        SECURITY_DEFENSE = "Segurança e Defesa", "Segurança e Defesa"
        INSURANCE = "Seguros", "Seguros"
        PROFESSIONAL_SERVICES = "Serviços profissionais", "Serviços profissionais"
        ENVIRONMENT = "Meio ambiente", "Meio ambiente"
        SUSTAINABILITY = "Sustentabilidade", "Sustentabilidade"
        INFORMATION_TECHNOLOGY = "Tecnologia da Informação", "Tecnologia da Informação"
        TELECOMMUNICATIONS = "Telecomunicações", "Telecomunicações"
        RETAIL_WHOLESALE = "Varejo e Atacado", "Varejo e Atacado"
        OTHER = "Outro", "Outro"


    class discovery_source_choices(models.TextChoices): #novo campo
        IMMERSION = 'Fui numa imersão do Programa', 'Fui numa imersão do Programa'
        CAMPUS_PARTY = 'Campus Party', 'Campus Party'
        INVESTE_NELAS_1 = 'Investe Nelas 1', 'Investe Nelas 1'
        INVESTE_NELAS_2 = 'Investe Nelas 2', 'Investe Nelas 2'
        EXPO_FAVELA_2023 = 'Expo Favela 2023', 'Expo Favela 2023'
        EXPO_FAVELA_2024 = 'Expo Favela 2024', 'Expo Favela 2024'
        GOOGLE_SEARCH = 'Achei no Google', 'Achei no Google'
        SOCIAL_MEDIA = 'Mídias Sociais', 'Mídias Sociais'
        REFERRAL = 'Indicação', 'Indicação'
        STARTUP_PIAUI_EVENT = 'Evento do Startup Piauí', 'Evento do Startup Piauí'
        OTHER = 'Outros', 'Outros'
    class maturity_stage_business_choices(models.TextChoices): #novo campo de negócio
        LOOKING_FOR_TEAM = 'Procurando Equipe', 'Procurando Equipe'
        IDEATION = 'Ideação (Modelando produto, sem MVP)', 'Ideação (Modelando produto, sem MVP)'
        MVP = 'MVP', 'MVP'
        INITIAL_TESTS = 'Primeiros testes (até 5 clientes)', 'Primeiros testes (até 5 clientes)'
        BETA_PHASE = 'Fase Beta de Negócio (menos que 20 clientes)', 'Fase Beta de Negócio (menos que 20 clientes)'
        MONETIZATION = 'Monetização (Faturamento > 10k, mais que 20 clientes, 1 recompra)', 'Monetização (Faturamento > 10k, mais que 20 clientes, 1 recompra)'
        CLIENT_CREATION = 'Criação de clientes (Faturamento > 30k em 3 meses)', 'Criação de clientes (Faturamento > 30k em 3 meses)'
        COMPANY_BUILDING = 'Construção de empresa (Faturamento > 1mi / 12 meses OU > 100k 3 meses OU investimento > 1mi)', 'Construção de empresa (Faturamento > 1mi / 12 meses OU > 100k 3 meses OU investimento > 1mi)'
        SCALE_UP = 'Scale Up', 'Scale Up'

    class cycle_choices(models.TextChoices):
        STARTUP_PIAUI_1 = "Startup Piaui 1", "Startup Piaui 1"
        STARTUP_PIAUI_2 = "Startup Piaui 2", "Startup Piaui 2"
        STARTUP_PIAUI_3 = "Startup Piaui 3", "Startup Piaui 3"
        STARTUP_PIAUI_4 = "Startup Piaui 4", "Startup Piaui 4"
        STARTUP_PIAUI_5 = "Startup Piaui 5", "Startup Piaui 5"
        STARTUP_PIAUI_6 = "Startup Piaui 6", "Startup Piaui 6"
        STARTUP_PIAUI_7 = "Startup Piaui 7", "Startup Piaui 7"
        BATALHA_DO_CONHECIMENTO_1 = "Batalha do Conhecimento 1", "Batalha do Conhecimento 1"
        MARATONA_DE_NEGOCIOS_1 = "Maratona de Negócios 1", "Maratona de Negócios 1"
        BATALHA_DE_STARTUPS_1 = "Batalha de Startups 1", "Batalha de Startups 1"
        INVESTE_NELAS_1 = "Investe Nelas 1", "Investe Nelas 1"
        INVESTE_NELAS_2 = "Investe Nelas 2", "Investe Nelas 2"
        EXPO_FAVELA_2024 = "Expo Favela 2024", "Expo Favela 2024"
        EXPO_FAVELA_2023 = "Expo Favela 2023", "Expo Favela 2023"

    class maturity_level_choices(models.TextChoices): #de produto
        TRL_0 = 'TRL 0 - Não iniciado', 'TRL 0 - Não iniciado'
        TRL_1 = 'TRL 1 - Princípios básicos observados e documentados', 'TRL 1 - Princípios básicos observados e documentados'
        TRL_2 = 'TRL 2 - Formulação do conceito da tecnologia', 'TRL 2 - Formulação do conceito da tecnologia'
        TRL_3 = 'TRL 3 - Prova de conceito experimental', 'TRL 3 - Prova de conceito experimental'
        TRL_4 = 'TRL 4 - Validação do conceito em laboratório', 'TRL 4 - Validação do conceito em laboratório'
        TRL_5 = 'TRL 5 - Validação do conceito em ambiente relevante', 'TRL 5 - Validação do conceito em ambiente relevante'
        TRL_6 = 'TRL 6 - Demonstração em ambiente relevante', 'TRL 6 - Demonstração em ambiente relevante'
        TRL_7 = 'TRL 7 - Demonstração em ambiente operacional', 'TRL 7 - Demonstração em ambiente operacional'
        TRL_8 = 'TRL 8 - Sistema completo e qualificado', 'TRL 8 - Sistema completo e qualificado'
        TRL_9 = 'TRL 9 - Sistema comprovado em ambiente operacional', 'TRL 9 - Sistema comprovado em ambiente operacional'
    cycle = models.CharField(
        max_length=50,
        choices=cycle_choices.choices,
        default=cycle_choices.STARTUP_PIAUI_1,
        help_text="Selecione o ciclo da sua startup",
    )    
    enterprise_id = models.AutoField(primary_key=True)
    initial_maturity = models.CharField(max_length=255,choices=maturity_stage_business_choices.choices, null=True, blank=True)# o choice foi trocado pelo de produto
    # Basic Information
    name = models.CharField(max_length=255, help_text="Digite o nome da sua startup")
    email = models.EmailField(max_length=500, null=True, blank=True, help_text="Principal email e ponto de contato")
    linkedin = models.URLField(max_length=500, null=True, blank=True, help_text="Digite o endereço completo do LinkedIn")
    instagram = models.URLField(max_length=500, null=True, blank=True, help_text="Digite o endereço completo do Instagram")
    whatsapp = models.CharField(max_length=20, null=True, blank=True, help_text="Digite o número do WhatsApp")
    website = models.URLField(max_length=500, null=True, blank=True, help_text="Digite o endereço do site da sua startup")
    summary = models.TextField(null=True, blank=True, help_text="Faça um breve resumo sobre sua empresa ou projeto")
    cnpj = models.CharField(max_length=20, null=True, blank=True, help_text="Informe o CNPJ caso sua empresa possua um")
    foundation_year = models.IntegerField(null=True, blank=True, help_text="Informe o ano em que sua startup foi fundada")
    city = models.CharField(max_length=255, null=True, blank=True, help_text="Informe a cidade")
    state = models.CharField(max_length=2,choices=state_choices.choices, null=True, blank=True, help_text="Selecione o estado")

    # Market and Product Information
    market = models.CharField(max_length=255,choices=market_choices.choices, null=True, blank=True, help_text="Selecione o mercado que sua startup atua")
    segment = models.CharField(max_length=255, null=True, blank=True, help_text="Escreva o mercado inicial da sua startup")
    problem = models.TextField(help_text="Descreva o problema que sua startup resolve")
    solution = models.TextField(help_text="Descreva brevemente a solução oferecida pela sua startup")
    client_type = models.CharField(max_length=255, null=True, blank=True, help_text="Selecione o tipo de cliente")
    product = models.CharField(max_length=500, help_text="Nos fale sobre seu produto e suas principais funcionalidades")
    product_stage = models.CharField(max_length=255, null=True,choices=maturity_level_choices.choices, blank=True, help_text="Selecione o estágio em que seu produto se encontra")

    # Strategy and Competitiveness
    value_proposition = models.TextField(help_text="Explique de forma breve os benefícios que sua startup oferece")
    competitive_differential = models.TextField(help_text="Descreva o benefício único oferecido ao cliente", default="Não especificado")
    competitors = models.TextField(help_text="Conte quem são seus principais competidores ou substitutivos")
    business_model = models.CharField(max_length=255,choices=BusinessModelChoices.choices, null=True, blank=True, help_text="Selecione o modelo de negócio")
    revenue_model = models.CharField(max_length=255,choices=revenue_model_choices.choices, null=True, blank=True, help_text="Selecione o modelo de receita")
    differential = models.TextField(null=True, blank=True, help_text="Diferencial competitivo da startup")

    # Investment Information
    invested = models.BooleanField(default=False, help_text="Informe se já recebeu investimento")
    investment_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Informe o valor total do investimento")
    boosting = models.BooleanField(default=False, help_text="Informe se recebeu fomento")
    funding_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Informe o valor recebido de fomento")
    funding_program = models.CharField(max_length=500, null=True, blank=True, help_text="Especifique o programa ou instituição de fomento")
    accelerated = models.BooleanField(default=False, help_text="Informe se já foi acelerada")
    accelerator_name = models.CharField(max_length=500, null=True, blank=True, help_text="Informe o nome da aceleradora")

    # Miscellaneous
    file = models.ImageField(upload_to='enterprise_files/', null=True, blank=True, help_text="Envie um arquivo relacionado à startup")
    other_projects = models.TextField(null=True, blank=True, help_text="Informe outros projetos do Programa Startup Piauí que você participa")
    profile_picture = models.URLField(max_length=255, null=True, blank=True)
    discovered_startup = models.CharField(max_length=255, choices=discovery_source_choices.choices, null=True, blank=True, help_text="Onde conheceu o programa?")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Data de criação do registro")

    def __str__(self):
        return f"{self.name} - {self.value_proposition[:30]}..."

class CompanyMetrics(models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name="metrics", help_text="Empresa associada às métricas")
    date_recorded = models.DateField(auto_now_add=True, help_text="Data de registro das métricas")
    created_time = models.TimeField(auto_now_add=True, help_text="Hora exata da criação do registro")
    team_size = models.IntegerField(help_text="Tamanho do time que não são sócios")
    revenue_period = models.DecimalField(max_digits=12, decimal_places=2, help_text="Receita durante o período")
    total_clients = models.IntegerField(help_text="Número total de clientes durante o período")
    new_clients = models.IntegerField(help_text="Número de novos clientes durante o período")
    investment_round_open = models.BooleanField(help_text="A empresa está com rodada de investimento aberta?")
    capital_needed = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        help_text="Necessidade de capital caso a rodada esteja aberta"
    )
    
    captable = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        help_text="Porcentagem de participação acionária (exemplo: 12.50 para 12,5%)"
    )
    value_foment = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    valuation = models.CharField(
        max_length=255, 
        help_text="Valor estimado do negócio (ou escreva NÃO SEI)"
    )
    current_capital = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        help_text="Capital atual da empresa"
    )

    def __str__(self):
        return f"Métricas de {self.enterprise.name}"


class Record(models.Model):
    class BusinessModelChoices(models.TextChoices):
        NAO_SEI = "Não sei", "Não sei"
        AFILIADOS = "Afiliados / Marketing de influência", "Afiliados / Marketing de influência"
        CONTEUDO_PREMIUM = "Conteúdo premium / Licenciamento de conteúdo / Educação on-line", "Conteúdo premium / Licenciamento de conteúdo / Educação on-line"
        COOPERATIVA = "Cooperativa", "Cooperativa"
        SOFTWARE_HOUSE = "Software house", "Software house"
        ECOMMERCE = "E-commerce", "E-commerce"
        MARKETPLACE = "Marketplace", "Marketplace"
        SAAS = "SAAS - Software como serviço", "SAAS - Software como serviço"
        HAAS = "HAAS - Hardware como serviço", "HAAS - Hardware como serviço"
        INDUSTRIA = "Indústria: Fabricação e venda direta online ou offline", "Indústria: Fabricação e venda direta online ou offline"
        EDUCACAO_ONLINE = "Educação on-line", "Educação on-line"
        COMERCIO_OFFLINE = "Comércio Offline", "Comércio Offline"
        SERVICO_OFFLINE = "Serviço Offline", "Serviço Offline"
        EDUCACAO_OFFLINE = "Educação off-line", "Educação off-line"
        INTERMEDIACAO = "Intermediação de negócios", "Intermediação de negócios"
        NEGOCIO_SOCIAL = "Negócio social", "Negócio social"
        PUBLICIDADE = "Publicidade", "Publicidade"
        OUTROS = "Outros", "Outros"

    class market_choices(models.TextChoices):
        AGRICULTURE_LIVESTOCK = "Agricultura e Pecuária", "Agricultura e Pecuária"
        FOOD_BEVERAGES = "Alimentos e Bebidas", "Alimentos e Bebidas"
        AUTOMOTIVE_MOBILITY = "Automotivo e Mobilidade", "Automotivo e Mobilidade"
        CAPITAL_INVESTMENTS = "Capital e Investimentos", "Capital e Investimentos"
        ECOMMERCE = "Comércio eletrônico", "Comércio eletrônico"
        COMMUNICATION_MEDIA = "Comunicação e Mídia", "Comunicação e Mídia"
        CONSTRUCTION_REAL_ESTATE = "Construção e Imóveis", "Construção e Imóveis"
        CREDIT_FINANCE = "Crédito e Finanças", "Crédito e Finanças"
        EDUCATION = "Educação", "Educação"
        ENERGY = "Energia", "Energia"
        SPORTS_LEISURE = "Esportes e Lazer", "Esportes e Lazer"
        MANAGEMENT_CONSULTING = "Gestão e Consultoria", "Gestão e Consultoria"
        GOVERNMENT_PUBLIC_SECTOR = "Governo e Poder Público", "Governo e Poder Público"
        HOSPITALITY_TOURISM = "Hotelaria e Turismo", "Hotelaria e Turismo"
        INDUSTRY_MANUFACTURING = "Indústria e Transformação", "Indústria e Transformação"
        GAMES_ENTERTAINMENT = "Jogos e Entretenimento", "Jogos e Entretenimento"
        LOGISTICS_TRANSPORT = "Logística e Transportes", "Logística e Transportes"
        FASHION_CLOTHING = "Moda e Vestuário", "Moda e Vestuário"
        ENGINES_EQUIPMENT = "Motores e Equipamentos", "Motores e Equipamentos"
        OIL_GAS = "Óleo e Gás", "Óleo e Gás"
        HEALTHCARE = "Saúde", "Saúde"
        WELLNESS = "Bem Estar", "Bem Estar"
        SECURITY_DEFENSE = "Segurança e Defesa", "Segurança e Defesa"
        INSURANCE = "Seguros", "Seguros"
        PROFESSIONAL_SERVICES = "Serviços profissionais", "Serviços profissionais"
        ENVIRONMENT = "Meio ambiente", "Meio ambiente"
        SUSTAINABILITY = "Sustentabilidade", "Sustentabilidade"
        INFORMATION_TECHNOLOGY = "Tecnologia da Informação", "Tecnologia da Informação"
        TELECOMMUNICATIONS = "Telecomunicações", "Telecomunicações"
        RETAIL_WHOLESALE = "Varejo e Atacado", "Varejo e Atacado"
        OTHER = "Outro", "Outro"

    class cycle_choices(models.TextChoices):
        STARTUP_PIAUI_1 = "Startup Piaui 1", "Startup Piaui 1"
        STARTUP_PIAUI_2 = "Startup Piaui 2", "Startup Piaui 2"
        STARTUP_PIAUI_3 = "Startup Piaui 3", "Startup Piaui 3"
        STARTUP_PIAUI_4 = "Startup Piaui 4", "Startup Piaui 4"
        STARTUP_PIAUI_5 = "Startup Piaui 5", "Startup Piaui 5"
        STARTUP_PIAUI_6 = "Startup Piaui 6", "Startup Piaui 6"
        STARTUP_PIAUI_7 = "Startup Piaui 7", "Startup Piaui 7"
        BATALHA_DO_CONHECIMENTO_1 = "Batalha do Conhecimento 1", "Batalha do Conhecimento 1"
        MARATONA_DE_NEGOCIOS_1 = "Maratona de Negócios 1", "Maratona de Negócios 1"
        BATALHA_DE_STARTUPS_1 = "Batalha de Startups 1", "Batalha de Startups 1"
        INVESTE_NELAS_1 = "Investe Nelas 1", "Investe Nelas 1"
        INVESTE_NELAS_2 = "Investe Nelas 2", "Investe Nelas 2"
        EXPO_FAVELA_2024 = "Expo Favela 2024", "Expo Favela 2024"
        EXPO_FAVELA_2023 = "Expo Favela 2023", "Expo Favela 2023"

    class record_type_choices(models.TextChoices):
        HOMEWORK = 'Dever de casa', 'Dever de casa'
        INTEL = 'Intel', 'Intel'
        RECEIVED_REQUEST = 'Recebemos pedido', 'Recebemos pedido'
        FOLLOW_UP = 'Follow', 'Follow'
        BOARD_MEETING = 'Reunião de Conselho', 'Reunião de Conselho'
        MONITORING_MEETING = 'Reunião de Acompanhamento', 'Reunião de Acompanhamento'

    class MITPhase(models.TextChoices):
        PHASE_1 = 'Fase 1', 'Fase 1'
        PHASE_2 = 'Fase 2', 'Fase 2'
        PHASE_3 = 'Fase 3', 'Fase 3'

    class maturity_level_choices(models.TextChoices):
        TRL_0 = 'TRL 0 - Não iniciado', 'TRL 0 - Não iniciado'
        TRL_1 = 'TRL 1 - Princípios básicos observados e documentados', 'TRL 1 - Princípios básicos observados e documentados'
        TRL_2 = 'TRL 2 - Formulação do conceito da tecnologia', 'TRL 2 - Formulação do conceito da tecnologia'
        TRL_3 = 'TRL 3 - Prova de conceito experimental', 'TRL 3 - Prova de conceito experimental'
        TRL_4 = 'TRL 4 - Validação do conceito em laboratório', 'TRL 4 - Validação do conceito em laboratório'
        TRL_5 = 'TRL 5 - Validação do conceito em ambiente relevante', 'TRL 5 - Validação do conceito em ambiente relevante'
        TRL_6 = 'TRL 6 - Demonstração em ambiente relevante', 'TRL 6 - Demonstração em ambiente relevante'
        TRL_7 = 'TRL 7 - Demonstração em ambiente operacional', 'TRL 7 - Demonstração em ambiente operacional'
        TRL_8 = 'TRL 8 - Sistema completo e qualificado', 'TRL 8 - Sistema completo e qualificado'
        TRL_9 = 'TRL 9 - Sistema comprovado em ambiente operacional', 'TRL 9 - Sistema comprovado em ambiente operacional'


    class business_level_choices(models.TextChoices):
        LOOKING_FOR_TEAM = 'Procurando Equipe', 'Procurando Equipe'
        IDEATION = 'Ideação', 'Ideação'
        MVP = 'MVP', 'MVP'
        TESTING = 'Primeiros Testes', 'Primeiros Testes'
        BETA_PHASE = 'Fase Beta', 'Fase Beta'
        MONETIZATION = 'Monetização', 'Monetização'
        CLIENT_CREATION = 'Criação de Clientes', 'Criação de Clientes'
        BUILDING_COMPANY = 'Construção de Empresa', 'Construção de Empresa'
        SCALE_UP = 'Scale Up', 'Scale Up'

    enterprise = models.ForeignKey(
        Enterprise, 
        on_delete=models.CASCADE, 
        related_name="records", 
        help_text="Empresa associada ao prontuário"
    )
    date_collected = models.DateField(help_text="Data de coleta dos dados")
    responsible_person = models.CharField(max_length=255, help_text="Nome do responsável pelo dado")
    data_type = models.CharField(max_length=255, choices=record_type_choices.choices, help_text="Tipo de dado")
    mit_phase = models.CharField(max_length=255, choices=MITPhase.choices, help_text="Fase do MIT")
    product_status = models.CharField(max_length=255, choices=maturity_level_choices.choices, help_text="Status do produto")
    initial_maturity = models.CharField(max_length=255, choices=business_level_choices.choices, help_text="Status do negócio")
    how_we_can_help = models.TextField(max_length=500, help_text="Como podemos ajudar?", blank=True, null=True)
    next_steps = models.TextField(max_length=500, help_text="Próximos passos", blank=True, null=True)
    next_meeting_date = models.DateField(help_text="Data da próxima agenda", blank=True, null=True)
    observations = models.TextField(max_length=500, help_text="Observações sobre a empresa", blank=True, null=True)
    market = models.CharField(max_length=255,choices=market_choices.choices, null=True, blank=True, help_text="Selecione o mercado que sua startup atua")
    business_model = models.CharField(max_length=255,choices=BusinessModelChoices.choices, null=True, blank=True, help_text="Selecione o modelo de negócio")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Data de criação do registro")

    cycle = models.CharField(
        max_length=50,
        choices=cycle_choices.choices,
        default=cycle_choices.STARTUP_PIAUI_1,
        help_text="Selecione o ciclo da sua startup",
    )  
    def __str__(self):
        return f"Prontuário da empresa {self.enterprise.name}"
