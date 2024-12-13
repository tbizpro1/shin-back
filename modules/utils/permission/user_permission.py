from django.http import HttpRequest
from ninja_extra.controllers import ControllerBase
from ninja_extra.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser


class BaseAcess(BasePermission):

    message = "Você não tem permissão para acessar este recurso"
    
    ROLE_USER: str
    
    def has_permission(self, request: HttpRequest, controller: ControllerBase) -> bool:
        if request.user.is_superuser:
            return True
        
        role = getattr(request.user, 'role', None)
        
        if role == self.ROLE_USER:
            return role
        
        return False