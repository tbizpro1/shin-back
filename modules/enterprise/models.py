from django.db import models

class Enterprise(models.Model):

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
        
    enterprise_id = models.AutoField(primary_key=True)
    initial_maturity = models.CharField(max_length=255,choices=maturity_level_choices.choices, null=True, blank=True)
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
    state = models.CharField(max_length=2, null=True, blank=True, help_text="Selecione o estado")

    # Market and Product Information
    market = models.CharField(max_length=255, null=True, blank=True, help_text="Selecione o mercado que sua startup atua")
    segment = models.CharField(max_length=255, null=True, blank=True, help_text="Escreva o mercado inicial da sua startup")
    problem = models.TextField(help_text="Descreva o problema que sua startup resolve")
    solution = models.TextField(help_text="Descreva brevemente a solução oferecida pela sua startup")
    client_type = models.CharField(max_length=255, null=True, blank=True, help_text="Selecione o tipo de cliente")
    product = models.CharField(max_length=500, help_text="Nos fale sobre seu produto e suas principais funcionalidades")
    product_stage = models.CharField(max_length=255, null=True, blank=True, help_text="Selecione o estágio em que seu produto se encontra")

    # Strategy and Competitiveness
    value_proposition = models.TextField(help_text="Explique de forma breve os benefícios que sua startup oferece")
    competitive_differential = models.TextField(help_text="Descreva o benefício único oferecido ao cliente", default="Não especificado")
    competitors = models.TextField(help_text="Conte quem são seus principais competidores ou substitutivos")
    business_model = models.CharField(max_length=255, null=True, blank=True, help_text="Selecione o modelo de negócio")
    revenue_model = models.CharField(max_length=255, null=True, blank=True, help_text="Selecione o modelo de receita")
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
    discovered_startup = models.CharField(max_length=255, null=True, blank=True, help_text="Onde conheceu o Programa Startup Piauí")
    other_projects = models.TextField(null=True, blank=True, help_text="Informe outros projetos do Programa Startup Piauí que você participa")
    profile_picture = models.URLField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.value_proposition[:30]}..."

class CompanyMetrics(models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name="metrics", help_text="Empresa associada às métricas")
    date_recorded = models.DateField(auto_now_add=True, help_text="Data de registro das métricas")
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
    
    value_invested = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    value_foment = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    valuation = models.CharField(
        max_length=255, 
        help_text="Valor estimado do negócio (ou escreva NÃO SEI)"
    )

    def __str__(self):
        return f"Métricas de {self.enterprise.name}"


class Record(models.Model):
    class MITPhase(models.TextChoices):
        PHASE_1 = 'Fase 1', 'Fase 1'
        PHASE_2 = 'Fase 2', 'Fase 2'
        PHASE_3 = 'Fase 3', 'Fase 3'

    class TRL(models.TextChoices):
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

    class ProductStatus(models.TextChoices):
        NOT_STARTED = 'Não Iniciado', 'Não Iniciado'
        IN_DEVELOPMENT = 'Em Desenvolvimento', 'Em Desenvolvimento'
        COMPLETED = 'Finalizado', 'Finalizado'

    class BusinessStatus(models.TextChoices):
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
    responsible = models.CharField(max_length=255, help_text="Responsável pelo dado")
    data_type = models.CharField(max_length=255, choices=TRL.choices, help_text="Tipo de dado")
    mit_phase = models.CharField(max_length=255, choices=MITPhase.choices, help_text="Fase do MIT")
    product_status = models.CharField(max_length=255, choices=ProductStatus.choices, help_text="Status do produto")
    business_status = models.CharField(max_length=255, choices=BusinessStatus.choices, help_text="Status do negócio")
    how_we_can_help = models.TextField(max_length=500, help_text="Como podemos ajudar?", blank=True, null=True)
    next_steps = models.TextField(max_length=500, help_text="Próximos passos", blank=True, null=True)
    next_meeting_date = models.DateField(help_text="Data da próxima agenda", blank=True, null=True)
    observations = models.TextField(max_length=500, help_text="Observações sobre a empresa", blank=True, null=True)

    def __str__(self):
        return f"Prontuário da empresa {self.enterprise.name}"
