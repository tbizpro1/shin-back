from ninja import UploadedFile, File
from typing import Any, Dict, Optional, Tuple, List, Union
from django.db import models
from django.db import transaction, IntegrityError
from django.http import Http404
from ninja_extra import status
from .repository import EnterpriseRepository
from ..user_enterprise.repository import UserEnterpriseRepository
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
    def list(cls, *, filters: Optional[Any] = None) -> models.QuerySet:
        """
        Retorna a lista de empresas com filtros opcionais.
        """
        queryset = cls.repository.list()
        if filters:
            queryset = queryset.filter(**filters)
        return queryset
    
    @classmethod
    def get(cls, *, id: int) -> Tuple[int, models.Model | Dict[str, str]]:
        """
        Retorna uma empresa pelo ID ou lança erro.
        """
        try:
            return status.HTTP_200_OK, cls.repository.get(id=id)
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
    ) -> Tuple[int, Union[models.Model, Dict[str, str]]]:
        """
        Atualiza os dados de uma empresa.
        """
        try:
            with transaction.atomic():
                status_code, message_or_object = cls.validate_payload(payload=payload, id=id)

                if status_code != status.HTTP_200_OK:
                    return status_code, message_or_object
                
                instance: models.Model = cls.repository.put(id=id, payload=payload)
                return status.HTTP_200_OK, instance
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
    ) -> Tuple[int, Union[models.Model, Dict[str, str]]]:
        """
        Atualiza o arquivo associado a uma empresa.
        """
        try:
            with transaction.atomic():
                status_code, message_or_object = cls.get(id=id)
                if status_code != status.HTTP_200_OK:
                    return status_code, message_or_object
                
                instance: models.Model = cls.repository.upload_file(id=id, file=file)
                return status.HTTP_200_OK, instance
        except IntegrityError as error:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {"message": str(error)}
