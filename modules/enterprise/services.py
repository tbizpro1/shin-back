from ninja import UploadedFile, File
from typing import Any, Dict, Optional, Tuple, List, Union
from django.db import models
from django.db import transaction, IntegrityError
from django.http import Http404
from ninja_extra import status
from .repository import EnterpriseRepository,CompanyMetricsRepository,RecordRepository
from .schemas import EnterpriseListSchema,CompanyMetricsGetSchema
from .models import Enterprise,CompanyMetrics
from datetime import datetime
from decimal import Decimal, InvalidOperation
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date

def validate_company_metrics_payload(payload: Dict[str, Any]) -> Optional[Dict[str, str]]:
    """
    Valida os dados do payload antes de criar ou atualizar um objeto CompanyMetrics.
    
    :param payload: Dicionário contendo os dados da requisição.
    :return: Dicionário com erros, se houver. Retorna None se estiver válido.
    """
    errors = {}
    
    if not payload.get("enterprise"):
        errors["enterprise"] = "O campo 'enterprise' é obrigatório."


    # Validar campos inteiros positivos
    for field in ["team_size", "total_clients", "new_clients"]:
        value = payload.get(field)
        if value is not None:
            if not isinstance(value, int) or value < 0:
                errors[field] = f"O campo '{field}' deve ser um número inteiro positivo."

    # Validar campos decimais positivos
    for field in ["revenue_period", "capital_needed", "value_foment"]:
        value = payload.get(field)
        if value is not None:
            try:
                decimal_value = Decimal(str(value))
                if decimal_value < 0:
                    errors[field] = f"O campo '{field}' deve ser um número positivo."
            except InvalidOperation:
                errors[field] = f"O campo '{field}' deve ser um número decimal válido."

    # Validar 'investment_round_open' e 'capital_needed'
    investment_round_open = payload.get("investment_round_open", False)
    capital_needed = payload.get("capital_needed")

    if investment_round_open and capital_needed is None:
        errors["capital_needed"] = "Se 'investment_round_open' for True, 'capital_needed' deve ser informado."

    # Validar 'valuation'
    valuation = payload.get("valuation", "").strip()
    if not valuation:
        errors["valuation"] = "O campo 'valuation' não pode ser vazio."

    return errors if errors else None

