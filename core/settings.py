from pathlib import Path
import environ
import os

ENVIRONMENT = os.getenv('DJANGO_ENV', 'local')
print(f"ENVIRONMENT: {ENVIRONMENT}")

env = environ.Env()
if ENVIRONMENT == 'production':
    environ.Env.read_env('.env.production')
else:
    environ.Env.read_env('.env.local')

BASE_DIR = Path(__file__).resolve().parent.parent

env_file = os.path.join(BASE_DIR, '.env.local')
if os.path.exists(env_file):
    print(f"Carregando variáveis de ambiente de {env_file}")
    environ.Env.read_env(env_file)
else:
    print(f"Arquivo {env_file} não encontrado")

# Security
SECRET_KEY = env('SECRET_KEY')  # Substitua em produção
DEBUG = env.bool('DEBUG', default=False) 
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["127.0.0.1", "localhost"])

# Applications
AUTH_USER_MODEL = 'user.User'  # Substitua pelo nome do seu app e modelo

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'ninja',
    'ninja_extra',
    'ninja_jwt',
    'django_extensions', 

]

LOCAL_APPS= [
    'core',
    'modules.user',
    'modules.token',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# URL Configuration
ROOT_URLCONF = 'core.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Adicione diretórios de templates personalizados se necessário
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI
WSGI_APPLICATION = 'core.wsgi.application'

# Database
DATABASES = {
        'default': env.db('DATABASE_URL', default=f'sqlite:///{BASE_DIR}/db.sqlite3'),
}

# Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Localization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Static Files
STATIC_URL = 'static/'

# Diretório onde os arquivos estáticos serão coletados
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Diretórios adicionais de arquivos estáticos (se necessário)
if ENVIRONMENT == 'production':
    STATICFILES_DIRS = []
else:
    STATICFILES_DIRS = [
        BASE_DIR / 'static',
    ]

# Primary Key Field Type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
