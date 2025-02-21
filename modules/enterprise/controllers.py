from modules.enterprise.models import Enterprise
from ninja_extra import api_controller, route
from modules.enterprise.services import EnterpriseServices,CompanyMetricsServices, RecordServices
from modules.enterprise.schemas import (
    EnterpriseListSchema,
    EnterprisePostSchema,
    EnterprisePutSchema,
    ErrorResponse,
    CompanyMetricsFilterSchema,
    CompanyMetricsListSchema,
    CompanyMetricsPostSchema,
    CompanyMetricsGetSchema,
    RecordInSchema,
    RecordOutSchema,
    RecordFilterSchema,
    RecordPutSchema,
    CompanyMetricsPutSchema
)
import requests
from modules.user_enterprise.repository import UserEnterpriseRepository
from typing import List, Dict,Any, Union
from ninja import Form, File, UploadedFile,Query,Body
from ..logs.services import LogService
from django.http import JsonResponse
from django.db.models.query import QuerySet


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

    @route.get('', response={200: List[EnterpriseListSchema], 400: ErrorResponse, 500: ErrorResponse})
    def list(self, request):
        """
        Retorna a lista de empresas cadastradas.
        """
        user_id = request.user.id

        result = self.services.list()

        self.log_service.create_log(
            user_id=user_id, 
            change_type="read", 
            description="Você listou todas as empresas cadastradas no sistema."
        )

        # Converter QuerySet para lista de dicionários compatíveis com Django Ninja
        enterprise_list = [
            EnterpriseListSchema(
                enterprise_id=enterprise.enterprise_id,
                name=enterprise.name,
                email=enterprise.email,
                linkedin=enterprise.linkedin,
                instagram=enterprise.instagram,
                whatsapp=enterprise.whatsapp,
                website=enterprise.website,
                summary=enterprise.summary,
                cnpj=enterprise.cnpj,
                foundation_year=enterprise.foundation_year,
                city=enterprise.city,
                state=enterprise.state,
                market=enterprise.market,
                segment=enterprise.segment,
                problem=enterprise.problem,
                solution=enterprise.solution,
                differential=enterprise.differential,
                client_type=enterprise.client_type,
                product=enterprise.product,
                product_stage=enterprise.product_stage,
                value_proposition=enterprise.value_proposition,
                competitors=enterprise.competitors,
                business_model=enterprise.business_model,
                revenue_model=enterprise.revenue_model,
                invested=enterprise.invested,
                investment_value=enterprise.investment_value,
                boosting=enterprise.boosting,
                funding_value=enterprise.funding_value,
                funding_program=enterprise.funding_program,
                accelerated=enterprise.accelerated,
                accelerator_name=enterprise.accelerator_name,
                discovered_startup=enterprise.discovered_startup,
                other_projects=enterprise.other_projects,
                profile_picture=enterprise.profile_picture,
                initial_maturity=enterprise.initial_maturity
            ).model_dump()  # Converte para dicionário
            for enterprise in result
        ]

        return enterprise_list

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
        payload_dict = payload.dict()
        owner_percentage = payload_dict.pop("owner_percentage", None)

        status_code, created_enterprise = self.services.post(payload=payload_dict, file=file)

        enterprise_id = created_enterprise.enterprise_id

        if owner_percentage is not None and owner_percentage != "":
            try:
                percentage = float(owner_percentage) if owner_percentage not in [None, ""] else 100.0
            except ValueError:
                raise ValueError(f"Invalid value for owner_percentage: {owner_percentage}. It must be a number.")

        else:
            percentage = 100.0
        UserEnterpriseRepository.post(
            payload={
                'user_id': user_id,
                'enterprise_id': enterprise_id,
                'role': 'owner',
                'status': 'accepted',
                'percentage': percentage
            }
        )

        self.log_service.create_log(
            user_id=user_id, 
            change_type="create", 
            description="Você criou uma nova empresa."
        )

        enterprise_response = EnterpriseListSchema(
            enterprise_id=created_enterprise.enterprise_id,
            name=created_enterprise.name,
            email=created_enterprise.email,
            linkedin=created_enterprise.linkedin,
            instagram=created_enterprise.instagram,
            whatsapp=created_enterprise.whatsapp,
            website=created_enterprise.website,
            summary=created_enterprise.summary,
            cnpj=created_enterprise.cnpj,
            foundation_year=created_enterprise.foundation_year,
            city=created_enterprise.city,
            state=created_enterprise.state,
            market=created_enterprise.market,
            segment=created_enterprise.segment,
            problem=created_enterprise.problem,
            solution=created_enterprise.solution,
            differential=created_enterprise.differential,
            client_type=created_enterprise.client_type,
            product=created_enterprise.product,
            product_stage=created_enterprise.product_stage,
            value_proposition=created_enterprise.value_proposition,
            competitors=created_enterprise.competitors,
            business_model=created_enterprise.business_model,
            revenue_model=created_enterprise.revenue_model,
            invested=created_enterprise.invested,
            investment_value=created_enterprise.investment_value,
            boosting=created_enterprise.boosting,
            funding_value=created_enterprise.funding_value,
            funding_program=created_enterprise.funding_program,
            accelerated=created_enterprise.accelerated,
            accelerator_name=created_enterprise.accelerator_name,
            discovered_startup=created_enterprise.discovered_startup,
            other_projects=created_enterprise.other_projects,
            profile_picture=created_enterprise.profile_picture,
            initial_maturity=created_enterprise.initial_maturity,
        )

        return 201, enterprise_response


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

    @route.delete('/{id}',response= {200: Dict[str, str], 404: ErrorResponse, 500: ErrorResponse})
    def delete(self, request, id: int):
        """
        Deleta uma empresa pelo ID.
        """
        user_id = request.user.id 
        self.log_service.create_log(
            user_id=user_id, 
            change_type="delete", 
            description="Você deletou uma empresa."
        )
        return self.services.delete(id=id)

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

    @route.post("/open_captable", response={200: CompanyMetricsGetSchema, 400: ErrorResponse, 500: ErrorResponse})
    def open_captable(self,request, enterprise_id: int, captable_percentage: float) -> Union[CompanyMetricsGetSchema, ErrorResponse]:
        """
        Endpoint para abrir a captable de uma empresa e atualizar os dados.
        """
        try:
            status, response = self.services.open_captable(
                enterprise_id=enterprise_id,
                captable_percentage=captable_percentage
            )

            if status == 200:
                return response
            elif status == 404:
                return 400, {"message": "Empresa não encontrada"}
            else:
                return 500, {"message": "Erro inesperado ao atualizar captable"}

        except Exception as e:
            return 500, {"message": f"Erro interno: {str(e)}"}

    @route.get("/", response={200: List[CompanyMetricsGetSchema]})
    def list(self, request, filters: CompanyMetricsFilterSchema = Query(...)):
        """
        Endpoint para listar os dados de métricas de empresas.
        """
        # Obtendo os dados com base nos filtros
        queryset = self.services.list(filters=filters.dict(exclude_none=True))
        return queryset
    
    @route.put('/{id}', response= {201: CompanyMetricsGetSchema, 400: ErrorResponse, 500: ErrorResponse})
    def put(self, request, id: int, payload: CompanyMetricsPutSchema = Body(...)):
        """
        Rota para Atualizar um Bioma por ID.
        """
        return self.services.update(id=id, payload=payload.dict())
    
    @route.get("/{company_metric_id}", response=CompanyMetricsGetSchema)
    def get_by_id(self,request, company_metric_id: int):
            
            response = CompanyMetricsServices.company_metrics_by_id(id=company_metric_id)
            if not response:
                return {"error": "register not found"}
            return response

    @route.post("/", response={200:CompanyMetricsGetSchema,201:CompanyMetricsGetSchema, 400: ErrorResponse, 500: ErrorResponse})
    def create( self, 
        request, 
        payload: CompanyMetricsPostSchema = Form(...)):
        response = CompanyMetricsServices.create(payload=payload)
        
 
        if not response:
            return {"error": "register not found"}
        return response

    @route.delete('/{company_metric_id}', response= {200: Dict[str, str], 404: ErrorResponse, 500: ErrorResponse})
    def delete(self,company_metric_id: int):
        """
        Exclui uma CompanyMetrics pelo ID.
        """

        return self.services.delete(id=company_metric_id)
    
    # @route.put('/{date_company_metric}', response= {200: CompanyMetricsGetSchema, 404: ErrorResponse, 500: ErrorResponse})
    # def put(self, request, date_company_metric: str, payload: CompanyMetricsPutSchema = Body(...)):
    #     """
    #     Rota para Atualizar uma CompanyMetrics pela data de criação.
    #     """
    #     return self.services.update_by_date(date_company_metric=date_company_metric, payload=payload.dict())

        

    @route.post("/get_by_date/{date_company_metric}/{id}", response={200: CompanyMetricsGetSchema, 400: ErrorResponse, 500: ErrorResponse})
    def get_by_date(self, request, date_company_metric: str, id: int, payload: CompanyMetricsPutSchema = Body(...)):
        response = CompanyMetricsServices.update_metrics_by_date(date_recorded=date_company_metric, id=id)
        
        if not response:
            return 400, {"error": "Register not found"}
        
        return 200, response



