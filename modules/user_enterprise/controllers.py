from ninja_extra import api_controller, route
from typing import List
from modules.user_enterprise.repository import UserEnterpriseRepository
from modules.user_enterprise.schemas import (
    UserEnterpriseListSchema,
    UserEnterprisePostSchema,
    UserEnterprisePutSchema,
    ErrorResponse,
)
from datetime import datetime
from django.http import Http404
from modules.user_enterprise.models import UserEnterprise
from ninja import Schema
from typing import List, Optional
from pydantic import Field
from ninja import Query

class Filters(Schema):
    limit: int = 100  
    offset: Optional[int] = None  
    username: Optional[str] = None 
    status: Optional[str] = None  #
    enterprise_name__in: Optional[List[str]] = Field(None, alias="enterprise_names") 


@api_controller(
    '/user-enterprises',
    tags=['Rota - User Enterprises']
)
class UserEnterpriseController:
  

    repository = UserEnterpriseRepository

    @route.get('', response={200: List[UserEnterpriseListSchema]}, auth=None)
    def list(self, request, filters: Query[Filters]):
        """
        Lista as relações UserEnterprise com filtros opcionais.

        ### Como o front deve fazer a requisição:
        **Endpoint:** `/user-enterprises`

        **Método:** `GET`

        **Parâmetros de Consulta (Query Params):**
        - `limit` (int, padrão: 100): Número máximo de registros retornados.
        - `offset` (int, opcional): Número de registros para pular no início.
        - `username` (str, opcional): Nome de usuário para filtrar.
        - `status` (str, opcional): Status para filtrar (exemplo: `active`, `pending`).
        - `enterprise_names` (list[str], opcional): Lista de nomes de empresas para filtrar.

        **Exemplo de Requisição:**
        ```http
        GET /user-enterprises?limit=10&offset=5&username=johndoe&status=active&enterprise_names=Google,Microsoft
        ```

        **Exemplo de Resposta (200):**
        ```json
        [
            {
                "ue_id": 1,
                "user_id": 101,
                "username": "johndoe",
                "enterprise_id": 201,
                "enterprise_name": "Google",
                "role": "admin",
                "status": "active",
                "token": "abc123"
            },
            {
                "ue_id": 2,
                "user_id": 102,
                "username": "janedoe",
                "enterprise_id": 202,
                "enterprise_name": "Microsoft",
                "role": "editor",
                "status": "active",
                "token": "xyz456"
            }
        ]
        ```
        """
        user_enterprises = self.repository.list()

        if filters.username:
            user_enterprises = [
                ue for ue in user_enterprises if ue.user.username == filters.username
            ]

        if filters.status:
            user_enterprises = [
                ue for ue in user_enterprises if ue.status == filters.status
            ]

        if filters.enterprise_name__in:
            user_enterprises = [
                ue for ue in user_enterprises if ue.enterprise.name in filters.enterprise_name__in
            ]

        if filters.offset is not None:
            user_enterprises = user_enterprises[filters.offset:]

        user_enterprises = user_enterprises[:filters.limit]

        return [
            {
                "ue_id": ue.ue_id,
                "user_id": ue.user.id,
                "username": ue.user.username,
                "enterprise_id": ue.enterprise.enterprise_id,
                "enterprise_name": ue.enterprise.name,
                "role": ue.role,
                "status": ue.status,
                "token": ue.token,
            }
            for ue in user_enterprises
        ]

    @route.get('/{id}', response={200: UserEnterpriseListSchema, 404: ErrorResponse})
    def get(self, request, id: int):
     
        user_enterprise = self.repository.get(id=id)
        return {
            "ue_id": user_enterprise.ue_id,
            "user_id": user_enterprise.user.id,
            "username": user_enterprise.user.username,
            "enterprise_id": user_enterprise.enterprise.enterprise_id,
            "enterprise_name": user_enterprise.enterprise.name,
            "role": user_enterprise.role,
            "status": user_enterprise.status,
        }

    @route.post('', response={200: UserEnterpriseListSchema, 500: ErrorResponse})
    def post(self, request, payload: UserEnterprisePostSchema):
        """
        Cria uma nova relação UserEnterprise.
        """
        user_enterprise = self.repository.post(payload=payload.dict())
        return {
            "ue_id": user_enterprise.ue_id,
            "user_id": user_enterprise.user.id,
            "username": user_enterprise.user.username,
            "enterprise_id": user_enterprise.enterprise.enterprise_id,
            "enterprise_name": user_enterprise.enterprise.name,
            "role": user_enterprise.role,
            "status": user_enterprise.status,
        }

    @route.put('/{id}', response={200: UserEnterpriseListSchema, 400: ErrorResponse, 500: ErrorResponse})
    def put(self, request, id: int, payload: UserEnterprisePutSchema):
        """
        Atualiza os dados de uma relação UserEnterprise existente.
        """
        user_enterprise = self.repository.put(id=id, payload=payload.dict(exclude_unset=True))
        return {
            "ue_id": user_enterprise.ue_id,
            "user_id": user_enterprise.user.id,
            "username": user_enterprise.user.username,
            "enterprise_id": user_enterprise.enterprise.enterprise_id,
            "enterprise_name": user_enterprise.enterprise.name,
            "role": user_enterprise.role,
            "status": user_enterprise.status,
        }

    @route.put('/invitation/{token}/', response={200: UserEnterpriseListSchema, 404: ErrorResponse}, auth=None)
    def accept(self, request, token: str, status: str):
            """
            Endpoint to accept or decline an invitation using a unique token.
            """
            if status not in ["accepted", "declined"]:
                return 404, {"message": "Invalid status. Choose 'accepted' or 'declined'."}

            try:
                invitation = UserEnterprise.objects.get(token=token)
            except UserEnterprise.DoesNotExist:
                raise Http404("Invitation not found.")

            if invitation.status != "pending":
                return 404, {"message": "Invitation has already been handled."}

            invitation.status = status
            if status == "accepted":
                invitation.accept_at = datetime.now()
            invitation.save()

            return {
                "ue_id": invitation.ue_id,
                "user_id": invitation.user.id,
                "username": invitation.user.username,
                "enterprise_id": invitation.enterprise.enterprise_id,
                "enterprise_name": invitation.enterprise.name,
                "role": invitation.role,
                "status": invitation.status,
                "token": invitation.token,
            }


        

    @route.delete('/{id}', response={204: None})
    def delete(self, request, id: int):
        """
        Deleta uma relação UserEnterprise pelo ID.
        """
        self.repository.delete(id=id)
        return None

    @route.get('/user/{user_id}', response={200: List[UserEnterpriseListSchema]}, auth=None)
    def list_by_user(self, request, user_id: int):
        """
        Retorna todas as relações UserEnterprise associadas a um usuário específico.
        """
        user_enterprises = self.repository.list_by_user(user_id=user_id)
        return [
            {
                "ue_id": ue.ue_id,
                "user_id": ue.user.id,
                "username": ue.user.username,
                "enterprise_id": ue.enterprise.enterprise_id,
                "enterprise_name": ue.enterprise.name,
                "role": ue.role,
                "token": ue.token,
                "status": ue.status,
            }
            for ue in user_enterprises
        ]

    @route.get('/enterprise/{enterprise_id}', response={200: List[UserEnterpriseListSchema]}, auth=None)
    def list_by_enterprise(self, request, enterprise_id: int):
        """
        Retorna todas as relações UserEnterprise associadas a uma empresa específica.
        """
        user_enterprises = self.repository.list_by_enterprise(enterprise_id=enterprise_id)
        return [
            {
                "ue_id": ue.ue_id,
                "user_id": ue.user.id,
                "username": ue.user.username,
                "enterprise_id": ue.enterprise.enterprise_id,
                "enterprise_name": ue.enterprise.name,
                "role": ue.role,
                "status": ue.status,
            }
            for ue in user_enterprises
        ]
