# from django.db import models
# from django.contrib.auth.models import AbstractUser

# class User(AbstractUser):
#     ROLE_CHOICES = (
#         ('admin', 'Admin'),
#         ('user', 'User'),
#     )
    
#     GENDER_CHOICES = (
#     ('m', 'Male'),
#     ('f', 'Female'),
#     ('n', 'Prefer not to say'),
#     )
#     class state_choices(models.TextChoices):
#         AC = "AC", "Acre"
#         AL = "AL", "Alagoas"
#         AP = "AP", "Amapá"
#         AM = "AM", "Amazonas"
#         BA = "BA", "Bahia"
#         CE = "CE", "Ceará"
#         DF = "DF", "Distrito Federal"
#         ES = "ES", "Espírito Santo"
#         GO = "GO", "Goiás"
#         MA = "MA", "Maranhão"
#         MT = "MT", "Mato Grosso"
#         MS = "MS", "Mato Grosso do Sul"
#         MG = "MG", "Minas Gerais"
#         PA = "PA", "Pará"
#         PB = "PB", "Paraíba"
#         PR = "PR", "Paraná"
#         PE = "PE", "Pernambuco"
#         PI = "PI", "Piauí"
#         RJ = "RJ", "Rio de Janeiro"
#         RN = "RN", "Rio Grande do Norte"
#         RS = "RS", "Rio Grande do Sul"
#         RO = "RO", "Rondônia"
#         RR = "RR", "Roraima"
#         SC = "SC", "Santa Catarina"
#         SP = "SP", "São Paulo"
#         SE = "SE", "Sergipe"
#         TO = "TO", "Tocantins"

#     class EducationLevelChoices(models.TextChoices):
#         SEM_ESCOLARIDADE = "Sem escolaridade", "Sem escolaridade"
#         ENSINO_FUNDAMENTAL = "Ensino Fundamental", "Ensino Fundamental"
#         ENSINO_MEDIO = "Ensino Médio", "Ensino Médio"
#         GRADUACAO = "Graduação", "Graduação"
#         ESPECIALIZACAO = "Especialização", "Especialização"
#         MESTRADO = "Mestrado", "Mestrado"
#         DOUTORADO = "Doutorado", "Doutorado"
#         POS_DOUTORADO = "Pós-Doutorado", "Pós-Doutorado"
    
#     class ethnicity_choices(models.TextChoices):
#         BRANCA = "Branca", "Branca"
#         PRETA = "Preta", "Preta"
#         PARDA = "Parda", "Parda"
#         AMARELA = "Amarela", "Amarela"
#         INDIGENA = "Indígena", "Indígena"

#     id = models.AutoField(primary_key=True)
#     username = models.CharField(max_length=50, unique=True)
#     email = models.EmailField(max_length=80, unique=True)
#     password = models.CharField(max_length=128)
#     phone = models.CharField(max_length=11, null=True, blank=True, default='')
#     linkedin = models.CharField(max_length=255, null=True, blank=True, default='')
#     profession = models.CharField(max_length=128, null=True, blank=True, default='')
#     date_joined = models.DateTimeField(auto_now_add=True)
#     last_login = models.DateTimeField(auto_now=True)
#     is_active = models.BooleanField(default=True)
#     role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='user', null=True, blank=True)
#     profile_picture = models.URLField(max_length=255, null=True, blank=True)
#     state = models.CharField(max_length=100,choices=state_choices.choices, null=True, blank=True)
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
#     institution = models.CharField(max_length=255, null=True, blank=True)
#     education_level = models.CharField(max_length=255,choices=EducationLevelChoices.choices, null=True, blank=True)
#     ethnicity = models.CharField(max_length=255,choices=ethnicity_choices.choices, null=True, blank=True)
#     city = models.CharField(max_length=100, null=True, blank=True)
#     whatsapp_number = models.CharField(max_length=15, null=True, blank=True, default='')
#     weekly_hours_worked = models.IntegerField(null=True, blank=True)
#     date_of_birth = models.DateField(null=True, blank=True)
#     country = models.CharField(max_length=100, null=True, blank=True)
#     cep = models.CharField(max_length=20, null=True, blank=True)
#     # street = models.CharField(max_length=255, null=True, blank=True)
#     # neighborhood = models.CharField(max_length=255, null=True, blank=True)
#     # number = models.CharField(max_length=10, null=True, blank=True)
#     cpf = models.CharField(max_length=14, unique=True, null=True, blank=True)  # Novo campo CPF

#     REQUIRED_FIELDS = ['username', 'password']
#     USERNAME_FIELD = 'email'

#     def __str__(self):
#         return f'{self.username} - {self.email}'
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    
    GENDER_CHOICES = (
    ('m', 'Male'),
    ('f', 'Female'),
    ('n', 'Prefer not to say'),
    )
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

    class EducationLevelChoices(models.TextChoices):
        SEM_ESCOLARIDADE = "Sem escolaridade", "Sem escolaridade"
        ENSINO_FUNDAMENTAL = "Ensino Fundamental", "Ensino Fundamental"
        ENSINO_MEDIO = "Ensino Médio", "Ensino Médio"
        GRADUACAO = "Graduação", "Graduação"
        ESPECIALIZACAO = "Especialização", "Especialização"
        MESTRADO = "Mestrado", "Mestrado"
        DOUTORADO = "Doutorado", "Doutorado"
        POS_DOUTORADO = "Pós-Doutorado", "Pós-Doutorado"
    
    class ethnicity_choices(models.TextChoices):
        BRANCA = "Branca", "Branca"
        PRETA = "Preta", "Preta"
        PARDA = "Parda", "Parda"
        AMARELA = "Amarela", "Amarela"
        INDIGENA = "Indígena", "Indígena"

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=80, unique=True)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=11, null=True, blank=True, default='')
    linkedin = models.CharField(max_length=255, null=True, blank=True, default='')
    profession = models.CharField(max_length=128, null=True, blank=True, default='')
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=50,choices=ROLE_CHOICES,  default='user', null=True, blank=True)
    profile_picture = models.URLField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)#choices=state_choices.choices,
    gender = models.CharField(max_length=1, null=True, blank=True)# choices=GENDER_CHOICES,
    institution = models.CharField(max_length=255, null=True, blank=True)
    education_level = models.CharField(max_length=255, null=True, blank=True)#choices=EducationLevelChoices.choices,
    ethnicity = models.CharField(max_length=255, null=True, blank=True)#choices=ethnicity_choices.choices,
    city = models.CharField(max_length=100, null=True, blank=True)
    whatsapp_number = models.CharField(max_length=15, null=True, blank=True, default='')
    # weekly_hours_worked = models.IntegerField(null=True, blank=True, default=0)
    # date_of_birth = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    cep = models.CharField(max_length=20, null=True, blank=True)
    # street = models.CharField(max_length=255, null=True, blank=True)
    # neighborhood = models.CharField(max_length=255, null=True, blank=True)
    # number = models.CharField(max_length=10, null=True, blank=True)
    cpf = models.CharField(max_length=14, null=True, blank=True)  # Novo campo CPF

    REQUIRED_FIELDS = ['username', 'password']
    USERNAME_FIELD = 'email'

    def __str__(self):
        return f'{self.username} - {self.email}'
