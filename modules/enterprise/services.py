from ninja import UploadedFile, File
from typing import Any, Dict, Optional, Tuple, List, Union
from django.db import models
from django.db import transaction, IntegrityError
from django.http import Http404
from ninja_extra import status
from .repository import EnterpriseRepository,CompanyMetricsRepository
from .schemas import EnterpriseListSchema,CompanyMetricsGetSchema
from .models import Enterprise,CompanyMetrics
from datetime import datetime
from decimal import Decimal, InvalidOperation
from django.core.exceptions import ObjectDoesNotExist

def validate_company_metrics_payload(payload: Dict[str, Any]) -> Optional[Dict[str, str]]:
    """
    Valida os dados do payload antes de criar ou atualizar um objeto CompanyMetrics.
    
    :param payload: Dicionário contendo os dados da requisição.
    :return: Dicionário com erros, se houver. Retorna None se estiver válido.
    """
    errors = {}
    print("passou no validate")
    
    if not payload.get("enterprise"):
        errors["enterprise"] = "O campo 'enterprise' é obrigatório."


    # Validar campos inteiros positivos
    for field in ["team_size", "total_clients", "new_clients"]:
        value = payload.get(field)
        if value is not None:
            if not isinstance(value, int) or value < 0:
                errors[field] = f"O campo '{field}' deve ser um número inteiro positivo."

    # Validar campos decimais positivos
    for field in ["revenue_period", "capital_needed", "value_invested", "value_foment"]:
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
            )
            for enterprise in queryset
        ]

        return enterprise_list
    
    @classmethod
    def get(cls, *, id: int) -> Tuple[int, Dict[str, Any]]:
        """
        Retorna uma empresa pelo ID ou lança erro.
        """
        try:
            instance: Enterprise = cls.repository.get(id=id)
            print("🔥 Instance ORM:", instance)  # Mostra a representação do objeto no Django ORM
            print("🔥 Instance as dict:", instance.__dict__)
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
                differential=instance.differential or "",  # ✅ Garante string válida
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

            return status.HTTP_200_OK, enterprise_response.model_dump()  # ✅ Retorna dicionário compatível

        except Http404:
            return status.HTTP_404_NOT_FOUND, {"message": "Enterprise not found"}

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
        """
        Deleta uma empresa pelo ID.
        """
        try:
            with transaction.atomic():
                status_code, message_or_object = cls.get(id=id)
                if status_code != status.HTTP_200_OK:
                    return status_code, message_or_object
                
                cls.repository.delete(id=id)
                return status.HTTP_204_NO_CONTENT, {"message": "Enterprise deleted successfully"}
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
                
                instance: Enterprise = cls.repository.upload_file(id=id, file=file)

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

    repository = CompanyMetricsRepository

    @classmethod
    def list(cls, *, filters: Optional[dict] = None) -> List[CompanyMetricsGetSchema]:
        queryset = CompanyMetrics.objects.all()

        if filters:
            queryset = queryset.filter(**filters)
        print(f"o queryset com id",queryset)
        # Convertendo os objetos Django em schemas
        company_metrics_data = [
            CompanyMetricsGetSchema.from_orm(company_metric) for company_metric in queryset
        ]       
        print(company_metrics_data,"acaboou")
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
                print("passou aquii",payload)
                validation_errors = validate_company_metrics_payload(payload=payload_dict)
                print("nao passou")
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
                print("companyyyy",company_metrics)
                company_metrics_data = CompanyMetricsGetSchema(
                    id=company_metrics.id,
                    enterprise=company_metrics.enterprise.enterprise_id,  # ou qualquer outro campo relevante
                    team_size=company_metrics.team_size,
                    revenue_period=company_metrics.revenue_period,
                    total_clients=company_metrics.total_clients,
                    new_clients=company_metrics.new_clients,
                    investment_round_open=company_metrics.investment_round_open,
                    capital_needed=company_metrics.capital_needed,
                    value_invested=company_metrics.value_invested,
                    value_foment=company_metrics.value_foment,
                    valuation=company_metrics.valuation
                )

                return status.HTTP_201_CREATED, company_metrics_data.dict()
        except IntegrityError as error:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {"message": str(error)}

    @classmethod
    def update(cls, *, id: int, payload: Dict[str, Any]) -> Tuple[int, Union[models.Model, Dict[str, str]]]:
        """
        Atualiza uma CompanyMetrics existente com os dados fornecidos.
        """
        try:
            payload_dict = payload.__dict__
            with transaction.atomic():
                validation_errors = validate_company_metrics_payload(payload=payload_dict)
                id_enterprise = payload_dict.get("enterprise")

                try:
                    instance_enterprise: Enterprise = Enterprise.objects.get(enterprise_id=id_enterprise)
                except ObjectDoesNotExist:
                    raise ValueError(f"Enterprise com ID {id_enterprise} não encontrado.")

                if validation_errors:
                    return status.HTTP_400_BAD_REQUEST, validation_errors
                payload_dict["enterprise"] = instance_enterprise

                # Atualizar o objeto CompanyMetrics
                company_metrics = CompanyMetricsRepository.update_company_metrics(id=id, payload=payload_dict)

                # Serializar os dados atualizados
                company_metrics_data = CompanyMetricsGetSchema(
                    enterprise=company_metrics.enterprise.enterprise_id,
                    team_size=company_metrics.team_size,
                    revenue_period=company_metrics.revenue_period,
                    total_clients=company_metrics.total_clients,
                    new_clients=company_metrics.new_clients,
                    investment_round_open=company_metrics.investment_round_open,
                    capital_needed=company_metrics.capital_needed,
                    value_invested=company_metrics.value_invested,
                    value_foment=company_metrics.value_foment,
                    valuation=company_metrics.valuation
                )

                return status.HTTP_200_OK, company_metrics_data.dict()
        except IntegrityError as error:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {"message": str(error)}

    @classmethod
    def delete(
        cls, *, id: int, **kwargs
    ) -> Tuple[int, Union[models.Model, Dict[str, str]]]:
        """
        Deleta uma empresa pelo ID.
        """
        try:
            with transaction.atomic():
                status_code, message_or_object = cls.get(id=id)
                if status_code != status.HTTP_200_OK:
                    return status_code, message_or_object
                
                cls.repository.delete(id=id)
                return status.HTTP_204_NO_CONTENT, {"message": "Enterprise deleted successfully"}
        except IntegrityError as error:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {"message": str(error)}