class EnterpriseServices:
    """
    Serviços para operações no modelo Enterprise.
    """
    
    repository = EnterpriseRepository
    whitelist_disable_models: List[Optional[str]] = []
    
    @classmethod
    def validate_payload(
        cls, *, payload: Dict[str, Any], id: Optional[int] = None, **kwargs
    ) -> Tuple[int, Optional[models.Model | Dict[str, str]]]:
        """
        Valida o payload antes de salvar ou atualizar.
        """
        instance: Optional[models.Model] = None
        return status.HTTP_200_OK, instance

    @classmethod
    def list(cls, *, filters: Optional[Any] = None) -> List[EnterpriseListSchema]:
        """
        Retorna a lista de empresas com filtros opcionais.
        """
        queryset = cls.repository.list()
        if filters:
            queryset = queryset.filter(**filters)
        # Converter o QuerySet para uma lista de `EnterpriseListSchema`
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
            )  
            for enterprise in queryset
        ]

        return enterprise_list
    
    @classmethod
    def get(cls, *, id: int) -> Tuple[int, models.Model | Dict[str, str]]:
        try:
            object_dict = cls.repository.get(id=id).__dict__
            return status.HTTP_200_OK, {
        "enterprise_id": object_dict["enterprise_id"],
        "name": object_dict["name"],
        "email": object_dict.get("email"),
        "linkedin": object_dict.get("linkedin"),
        "instagram": object_dict.get("instagram"),
        "whatsapp": object_dict.get("whatsapp"),
        "website": object_dict.get("website"),
        "summary": object_dict.get("summary"),
        "cnpj": object_dict.get("cnpj"),
        "foundation_year": object_dict.get("foundation_year"),
        "city": object_dict.get("city"),
        "state": object_dict.get("state"),
        "market": object_dict.get("market"),
        "segment": object_dict.get("segment"),
        "problem": object_dict.get("problem"),
        "solution": object_dict.get("solution"),
        "differential": object_dict.get("differential"),
        "client_type": object_dict.get("client_type"),
        "product": object_dict.get("product"),
        "product_stage": object_dict.get("product_stage"),
        "value_proposition": object_dict.get("value_proposition"),
        "competitors": object_dict.get("competitors"),
        "business_model": object_dict.get("business_model"),
        "revenue_model": object_dict.get("revenue_model"),
        "invested": object_dict.get("invested", False),
        "investment_value": object_dict.get("investment_value"),
        "boosting": object_dict.get("boosting", False),
        "funding_value": object_dict.get("funding_value"),
        "funding_program": object_dict.get("funding_program"),
        "accelerated": object_dict.get("accelerated", False),
        "accelerator_name": object_dict.get("accelerator_name"),
        "discovered_startup": object_dict.get("discovered_startup"),
        "other_projects": object_dict.get("other_projects"),
        "profile_picture": object_dict.get("profile_picture"),
        "initial_maturity": object_dict.get("initial_maturity"),
    }
        
        except Http404:
            return status.HTTP_404_NOT_FOUND, {"message": (
                f"{cls.repository.model._meta.verbose_name.capitalize()} not found"
                ' não existe'
            ) }
    @classmethod
    def post(
        cls, *, payload: Dict[str, Any], file: Optional[UploadedFile] = File(None), **kwargs
    ) -> Tuple[int, Union[models.Model, Dict[str, str]]]:
        """
        Cria uma nova empresa no banco de dados.
        """
        try:
            with transaction.atomic():
                status_code, message = cls.validate_payload(payload=payload)

                if status_code != status.HTTP_200_OK:
                    return status_code, message
                
                instance = cls.repository.post(payload=payload, file=file)
                return status.HTTP_201_CREATED, instance
        except IntegrityError as error:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {"message": str(error)}

    @classmethod
    def put(
        cls, *, id: int, payload: Dict[str, Any], **kwargs
    ) -> Tuple[int, Union[EnterpriseListSchema, Dict[str, str]]]:
        """
        Atualiza os dados de uma empresa.
        """
        try:
            with transaction.atomic():
                status_code, message_or_object = cls.validate_payload(payload=payload, id=id)

                if status_code != status.HTTP_200_OK:
                    return status_code, message_or_object
                
                instance: Enterprise = cls.repository.put(id=id, payload=payload)

                enterprise_response = EnterpriseListSchema(
                    enterprise_id=instance.enterprise_id,
                    name=instance.name,
                    email=instance.email,
                    linkedin=instance.linkedin,
                    instagram=instance.instagram,
                    whatsapp=instance.whatsapp,
                    website=instance.website,
                    summary=instance.summary,
                    cnpj=instance.cnpj,
                    foundation_year=instance.foundation_year,
                    city=instance.city,
                    state=instance.state,
                    market=instance.market,
                    segment=instance.segment,
                    problem=instance.problem,
                    solution=instance.solution,
                    differential=instance.differential or "",  
                    client_type=instance.client_type,
                    product=instance.product,
                    product_stage=instance.product_stage,
                    value_proposition=instance.value_proposition,
                    competitors=instance.competitors,
                    business_model=instance.business_model,
                    revenue_model=instance.revenue_model,
                    invested=instance.invested,
                    investment_value=instance.investment_value,
                    boosting=instance.boosting,
                    funding_value=instance.funding_value,
                    funding_program=instance.funding_program,
                    accelerated=instance.accelerated,
                    accelerator_name=instance.accelerator_name,
                    discovered_startup=instance.discovered_startup,
                    other_projects=instance.other_projects,
                )

                return status.HTTP_200_OK, enterprise_response  # ✅ Retorna o schema correto

        except IntegrityError as error:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {"message": str(error)}

    @classmethod
    def delete(
        cls, *, id: int, **kwargs
    ) -> Tuple[int, Union[models.Model, Dict[str, str]]]:
        try:
            with transaction.atomic():
                status_code: int
                message_or_object: Dict[str, str] | models.Model

                status_code, message_or_object = cls.get(id=id)
                if status_code != status.HTTP_200_OK:
                    return status_code, message_or_object
                
                instance: models.Model = message_or_object

                instance = cls.repository.delete(instance=instance)

                return status.HTTP_200_OK, {"message": "Empresa deletado com sucesso"}
            
        except IntegrityError as error:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {"message": str(error)}

    @classmethod
    def upload_file(
        cls, *, id: int, file: UploadedFile, **kwargs
    ) -> Tuple[int, Dict[str, Any]]:
        """
        Atualiza o arquivo associado a uma empresa.
        """
        try:
            with transaction.atomic():
                status_code, message_or_object = cls.get(id=id)
                if status_code != status.HTTP_200_OK:
                    return status_code, message_or_object
                
                instance: Enterprise = cls.repository.put_picture(id=id, file=file)
                # ✅ Converter `instance` para `EnterpriseListSchema`
                enterprise_response = EnterpriseListSchema(
                    enterprise_id=instance.enterprise_id,
                    name=instance.name,
                    email=instance.email,
                    linkedin=instance.linkedin,
                    instagram=instance.instagram,
                    whatsapp=instance.whatsapp,
                    website=instance.website,
                    summary=instance.summary,
                    cnpj=instance.cnpj,
                    foundation_year=instance.foundation_year,
                    city=instance.city,
                    state=instance.state,
                    market=instance.market,
                    segment=instance.segment,
                    problem=instance.problem,
                    solution=instance.solution,
                    differential=instance.differential or "",  # ✅ Evita erro de `None`
                    client_type=instance.client_type,
                    product=instance.product,
                    product_stage=instance.product_stage,
                    value_proposition=instance.value_proposition,
                    competitors=instance.competitors,
                    business_model=instance.business_model,
                    revenue_model=instance.revenue_model,
                    invested=instance.invested,
                    investment_value=instance.investment_value,
                    boosting=instance.boosting,
                    funding_value=instance.funding_value,
                    funding_program=instance.funding_program,
                    accelerated=instance.accelerated,
                    accelerator_name=instance.accelerator_name,
                    discovered_startup=instance.discovered_startup,
                    other_projects=instance.other_projects,
                    profile_picture=instance.profile_picture
                )

                return status.HTTP_200_OK, enterprise_response.model_dump()  # ✅ Retorna um dicionário compatível

        except IntegrityError as error:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {"message": str(error)}

