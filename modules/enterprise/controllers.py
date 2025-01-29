from modules.enterprise.models import Enterprise
from ninja_extra import api_controller, route
from modules.enterprise.services import EnterpriseServices,CompanyMetricsServices
from modules.enterprise.schemas import (
    EnterpriseListSchema,
    EnterprisePostSchema,
    EnterprisePutSchema,
    ErrorResponse,
    CompanyMetricsFilterSchema,
    CompanyMetricsListSchema,
    CompanyMetricsGetSchema
)
import requests
from modules.user_enterprise.repository import UserEnterpriseRepository
from typing import List
from ninja import Form, File, UploadedFile,Query
from ..logs.services import LogService


@api_controller(
    '/enterprises',
    tags=['Rota - Empresas'],
)
class EnterpriseController:
    """
    Controller para gerenciar operações relacionadas ao modelo Enterprise.
    """

    services = EnterpriseServices
    log_service = LogService()  # Instância do LogService

    @route.get('', response={200: List[EnterpriseListSchema]})
    def list(self, request):
        """
        Retorna a lista de empresas cadastradas.
        """
        user_id = request.user.id
        print('user_id', user_id)
        result = self.services.list()
        self.log_service.create_log(
            user_id=user_id, 
            change_type="read", 
            description="Você listou todas as empresas cadastras no sistema."
        )
        return result

    @route.get('/{id}', response={200: EnterpriseListSchema, 404: ErrorResponse})
    def get(self, request, id: int):
        """
        Retorna os detalhes de uma empresa pelo ID.
        """
        user_id = request.user.id
        result = self.services.get(id=id)
        self.log_service.create_log(
            user_id=user_id, 
            change_type="read", 
            description="Você visualizou os detalhes de uma empresa."
        )

        return result

    @route.post('', response={201: EnterpriseListSchema, 500: ErrorResponse})
    def post(
        self, 
        request, 
        payload: EnterprisePostSchema = Form(...), 
        file: UploadedFile = File(None)
    ):
        """
        Cria uma nova empresa e associa o usuário a ela.
        """
        user_id = request.user.id
        status_code, created_enterprise = self.services.post(payload=payload.dict(), file=file)
        enterprise_id = created_enterprise.enterprise_id

        UserEnterpriseRepository.post(
            payload={
                'user_id': user_id,
                'enterprise_id': enterprise_id,
                'role': 'owner',
                'status': 'accepted',
            }
        )

        self.log_service.create_log(
            user_id=user_id, 
            change_type="create", 
            description="Você criou uma nova empresa."
        )
        return 201, created_enterprise

    @route.put('/{id}', response={200: EnterpriseListSchema, 400: ErrorResponse, 500: ErrorResponse})
    def put(self, request, id: int, payload: EnterprisePutSchema):
        """
        Atualiza os dados de uma empresa existente.
        """
        user_id = request.user.id
        updated_enterprise = self.services.put(id=id, payload=payload.dict())
        self.log_service.create_log(
            user_id=user_id, 
            change_type="update", 
            description="Você atualizou os dados de uma empresa."
        )
        return updated_enterprise

    @route.delete('/{id}', response={204: None})
    def delete(self, request, id: int):
        """
        Deleta uma empresa pelo ID.
        """
        user_id = request.user.id
        self.services.delete(id=id)
        self.log_service.create_log(
            user_id=user_id, 
            change_type="delete", 
            description="Você deletou uma empresa."
        )
        return 204, None

    @route.post('file/{id}', response={200: EnterpriseListSchema, 404: ErrorResponse, 500: ErrorResponse})
    def upload_file(self, request, id: int, file: UploadedFile = File(...)):
        """
        Atualiza o arquivo associado à empresa.
        """
        user_id = request.user.id
        updated_file = self.services.upload_file(id=id, file=file)
        self.log_service.create_log(
           user_id=user_id, 
            change_type="update", 
            description="Você atualizou a foto de uma empresa."
        )
        return updated_file

    @route.get('tokenrd/')
    def checkToken(self, request):
        """
        Atualiza o arquivo associado à empresa.
        """
        url = "https://crm.rdstation.com/api/v1/token/check?token=6762e9a8ccd3ee001af5dc23"
        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)

        print(f"resposta{response.text}resposta")
        
@api_controller(
    '/company-metrics',
    tags=['Rota - Metricas Economicas da Empresa'],
)
class CompanyMetricsController:
    """
    Controller para gerenciar operações relacionadas ao modelo Enterprise.
    """

    services = CompanyMetricsServices
   # Instância do LogService

    @route.get('/', response={200:List[CompanyMetricsGetSchema]},)
    def list(self, request,filters: CompanyMetricsFilterSchema = Query(...)):
        """

        """
        queryset = self.services.list(filters=filters.dict(exclude_none=True))
        return list(queryset)
        
