from typing import Dict, Optional
from django.db import models
from django.shortcuts import get_object_or_404
from modules.user_enterprise.models import UserEnterprise
from modules.user.models import User
from modules.enterprise.models import Enterprise


class UserEnterpriseRepository:
    """
    Repositório para a modelagem de UserEnterprise.
    Gerencia operações CRUD no banco de dados.
    """

    model = UserEnterprise

    @classmethod
    def list(cls) -> models.QuerySet:
        """
        Retorna todas as relações UserEnterprise ordenadas por ID.
        """
        return cls.model.objects.all().order_by("ue_id")

    @classmethod
    def get(cls, *, id: int) -> models.Model:
        """
        Retorna uma relação UserEnterprise específica pelo ID ou lança um erro 404.
        """
        return get_object_or_404(cls.model, ue_id=id)

    @classmethod
    def post(cls, *, payload: Dict, **kwargs) -> models.Model:
        """
        Cria um novo registro de relação UserEnterprise no banco de dados.
        """
        user = get_object_or_404(User, id=payload["user_id"])
        enterprise = get_object_or_404(Enterprise, enterprise_id=payload["enterprise_id"])
        
        payload["user"] = user
        payload["enterprise"] = enterprise
        del payload["user_id"]
        del payload["enterprise_id"]

        return cls.model.objects.create(**payload)

    @classmethod
    def put(cls, *, id: int, payload: Dict, **kwargs) -> models.Model:
        """
        Atualiza os dados de uma relação UserEnterprise existente.
        """
        instance = cls.get(id=id)

        if "user_id" in payload:
            user = get_object_or_404(User, id=payload["user_id"])
            instance.user = user

        if "enterprise_id" in payload:
            enterprise = get_object_or_404(Enterprise, enterprise_id=payload["enterprise_id"])
            instance.enterprise = enterprise

        if "role" in payload and payload["role"] is not None:
            instance.role = payload["role"]

        instance.save()
        return instance

    @classmethod
    def delete(cls, *, id: int, **kwargs) -> None:
        """
        Deleta uma relação UserEnterprise pelo ID.
        """
        instance = cls.get(id=id)
        instance.delete()

    @classmethod
    def list_by_user(cls, *, user_id: int) -> models.QuerySet:
        """
        Retorna todas as relações UserEnterprise associadas a um usuário específico.
        """
        user = get_object_or_404(User, id=user_id)
        return cls.model.objects.filter(user=user).order_by("ue_id")

    @classmethod
    def list_by_enterprise(cls, *, enterprise_id: int) -> models.QuerySet:
        """
        Retorna todas as relações UserEnterprise associadas a uma empresa específica.
        """
        enterprise = get_object_or_404(Enterprise, enterprise_id=enterprise_id)
        return cls.model.objects.filter(enterprise=enterprise).order_by("ue_id")
