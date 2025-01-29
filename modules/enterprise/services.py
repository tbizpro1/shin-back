from ninja import UploadedFile, File
from typing import Any, Dict, Optional, Tuple, List, Union
from django.db import models
from django.db import transaction, IntegrityError
from django.http import Http404
from ninja_extra import status
from .repository import EnterpriseRepository,CompanyMetricsRepository
from .schemas import EnterpriseListSchema
from .models import Enterprise
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
    def list(cls, *, filters: Optional[Any] = None) -> models.QuerySet:
        queryset = cls.repository.list()
        if filters:
            queryset = queryset.filter(**filters)
        return queryset