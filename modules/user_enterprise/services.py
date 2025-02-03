from django.db import models
from django.db import transaction, IntegrityError
from ninja_extra import status
from .repository import UserEnterpriseRepository
from typing import Any, Dict, Optional, Tuple, List, Union
from django.http import Http404
class UserEnterpriseServices:
    repository = UserEnterpriseRepository
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
        