from core import settings
from ninja import UploadedFile, File
import os
from typing import Any, Dict, Optional, Tuple, List, Union
from .repository import Repository
from django.db import models
from django.http import Http404
from ninja_extra import status
from django.db import transaction, IntegrityError

class Services:
    
    repository = Repository
    whitelist_disable_models: List[Optional[str]] = []
    
    @classmethod
    def validate_payload(
        cls, *, payload: Dict[str, Any], id: Optional[int] = None, **kwargs
    ) -> Tuple[int, Optional[models.Model | Dict[str, str]]]:
        instance: Optional[models.Model] = None
        return status.HTTP_200_OK, instance

    @classmethod
    def list(cls, *, filters: Optional[Any] = None) -> models.QuerySet:
        queryset = cls.repository.list()
        if filters:
            queryset = queryset.filter(**filters)
        return queryset
    
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
    def post(
        cls, *, payload: Dict[str, Any], file: Optional[UploadedFile] = File(None), **kwargs
    ) -> Tuple [int, Union[models.Model, Dict[str, str]]]:
        try:
            with transaction.atomic():
                status_code: int
                message: Dict[str, str]

                status_code, message = cls.validate_payload(payload=payload)

                if status_code != status.HTTP_200_OK:
                    return status_code, message
                
                instance = cls.repository.post(payload=payload, file=file)
                return status.HTTP_201_CREATED, instance
        except IntegrityError as error:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {"message": str(error)}

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

                # Validação do payload
                status_code, message_or_object = cls.validate_payload(payload=payload, id=id)

                if status_code != status.HTTP_200_OK:
                    return status_code, message_or_object

                instance: models.Model = message_or_object

                # Atualizar a instância no repositório
                instance = cls.repository.put(
                    instance=instance, payload=payload, id=id,
                )

                # Retornar status 200 para atualização bem-sucedida
                return status.HTTP_200_OK, instance

        except IntegrityError as error:
            # Erro de integridade do banco de dados
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {"message": str(error)}

        except Exception as error:
            # Qualquer outro erro
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {"message": f"Erro inesperado: {str(error)}"}
        
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

                return status.HTTP_200_OK, {"message": "Usuário deletado com sucesso"}
            
        except IntegrityError as error:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {"message": str(error)}
        
    @classmethod
    def put_picture(
        cls,
        *,
        id: int,
        file: UploadedFile,
        **kwargs
    ) -> Tuple[int, Union[models.Model, Dict[str, str]]]:
        try:
            with transaction.atomic():
                status_code: int
                message_or_object: Dict[str, str] | models.Model

                status_code, message_or_object = cls.get(id=id)
                if status_code != status.HTTP_200_OK:
                    return status_code, message_or_object
                
                instance: models.Model = message_or_object

                instance = cls.repository.put_picture(
                    instance=instance, file=file, id=id
                )

                return status.HTTP_201_CREATED, instance
            
        except IntegrityError as error:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {"message": str(error)}