@api_controller(
    '/records',
    tags=['Rota - Prontuários'],
    
)
class RecordController:
    
    services= RecordServices

    @route.get('/', response= {200: List[RecordOutSchema], 404: ErrorResponse, 500: ErrorResponse})
    def list(self, request, filters: RecordFilterSchema = Query(...)) -> QuerySet[Any]:
        """
        Rota para Listar todos os Biomas.
        """
        return self.services.list(filters=filters)
    
    @route.post('', response= {201: RecordOutSchema, 400: ErrorResponse, 500: ErrorResponse})
    def post(self, request, payload: RecordInSchema = Form(...)):
        """
        Rota para Criar um Bioma.
        """
        
        return self.services.post(payload=payload.dict())
    
    @route.get('/{id}/', response= {200: RecordOutSchema, 404: ErrorResponse, 500: ErrorResponse})
    def get(self, request, id: int):
        """
        Rota para Listar uma empresa por ID.
        """
        return self.services.get(id=id)
    @route.put('/{id}/', response= {201: RecordOutSchema, 400: ErrorResponse, 500: ErrorResponse})
    def put(self, request, id: int, payload: RecordPutSchema = Body(...)):
        """
        Rota para Atualizar um Bioma por ID.
        """
        return self.services.put(id=id, payload=payload.dict())
    
