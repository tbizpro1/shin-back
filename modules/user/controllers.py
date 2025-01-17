from modules.user.models import User
from ninja_extra import api_controller, route
from modules.user.services import Services
from modules.user.schemas import UserListSchema, UserPostSchema, UserPutSchema, ErrorResponse,RegisterSchema, RegisterResponseSchema
from typing import List
from ninja import Form, File, UploadedFile
from modules.utils.permission.permissions import AdminPermission
from ninja.errors import HttpError

@api_controller(
    '/users',
    tags=['Rota - Usuários'],
)

class UsersController:
    
    services = Services
    
    @route.get('', response={200: List[UserListSchema]}, auth=None)
    def list(self, request):
        return self.services.list()
    
    @route.get('/{id}', response={200: UserListSchema})
    def get(self, request, id: int):
        return self.services.get(id=id)
    
    @route.post('', response={201: UserListSchema, 500: ErrorResponse}, auth=None)
    def post(self, request, payload: UserPostSchema = Form(...), profile_picture: UploadedFile = File(None)):
        # Converter o payload para dicionário
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

    @route.delete('/{id}', response={204: None})
    def delete(self, request, id: int):
        return self.services.delete(id=id)
    
    @route.post('picture/{id}', response={201: UserListSchema, 404: ErrorResponse, 500: ErrorResponse})
    def put_picture(self, request, id: int, profile_picture: UploadedFile = File(...)):
        print("essa é a file", profile_picture)

        print(f"reqeust: {request}")
        return self.services.put_picture(id=id, file=profile_picture)

    @route.post("/users/picture/")
    def test_upload(self, request, file: UploadedFile = File(...)):
        print("Arquivo recebido:", file)
        if file:
            print("Nome do arquivo:", file.name)
        return {"status": "sucesso"}

    