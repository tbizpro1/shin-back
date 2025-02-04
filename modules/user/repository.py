import os
from typing import Dict, Optional
from core import settings
from ninja import UploadedFile, File
from modules.user.models import User
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from django.db import models
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password


class Repository:
    
    model = User
    
    @classmethod
    def list(cls) -> models.QuerySet:
        return cls.model.objects.all().order_by("id")
    
    @classmethod
    def get(cls, *, id: int) -> models.Model:
        return get_object_or_404(cls.model, id=id)
    
    @classmethod
    def filter_by_name(cls, name: str):
        return cls.model.objects.filter(name__icontains=name).values_list('id', flat=True)


    @classmethod
    def password_hash(cls, password: str) -> str:
        password_hashed = make_password(password)
        return password_hashed

    @classmethod
    def update_payload(
        cls, *, payload: Dict, **kwargs
    ) -> Dict:
        
        if "password" in payload:
            payload["password"] = cls.password_hash(payload["password"])
        
        if "role" in payload and payload["role"] == "admin":
            payload["is_superuser"] = True
            payload["is_staff"] = True
        else:
            payload["is_superuser"] = False
            payload["is_staff"] = False
            
        
        updated_payload: Dict = {
            **payload
        }
        return updated_payload
    
    @classmethod
    def post(cls, *, payload: Dict, file: Optional[UploadedFile] = File(None), **kwargs) -> models.Model:
        
        if file:
            try:
                upload_response = upload(file, folder="profile_pictures/")
                file_url = upload_response.get("secure_url")
                payload["profile_picture"] = file_url
            except Exception as e:
                raise e
        
        payload = cls.update_payload(payload=payload)
        return cls.model.objects.create(**payload)
    
    @classmethod
    def put(
        cls,
        *,
        id: int,
        instance: models.Model,
        payload: Dict,
        **kwargs
    ) -> models.Model:
        
        instance = cls.get(id=id)
    
        for attr, value in payload.items():
            if value:
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
    def get(cls, *, id: int) -> models.Model:
        """
        Retorna um user pelo ID ou lança um erro 404.
        """
        return get_object_or_404(cls.model, id=id)
    
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