class CompanyMetricsServices:
    """
    Serviços para operações no modelo Company Metrics.
    """
    Enterprise_repository = EnterpriseRepository
    repository = CompanyMetricsRepository

    @classmethod
    def open_captable(cls, *, enterprise_id: int, captable_percentage: float):
        """
        Serviço para abrir a captable de uma empresa.
        Verifica se a empresa existe e chama o repositório para atualizar ou criar o registro.

        :param enterprise_id: ID da empresa (Enterprise)
        :param captable_percentage: Porcentagem da captable (exemplo: 12.5 para 12,5%)
        :return: Dicionário com status e mensagem
        """
        try:
            # Verifica se a empresa existe
            enterprise = EnterpriseRepository.get(id=enterprise_id)

            # Chama o repositório para atualizar a captable
            status, response = CompanyMetricsRepository.open_captable(
                enterprise_id=enterprise.enterprise_id, 
                captable_percentage=captable_percentage
            )
            print(f"response: {response} status: {status}")

            return status, response

        except Exception:
            return 404, {"message": "Empresa não encontrada"}

    @classmethod
    def get(cls, *, id: int) -> Tuple[int, models.Model | Dict[str, str]]:
        try:
            return status.HTTP_200_OK, cls.repository.get(id=id)
        except Http404:
            return status.HTTP_404_NOT_FOUND, {"message": (
                f"{cls.repository.model._meta.verbose_name.capitalize()} not found"
                ' não existe'
            ) }
        
    @classmethod
    def list(cls, *, filters: Optional[dict] = None) -> List[CompanyMetricsGetSchema]:
        queryset = CompanyMetrics.objects.all()

        if filters:
            queryset = queryset.filter(**filters)
        # Convertendo os objetos Django em schemas
        company_metrics_data = [
            CompanyMetricsGetSchema.from_orm(company_metric) for company_metric in queryset
        ]       

        print(f"company_metrics_data: {company_metrics_data}")
        return company_metrics_data
    @classmethod
    def company_metrics_by_id(cls,*,id: int) -> models.QuerySet:
        register = CompanyMetricsRepository.company_metrics_by_id(id=id)
        if register:
            return CompanyMetricsGetSchema(**register.__dict__)
        return None
    
    @classmethod
    def create(cls, *, payload: Dict[str, Any]) -> Tuple[int, Union[models.Model, Dict[str, str]]]:
        """
        Cria uma nova CompanyMetrics.
        """
        try:
            payload_dict = payload.__dict__
            with transaction.atomic():
                validation_errors = validate_company_metrics_payload(payload=payload_dict)
                
                id_enterprise=payload_dict.get("enterprise")
                try:
                    instance_enterprise:Enterprise = Enterprise.objects.get(enterprise_id=id_enterprise)
                except ObjectDoesNotExist:
                    raise ValueError(f"Enterprise com ID {instance_enterprise} não encontrado.")

                if validation_errors:
                    return status.HTTP_400_BAD_REQUEST, validation_errors
                payload_dict["enterprise"] = instance_enterprise

                # Criar o objeto CompanyMetrics
                company_metrics = CompanyMetricsRepository.create_company_metrics(payload=payload_dict)
                company_metrics_data = CompanyMetricsGetSchema(
                    id=company_metrics.id,
                    enterprise_id=id_enterprise,  # ou qualquer outro campo relevante
                    team_size=company_metrics.team_size,
                    revenue_period=company_metrics.revenue_period,
                    total_clients=company_metrics.total_clients,
                    new_clients=company_metrics.new_clients,
                    investment_round_open=company_metrics.investment_round_open,
                    capital_needed=company_metrics.capital_needed,
                    value_foment=company_metrics.value_foment,
                    valuation=company_metrics.valuation
                )

                return status.HTTP_201_CREATED, company_metrics_data.dict()
        except IntegrityError as error:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {"message": str(error)}

    @classmethod
    def update(
        cls,
        *,
        id: int,
        payload: Dict[str, Any],
        **kwargs
    ) -> Tuple[int, Union[models.Model, Dict[str, str]]]:
        
        try:
            with transaction.atomic():
                status_code: int
                message: Dict[str, str]

                # Aqui você pode deixar o código de validação descomentado quando quiser validar
                # status_code, message_or_object = cls.validate_payload(payload=payload, id=id)

                # if status_code != status.HTTP_200_OK:
                #     message = message_or_object
                #     return status_code, message

                # A instância do modelo deve ser recuperada antes de ser passada ao repositório


                # Passa a instância e o payload para a função `put` no repositório
                updated_instance = cls.repository.put( payload=payload, id=id)
                
                # Aqui, `updated_instance` é o objeto atualizado que será retornado
                response_dict = updated_instance.__dict__
                return status.HTTP_201_CREATED, {
    "id": response_dict["id"],
    "enterprise_id": response_dict["enterprise_id"],
    "team_size": response_dict["team_size"],
    "revenue_period": float(response_dict["revenue_period"]),  # Convertendo Decimal para float
    "total_clients": response_dict["total_clients"],
    "new_clients": response_dict["new_clients"],
    "investment_round_open": response_dict["investment_round_open"],
    "capital_needed": float(response_dict["capital_needed"]),  # Convertendo Decimal para float  # Convertendo Decimal para float
    "value_foment": float(response_dict["value_foment"]),  # Convertendo Decimal para float
    "valuation": response_dict["valuation"],
    "date_recorded": response_dict["date_recorded"].isoformat()  # Convertendo datetime para string
}

        except Exception as e:
            return status.HTTP_400_BAD_REQUEST, {"error": str(e)}
    @classmethod
    def delete(
        cls, *, id: int, **kwargs
    ) -> Tuple[int, Union[models.Model, Dict[str, str]]]:
        try:
            with transaction.atomic():
                status_code: int
                message_or_object: Dict[str, str] | models.Model

                status_code, message_or_object = cls.get(id=id)
                if status_code != status.HTTP_200_OK:
                    return status_code, message_or_object
                
                instance: models.Model = message_or_object

                instance = cls.repository.delete(instance=instance)

                return status.HTTP_200_OK, {"message": "Empresa deletado com sucesso"}
            
        except IntegrityError as error:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {"message": str(error)}
        
    @classmethod
    def update_metrics_by_date(
        cls, *, date_recorded: str, id: int, payload: Dict[str, Any], **kwargs
    ) -> Tuple[int, Union[models.Model, Dict[str, str]]]:
        try:
            with transaction.atomic():
                # Obtém o registro pelo date_recorded e id
                status_code, result = cls.repository.get_by_date(
                    date_recorded=date_recorded, id=id
                )

                if status_code != status.HTTP_200_OK:
                    return status_code, result  # Retorna erro caso não encontre

                instance: models.Model = result  # Garantia que result é um Model
                updated_instance = cls.repository.update_by_date(
                    instance=instance, payload=payload
                )

                return status.HTTP_200_OK, updated_instance  # Retorna o objeto atualizado

        except Exception as e:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {"error": str(e)}
        

        
