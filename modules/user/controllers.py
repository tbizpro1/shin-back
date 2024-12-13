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
        
        return self.services.post(payload=payload.dict(), file=profile_picture)
    
    @route.put('/{id}', response={201: UserListSchema, 400: ErrorResponse, 500: ErrorResponse})
    def put(self, request, id: int, payload: UserPutSchema = Form(...)):
        return self.services.put(id=id, payload=payload.dict())
    
    @route.delete('/{id}', response={204: None})
    def delete(self, request, id: int):
        return self.services.delete(id=id)
    
    @route.put('picture/{id}', response={201: UserListSchema, 404: ErrorResponse, 500: ErrorResponse})
    def put_picture(self, request, id: int, profile_picture: UploadedFile = File(...)):
        return self.services.put_picture(id=id, file=profile_picture)

    @route.post('/user-register', response={201: RegisterResponseSchema, 400: ErrorResponse}, auth=None)
    def register(self, request, payload: RegisterSchema = Form(...)):
        try:
            # Hashing a senha
            payload.password = self.services.repository.password_hash(payload.password)
            
            # Criando o usuário
            user = self.services.repository.model.objects.create(
                username=payload.username,
                email=payload.email,
                password=payload.password,
                role=payload.role
            )
            return 201, RegisterResponseSchema(
                id=user.id,
                username=user.username,
                email=user.email
            )
        except Exception as e:
            raise HttpError(400, f"Error during user registration: {str(e)}")