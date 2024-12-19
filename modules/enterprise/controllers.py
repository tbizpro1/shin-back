from modules.enterprise.models import Enterprise
from ninja_extra import api_controller, route
from modules.enterprise.services import EnterpriseServices
from modules.enterprise.schemas import (
    EnterpriseListSchema,
    EnterprisePostSchema,
    EnterprisePutSchema,
    ErrorResponse,
)
from typing import List
from ninja import Form, File, UploadedFile

@api_controller(
    '/enterprises',
    tags=['Rota - Empresas'],
)
class EnterpriseController:
    """
    Controller para gerenciar operações relacionadas ao modelo Enterprise.
    """

    services = EnterpriseServices

    @route.get('', response={200: List[EnterpriseListSchema]}, auth=None)
    def list(self, request):
        """
        Retorna a lista de empresas cadastradas.
        """
        return self.services.list()

    @route.get('/{id}', response={200: EnterpriseListSchema, 404: ErrorResponse})
    def get(self, request, id: int):
        """
        Retorna os detalhes de uma empresa pelo ID.
        """
        return self.services.get(id=id)

    @route.post('', response={201: EnterpriseListSchema, 500: ErrorResponse}, auth=None)
    def post(
        self, 
        request, 
        payload: EnterprisePostSchema = Form(...), 
        file: UploadedFile = File(None)
    ):
        """
        Cria uma nova empresa.
        """
        return self.services.post(payload=payload.dict(), file=file)

    @route.put('/{id}', response={200: EnterpriseListSchema, 400: ErrorResponse, 500: ErrorResponse})
    def put(self, request, id: int, payload: EnterprisePutSchema = Form(...)):
        """
        Atualiza os dados de uma empresa existente.
        """
        return self.services.put(id=id, payload=payload.dict())

    @route.delete('/{id}', response={204: None})
    def delete(self, request, id: int):
        """
        Deleta uma empresa pelo ID.
        """
        return self.services.delete(id=id)

    @route.put('file/{id}', response={200: EnterpriseListSchema, 404: ErrorResponse, 500: ErrorResponse})
    def upload_file(self, request, id: int, file: UploadedFile = File(...)):
        """
        Atualiza o arquivo associado à empresa.
        """
        return self.services.upload_file(id=id, file=file)