class RecordServices:
    """
    Serviços para operações no modelo Company Metrics.
    """

    repository = RecordRepository

    # @classmethod
    # def validate_payload(cls, data):
    #     """
    #     Valida o payload antes de criar ou atualizar o registro.
    #     """
    #     required_fields = ['enterprise', 'date_collected', 'responsible', 'data_type', 'mit_phase', 'product_status', 'business_status']
    #     for field in required_fields:
    #         if field not in data or not data[field]:
    #             raise ValidationError(_("Campo '{}' é obrigatório.".format(field)))

    #     if data['data_type'] not in dict(cls.TRL.choices):
    #         raise ValidationError(_("Valor inválido para 'data_type'."))        
    #     if data['mit_phase'] not in dict(cls.MITPhase.choices):
    #         raise ValidationError(_("Valor inválido para 'mit_phase'."))        
    #     if data['product_status'] not in dict(cls.ProductStatus.choices):
    #         raise ValidationError(_("Valor inválido para 'product_status'."))        
    #     if data['business_status'] not in dict(cls.BusinessStatus.choices):
    #         raise ValidationError(_("Valor inválido para 'business_status'."))

    #     if data.get('next_meeting_date') and data['next_meeting_date'] < date.today():
    #         raise ValidationError(_("A data da próxima agenda não pode ser no passado."))

    #     return status.HTTP_200_OK, {}
    @classmethod
    def list(cls, *, filters: Optional[Any] = None) -> models.QuerySet:
        queryset = cls.repository.list()
        if filters is not None:
            queryset = filters.filter(queryset)
        response = []
        for record in queryset:
            record_dict = {
                "id": record.id,
                "enterprise": record.enterprise_id,  # Adiciona o ID da empresa, não a instância
                "date_collected": record.date_collected,
                "data_type": record.data_type,
                "mit_phase": record.mit_phase,
                "product_status": record.product_status,
                "business_status": record.business_status,
                "how_we_can_help": record.how_we_can_help,
                "next_steps": record.next_steps,
                "next_meeting_date": record.next_meeting_date,
                "observations": record.observations,
                "responsible_person": record.responsible_person,

            }
            response.append(record_dict)
        
        return response
        
    @classmethod
    def post(
        cls, *, payload: Dict[str, Any], **kwargs
    ) -> Tuple [int, Union[models.Model, Dict[str, str]]]:
        try:
            with transaction.atomic():
                status_code: int
                message: Dict[str, str]

                # status_code, message = cls.validate_payload(payload)

                # if status_code != status.HTTP_200_OK:
                #     return status_code, message
                
                instance = cls.repository.post(payload=payload)
                response_dict = instance.__dict__
                
                return status.HTTP_201_CREATED, {
                "id": response_dict["id"],
                "enterprise": response_dict["enterprise_id"],  # Aqui é o ID da empresa
                "date_collected": response_dict["date_collected"],
                "responsible_person": response_dict["responsible_person"],
                "data_type": response_dict["data_type"],
                "mit_phase": response_dict["mit_phase"],
                "product_status": response_dict["product_status"],
                "business_status": response_dict["business_status"],
                "how_we_can_help": response_dict.get("how_we_can_help", None),
                "next_steps": response_dict.get("next_steps", None),
                "next_meeting_date": response_dict.get("next_meeting_date", None),
                "observations": response_dict.get("observations", None),
            }   
        except IntegrityError as error:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {"message": str(error)}
        
    @classmethod
    def get(cls, *, id: int) -> Tuple[int, models.Model | Dict[str, str]]:
        try:
            response_dict = cls.repository.get(id=id).__dict__
            return status.HTTP_200_OK, {
                "id": response_dict["id"],
                "enterprise": response_dict["enterprise_id"],  # Aqui é o ID da empresa
                "date_collected": response_dict["date_collected"],
                "responsible_person": response_dict["responsible_person"],
                "data_type": response_dict["data_type"],
                "mit_phase": response_dict["mit_phase"],
                "product_status": response_dict["product_status"],
                "business_status": response_dict["business_status"],
                "how_we_can_help": response_dict.get("how_we_can_help", None),
                "next_steps": response_dict.get("next_steps", None),
                "next_meeting_date": response_dict.get("next_meeting_date", None),
                "observations": response_dict.get("observations", None),
            }
        except Http404:
            return status.HTTP_404_NOT_FOUND, {"message": (
                f"{cls.repository.model._meta.verbose_name.capitalize()} not found"
                ' não existe'
            ) }
        

    @classmethod
    def put(
        cls,
        *,
        id: int,
        payload: Dict[str, Any],
        **kwargs
    ) -> Tuple[int, Union[models.Model, Dict[str, str]]]:
        
        try:
            with transaction.atomic():
                status_code: int
                message: Dict[str, str]

                # Aqui você pode deixar o código de validação descomentado quando quiser validar
                # status_code, message_or_object = cls.validate_payload(payload=payload, id=id)

                # if status_code != status.HTTP_200_OK:
                #     message = message_or_object
                #     return status_code, message

                # A instância do modelo deve ser recuperada antes de ser passada ao repositório


                # Passa a instância e o payload para a função `put` no repositório
                updated_instance = cls.repository.put( payload=payload, id=id)
                
                # Aqui, `updated_instance` é o objeto atualizado que será retornado
                response_dict = updated_instance.__dict__
                
                return status.HTTP_201_CREATED, {
                    "id": response_dict["id"],
                    "enterprise": response_dict["enterprise_id"],  # Aqui é o ID da empresa
                    "date_collected": response_dict["date_collected"],
                    "responsible_person": response_dict["responsible_person"],
                    "data_type": response_dict["data_type"],
                    "mit_phase": response_dict["mit_phase"],
                    "product_status": response_dict["product_status"],
                    "business_status": response_dict["business_status"],
                    "how_we_can_help": response_dict.get("how_we_can_help", None),
                    "next_steps": response_dict.get("next_steps", None),
                    "next_meeting_date": response_dict.get("next_meeting_date", None),
                    "observations": response_dict.get("observations", None),
                }

        except Exception as e:
            return status.HTTP_400_BAD_REQUEST, {"error": str(e)}