from modules.user.models import User
from ninja_extra import api_controller, route
from modules.user.services import Services
from modules.user.schemas import UserListSchema, UserPostSchema, UserPutSchema, ErrorResponse, ErrorResponse
from typing import List, Dict
from ninja import Form, File, UploadedFile
from modules.utils.permission.permissions import AdminPermission
from ninja.errors import HttpError

@api_controller(
    '/users',
    tags=['Rota - Usuários'],
)

class UsersController:
    
    services = Services
    
    @route.get('', response={200: List[UserListSchema]})
    def list(self, request):
        return self.services.list()
    
    @route.get('/{id}', response={200: UserListSchema})
    def get(self, request, id: int):
        return self.services.get(id=id)
    
    @route.post('', response={201: UserListSchema, 500: ErrorResponse},auth=None)
    def post(self, request, payload: UserPostSchema = Form(...), profile_picture: UploadedFile = File(None)):
        """
        Criação de usuários.
        Essa rota permite a criação de usuários com dados pessoais e profissionais.

        - **username**: Nome de usuário.
        - **email**: Endereço de e-mail.
        - **password**: Senha do usuário.
        - **phone**: (Opcional) Telefone de contato.
        - **linkedin**: (Opcional) Perfil do LinkedIn.
        - **profession**: (Opcional) Profissão do usuário.
        - **role**: Função do usuário (admin ou usuário regular).
        - **state**: (Opcional) Estado de residência.
        - **gender**: (Opcional) Gênero do usuário.
        - **institution**: (Opcional) Instituição de trabalho ou estudo.
        - **education_level**: (Opcional) Nível de educação.
        - **ethnicity**: (Opcional) Etnia.
        - **city**: (Opcional) Cidade de residência.
        - **whatsapp_number**: (Opcional) Número do WhatsApp.
        - **weekly_hours_worked**: (Opcional) Horas semanais de trabalho.
        - **date_of_birth**: (Opcional) Data de nascimento.
        - **country**: (Opcional) País de residência.
        - **cep**: (Opcional) Código postal.
        - **cpf**: (Opcional) CPF do usuário.

        Arquivo opcional:
        - **file**: Um arquivo opcional que pode ser associado ao usuário.
        {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "password": "StrongPassword123",
        "phone": "+5511998765432",
        "linkedin": "https://www.linkedin.com/in/johndoe",
        "profession": "Software Engineer",
        "role": "user",
        "state": "São Paulo",
        "gender": "male",
        "institution": "Universidade de São Paulo",
        "education_level": "Mestrado",
        "ethnicity": "Branco",
        "city": "São Paulo",
        "whatsapp_number": "+5511998765432",
        "weekly_hours_worked": 40,
        "date_of_birth": "1990-01-15",
        "country": "Brasil",
        "cep": "01001-000",
        "cpf": "123.456.789-09"
        }
        Retornos:
        - **201**: Usuário criado com sucesso.
        - **400**: Erro de validação no payload.
        """
        schema_dict = payload.dict()

        # Iterar sobre os itens do dicionário
        for key, value in schema_dict.items():
            if isinstance(value, str) and len(value) > 100:
                print(f"Campo {key} tem {len(value)} caracteres: {value}")

    # Passar o dicionário para o serviço
        return self.services.post(payload=schema_dict, file=profile_picture)
    @route.put('/{id}', response={200: UserListSchema, 400: ErrorResponse, 500: ErrorResponse})
    def put(self, request, id: int, payload: UserPutSchema):
        print(f"Payload recebido no controlador: {payload.dict()}")
        return self.services.put(id=id, payload=payload.dict())

    @route.delete('/{id}',  response= {200: Dict[str, str], 404: ErrorResponse, 500: ErrorResponse})
    def delete(self, request, id: int):
        return self.services.delete(id=id)
    
    @route.post('picture/{id}', response={201: UserListSchema, 404: ErrorResponse, 500: ErrorResponse})
    def put_picture(self, request, id: int, profile_picture: UploadedFile = File(...)):
        print("essa é a file", profile_picture)

        print(f"reqeust: {request}")
        return self.services.put_picture(id=id, file=profile_picture)


    