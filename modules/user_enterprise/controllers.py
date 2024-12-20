from ninja_extra import api_controller, route
from typing import List
from modules.user_enterprise.repository import UserEnterpriseRepository
from modules.user_enterprise.schemas import (
    UserEnterpriseListSchema,
    UserEnterprisePostSchema,
    UserEnterprisePutSchema,
    ErrorResponse,
)
from modules.user_enterprise.models import UserEnterprise

@api_controller(
    '/user-enterprises',
    tags=['Rota - User Enterprises']
)
class UserEnterpriseController:
    """
    Controller para gerenciar operações relacionadas ao modelo UserEnterprise.
    """

    repository = UserEnterpriseRepository

    @route.get('', response={200: List[UserEnterpriseListSchema]}, auth=None)
    def list(self, request):
        """
        Retorna a lista de relações UserEnterprise cadastradas.
        """
        user_enterprises = self.repository.list()
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

    @route.get('/{id}', response={200: UserEnterpriseListSchema, 404: ErrorResponse})
    def get(self, request, id: int):
        """
        Retorna os detalhes de uma relação UserEnterprise pelo ID.
        """
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

    @route.post('', response={200: UserEnterpriseListSchema, 500: ErrorResponse}, auth=None)
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

    @route.put('/accept/{id}', response={200: UserEnterpriseListSchema, 404: ErrorResponse})
    def accept(self, request, id: int):
        """
        Aceita um convite, atualizando o status para 'accepted'.
        """
        user_enterprise = self.repository.get(id=id)
        if user_enterprise.status != 'pending':
            return {"message": "Convite já foi aceito ou recusado."}, 400
        user_enterprise.status = 'accepted'
        user_enterprise.save()
        return {
            "ue_id": user_enterprise.ue_id,
            "user_id": user_enterprise.user.id,
            "username": user_enterprise.user.username,
            "enterprise_id": user_enterprise.enterprise.enterprise_id,
            "enterprise_name": user_enterprise.enterprise.name,
            "role": user_enterprise.role,
            "status": user_enterprise.status,
        }

    @route.put('/decline/{id}', response={200: UserEnterpriseListSchema, 404: ErrorResponse})
    def decline(self, request, id: int):
        """
        Recusa um convite, atualizando o status para 'declined'.
        """
        user_enterprise = self.repository.get(id=id)
        if user_enterprise.status != 'pending':
            return {"message": "Convite já foi aceito ou recusado."}, 400
        user_enterprise.status = 'declined'
        user_enterprise.save()
        return {
            "ue_id": user_enterprise.ue_id,
            "user_id": user_enterprise.user.id,
            "username": user_enterprise.user.username,
            "enterprise_id": user_enterprise.enterprise.enterprise_id,
            "enterprise_name": user_enterprise.enterprise.name,
            "role": user_enterprise.role,
            "status": user_enterprise.status,
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
