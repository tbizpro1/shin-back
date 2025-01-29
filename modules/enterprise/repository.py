import os
from typing import Dict, Optional
from django.db import models
from django.shortcuts import get_object_or_404
from ninja import UploadedFile, File
from core import settings
from modules.enterprise.models import Enterprise,CompanyMetrics
from ..user_enterprise.repository import UserEnterpriseRepository
from cloudinary.uploader import upload

class EnterpriseRepository:
    """
    Repositório para a modelagem de Enterprise.
    Gerencia operações CRUD no banco de dados.
    """

    model = Enterprise
    model_user_enterprise = UserEnterpriseRepository
    @classmethod
    def list(cls) -> models.QuerySet:
        """
        Retorna todas as empresas ordenadas por ID.
        """
        return cls.model.objects.all().order_by("enterprise_id")

    @classmethod
    def get(cls, *, id: int) -> models.Model:
        """
        Retorna uma empresa específica pelo ID ou lança um erro 404.
        """
        object = get_object_or_404(cls.model, enterprise_id=id)
      
        return object

    @classmethod
    def update_payload(cls, *, payload: Dict, **kwargs) -> Dict:
        """
        Atualiza o payload com valores específicos antes de salvar.
        """
        if "invested" in payload and payload["invested"]:
            payload["boosting"] = True

        if "value_invested" in payload and payload["value_invested"] is None:
            payload["value_invested"] = 0.0

        if "value_foment" in payload and payload["value_foment"] is None:
            payload["value_foment"] = 0.0

        return payload


    @classmethod
    def post(
        cls, *, payload: Dict, file: Optional[UploadedFile] = None, **kwargs
    ) -> models.Model:
        """
        Cria um novo registro de empresa no banco de dados.
        """
        if file:
            try:
                upload_response = upload(file, folder="enterprises_pictures/")
                file_url = upload_response.get("secure_url")
                payload["profile_picture"] = file_url
            except Exception as e:
                print(f"Erro ao fazer upload para o Cloudinary: {e}")
                raise e
        
        # Atualiza payload antes da criação
        payload = cls.update_payload(payload=payload)
        
        # Cria a instância do modelo no banco de dados
        enterprise = cls.model.objects.create(**payload)
        
        return enterprise
    
    @classmethod
    def put(cls, *, id: int, payload: Dict, **kwargs) -> models.Model:
        """
        Atualiza os dados de uma empresa existente.
        """
        instance = cls.get(id=id)

        for attr, value in payload.items():
            if value is not None:  # Ignora valores nulos
                setattr(instance, attr, value)

        instance.save()
        return instance

    @classmethod
    def delete(cls, *, id: int, **kwargs) -> None:
        """
        Deleta uma empresa pelo ID.
        """
        instance = cls.get(id=id)
        instance.delete()

    @classmethod
    def upload_file(cls, *, id: int, file: UploadedFile, **kwargs) -> models.Model:
        """
        Atualiza o arquivo associado a uma empresa.
        """
        instance = cls.get(id=id)

        upload_dir = os.path.join(settings.MEDIA_ROOT, "enterprise_files")
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        file_name = f"{file.name}"
        file_path = os.path.join(upload_dir, file_name)

        with open(file_path, "wb+") as f:
            for chunk in file.chunks():
                f.write(chunk)

        instance.file = os.path.join("enterprise_files", file_name)
        instance.save()
        return instance


class CompanyMetricsRepository:
    """
    Repositório para a modelagem de Enterprise.
    Gerencia operações CRUD no banco de dados.
    """

    model = CompanyMetrics

    @classmethod
    def list(cls)-> models.QuerySet:
        """
        Retorna todas as empresas ordenadas por ID.
        """
        return cls.model.objects.all()