import os
from typing import Dict, Optional, Tuple, Any
from django.db import models,transaction
from django.shortcuts import get_object_or_404
from ninja import UploadedFile, File
from core import settings
from modules.enterprise.models import Enterprise,CompanyMetrics,Record
from ..user_enterprise.repository import UserEnterpriseRepository
from cloudinary.uploader import upload
from django.db.models import Q

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
    def delete(
        cls, *, instance: models.Model
        ) -> models.Model:
        instance.delete()
        return instance

    
    @classmethod
    def put_picture(
        cls,
        *,
        id: int,
        file: UploadedFile,
        **kwargs
    ) -> models.Model:
        instance = cls.get(id=id)

        try:
            upload_response = upload(file, folder="profile_pictures/")
            file_url = upload_response.get("secure_url")
            instance.profile_picture = file_url  # Atualizar o campo profile_picture com a URL gerada
        except Exception as e:
            raise e

        instance.save()

        return instance


class CompanyMetricsRepository:
    """
    Repositório para a modelagem de Enterprise.
    Gerencia operações CRUD no banco de dados.
    """

    model = CompanyMetrics
    @classmethod
    def get(cls, *, id: int) -> models.Model:
        """
        Retorna uma empresa específica pelo ID ou lança um erro 404.
        """
        object = get_object_or_404(cls.model, id=id)
      
        return object
    @classmethod
    def list(cls)-> models.QuerySet:
        """
        Retorna todas as empresas ordenadas por ID.
        """
        return cls.model.objects.all()
    
    @classmethod
    def company_metrics_by_id(cls,*,id:int) -> models.Model:
        """
        Busca um registro pelo id
        """
        return get_object_or_404(cls.model,id=id)
    
    @classmethod
    def create_company_metrics(cls, *, payload: Dict) -> models.Model:
        response = cls.model.objects.create(**payload)
        return response
    @classmethod
    def put(cls, id: int, payload: dict) -> models.Model:
            """
            Atualiza um registro existente com base nos campos fornecidos no payload.
            Apenas os campos enviados são atualizados.
            """

            instance = cls.get(id=id)

            # Exclui os campos não enviados para evitar sobrescrever com None
            filtered_payload = {k: v for k, v in payload.items() if v is not None}

            for key, value in filtered_payload.items():
                setattr(instance, key, value)


                instance.save()

            return instance
    
    @classmethod
    def get_by_date(cls, *, date_recorded: str, id: int) -> models.Model:
        try:
            return cls.model.objects.get(date_recorded=date_recorded, id=id)
        except Exception as e:
            raise e  
        
    

    @classmethod
    def update_by_date(cls, *, instance: models.Model, payload: Dict[str, Any]) -> Tuple[int, Dict[str, str]]:
        try:
            with transaction.atomic():
                for field, value in payload.items():
                    setattr(instance, field, value)  # Atualiza os campos dinamicamente
                
                instance.save()  # Salva no banco de dados

                return 200, {"message": "Métricas atualizadas com sucesso"}
        except Exception as e:
            return 500, {"error": str(e)}

        

    @classmethod
    def delete(
        cls, *, instance: models.Model
        ) -> models.Model:
        instance.delete()
        return instance
    
class RecordRepository:
        """
        Repositório para a modelagem de Enterprise.
        Gerencia operações CRUD no banco de dados.
        """

        model = Record
        @classmethod
        def get(cls, *, id: int) -> models.Model:
            """
            Retorna uma empresa específica pelo ID ou lança um erro 404.
            """
            object = get_object_or_404(cls.model, id=id)
      
            return object
        
        @classmethod
        def list(cls)-> models.QuerySet:
            """
            Retorna todas as empresas ordenadas por ID.
            """
            return cls.model.objects.all().order_by("id")
        
        @classmethod
        def post(cls, *, payload: Dict) -> models.Model:
            id = payload["enterprise"]
            enterprise = EnterpriseRepository.get(id=payload["enterprise"])
            payload["enterprise"] = enterprise
            response = cls.model.objects.create(**payload)
            return response
        
        @classmethod
        def put(cls, id: int, payload: dict) -> models.Model:
            """
            Atualiza um registro existente com base nos campos fornecidos no payload.
            Apenas os campos enviados são atualizados.
            """

            instance = cls.get(id=id)

            # Exclui os campos não enviados para evitar sobrescrever com None
            filtered_payload = {k: v for k, v in payload.items() if v is not None}

            for key, value in filtered_payload.items():
                setattr(instance, key, value)


                instance.save()

            return instance
        
        @classmethod
        def delete(cls, instance: models.Model) -> models.Model:
            
            instance.delete()
            return instance
        
        @classmethod
        def search(cls, *, search: str) -> models.QuerySet:
            return cls.model.objects.filter(
                Q(name__istartswith=search)
            )