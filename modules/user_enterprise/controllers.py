from ninja_extra import api_controller, route
from typing import List, Optional
from modules.user_enterprise.repository import UserEnterpriseRepository
from modules.user_enterprise.schemas import (
    UserEnterpriseListSchema,
    UserEnterprisePostSchema,
    UserEnterprisePutSchema,
    ErrorResponse,
)
from datetime import datetime
from django.http import Http404
from modules.user_enterprise.models import UserEnterprise
from ninja import Schema
from pydantic import Field
from ninja import Query
from ..logs.services import LogService
from ..user.repository import Repository as UserRepository
from django.core.mail import send_mail
from django.urls import reverse
from django.shortcuts import render


# Filtro de consulta para as relações UserEnterprise
class Filters(Schema):
    limit: int = 100  
    offset: Optional[int] = None  
    username: Optional[str] = None 
    status: Optional[str] = None  
    enterprise_name__in: Optional[List[str]] = Field(None, alias="enterprise_names")


@api_controller(
    '/user-enterprises',
    tags=['Rota - User Enterprises']
)
class UserEnterpriseController:
    log_service = LogService()  # Instância do LogService
    repository = UserEnterpriseRepository

    @staticmethod
    def handle_invitation(request, token):
        try:
            invitation = UserEnterprise.objects.get(token=token)
        except UserEnterprise.DoesNotExist:
            raise Http404("Convite não encontrado.")

        if request.method == "POST":
            action = request.POST.get("action")  # "accepted" ou "declined"
            if action == "accepted":
                invitation.status = "accepted"
                invitation.accept_at = datetime.now()
                message = f"Você aceitou o convite para a empresa {invitation.enterprise.name}."
            elif action == "declined":
                invitation.status = "declined"
                message = f"Você recusou o convite para a empresa {invitation.enterprise.name}."
            else:
                return render(request, "accept_email/accept_email.html", {"error_message": "Ação inválida."})

            invitation.save()
            return render(request, "accept_email/accept_email.html", {"success_message": message, "enterprise_name": invitation.enterprise.name})

        return render(request, "accept_email/accept_email.html", {"enterprise_name": invitation.enterprise.name})

    @route.get('', response={200: List[UserEnterpriseListSchema]})
    def list(self, request, filters: Query[Filters]):
        """
        Lista as relações UserEnterprise com filtros opcionais.
        """
        user_enterprises = self.repository.list()

        if filters.username:
            user_enterprises = [ue for ue in user_enterprises if ue.user.username == filters.username]

        if filters.status:
            user_enterprises = [ue for ue in user_enterprises if ue.status == filters.status]

        if filters.enterprise_name__in:
            user_enterprises = [ue for ue in user_enterprises if ue.enterprise.name in filters.enterprise_name__in]

        if filters.offset is not None:
            user_enterprises = user_enterprises[filters.offset:]

        user_enterprises = user_enterprises[:filters.limit]

        return [
            {
                "ue_id": ue.ue_id,
                "user_id": ue.user.id,
                "username": ue.user.username,
                "enterprise_id": ue.enterprise.enterprise_id,
                "enterprise_name": ue.enterprise.name,
                "role": ue.role,
                "status": ue.status,
                "token": ue.token,
            }
            for ue in user_enterprises
        ]

    @route.get('/{id}', response={200: UserEnterpriseListSchema, 404: ErrorResponse})
    def get(self, request, id: int):
        """
        Retorna os detalhes de uma relação UserEnterprise pelo ID.
        """
        user_enterprise = self.repository.get(id=id)
        return {
            "ue_id": user_enterprise.ue_id,
            "user_id": user_enterprise.user.id,
            "username": user_enterprise.user.username,
            "enterprise_id": user_enterprise.enterprise.enterprise_id,
            "enterprise_name": user_enterprise.enterprise.name,
            "role": user_enterprise.role,
            "status": user_enterprise.status,
        }

    @route.post('', response={200: UserEnterpriseListSchema, 500: ErrorResponse})
    def post(self, request, payload: UserEnterprisePostSchema):
        """
        Cria uma nova relação UserEnterprise.
        """
        base_url = request.build_absolute_uri('/')[:-1].strip("/")
        user_email = UserRepository.get(id=payload.user_id).email

        user_enterprise = self.repository.post(payload=payload.dict())
        self.log_service.create_log(
            user_id=user_enterprise.user.id, 
            change_type="post", 
            description=f'Você foi convidado para participar da {user_enterprise.enterprise.name}.'
        )

        token = user_enterprise.token
        link_response = request.build_absolute_uri(reverse("accept_email", kwargs={"token": token}))
        enterprise_name = user_enterprise.enterprise.name
        accept_invitation_link = f"{base_url}{token}/?status=accepted"
        decline_invitation_link = f"{base_url}{token}/?status=declined"

        response = send_mail(
            subject=f"Convite para participar da {enterprise_name}",
            message="",
            from_email="noreply@shin.com",
            recipient_list=[user_email],
            html_message=f"""
            <!DOCTYPE html>
            <html lang="pt-BR">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Convite para Participar</title>
                <style>
                    body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; }}
                    .email-container {{ max-width: 600px; margin: 20px auto; background-color: #ffffff; border-radius: 8px; }}
                    .email-header {{ background-color: #007bff; color: #ffffff; padding: 20px; text-align: center; }}
                    .email-body {{ padding: 20px; color: #333; }}
                    .email-body a {{ text-decoration: none; background-color: #007bff; color: #fff; padding: 10px 20px; border-radius: 4px; margin-right: 10px; }}
                    .email-body a.decline {{ background-color: #dc3545; }}
                </style>
            </head>
            <body>
                <div class="email-container">
                    <div class="email-header">
                        <h1>Convite para Participar</h1>
                    </div>
                    <div class="email-body">
                        <p>Olá,</p>
                        <p>Você foi convidado para participar da <strong>{enterprise_name}</strong>.</p>
                        <a href="{link_response}" target="_blank">Responder convite</a>
                        <p>Ou copie o seguinte código e insira no aplicativo:</p>
                        <p style="font-weight: bold; font-size: 18px;">{token}</p>
                        <p>Se você não esperava este convite, pode ignorar este e-mail.</p>
                        <p>Atenciosamente,<br><strong>{enterprise_name}</strong></p>
                    </div>
                </div>
            </body>
            </html>
            """
        )

        return {
            "ue_id": user_enterprise.ue_id,
            "user_id": user_enterprise.user.id,
            "username": user_enterprise.user.username,
            "enterprise_id": user_enterprise.enterprise.enterprise_id,
            "enterprise_name": user_enterprise.enterprise.name,
            "role": user_enterprise.role,
            "status": user_enterprise.status,
            "token": user_enterprise.token,
        }

    @route.put('/{id}', response={200: UserEnterpriseListSchema, 400: ErrorResponse, 500: ErrorResponse})
    def put(self, request, id: int, payload: UserEnterprisePutSchema):
        """
        Atualiza os dados de uma relação UserEnterprise existente.
        """
        user_enterprise = self.repository.put(id=id, payload=payload.dict(exclude_unset=True))
        return {
            "ue_id": user_enterprise.ue_id,
            "user_id": user_enterprise.user.id,
            "username": user_enterprise.user.username,
            "enterprise_id": user_enterprise.enterprise.enterprise_id,
            "enterprise_name": user_enterprise.enterprise.name,
            "role": user_enterprise.role,
            "status": user_enterprise.status,
        }

    @route.put('/invitation/{token}/', response={200: UserEnterpriseListSchema, 404: ErrorResponse})
    def accept(self, request, token: str, status: str):
        """
        Endpoint para aceitar ou recusar um convite utilizando um token único.
        """
        if status not in ["accepted", "declined"]:
            return 404, {"message": "Status inválido. Escolha 'accepted' ou 'declined'."}

        try:
            invitation = UserEnterprise.objects.get(token=token)
        except UserEnterprise.DoesNotExist:
            raise Http404("Convite não encontrado.")

        if invitation.status != "pending":
            return 404, {"message": "Convite já foi tratado."}

        invitation.status = status
        if status == "accepted":
            self.log_service.create_log(
                user_id=request.user.id,
                change_type="post",
                description=f"Você aceitou o convite da empresa {invitation.enterprise.name}."
            )
            invitation.accept_at = datetime.now()
        elif status == "declined":
            self.log_service.create_log(
                user_id=request.user.id,
                change_type="post",
                description=f"Você recusou o convite da empresa {invitation.enterprise.name}."
            )

        invitation.save()
        return {
            "ue_id": invitation.ue_id,
            "user_id": invitation.user.id,
            "enterprise_id": invitation.enterprise.enterprise_id,
            "enterprise_name": invitation.enterprise.name,
            "status": invitation.status,
        }

        

    @route.delete('/{id}', response={204: None})
    def delete(self, request, id: int):
        """
        Deleta uma relação UserEnterprise pelo ID.
        """
        self.repository.delete(id=id)
        return None

    @route.get('/user/{user_id}', response={200: List[UserEnterpriseListSchema]})
    def list_by_user(self, request, user_id: int):
        """
        Retorna todas as relações UserEnterprise associadas a um usuário específico.
        """
        user_enterprises = self.repository.list_by_user(user_id=user_id)
        return [
            {
                "ue_id": ue.ue_id,
                "user_id": ue.user.id,
                "username": ue.user.username,
                "enterprise_id": ue.enterprise.enterprise_id,
                "enterprise_name": ue.enterprise.name,
                "role": ue.role,
                "token": ue.token,
                "status": ue.status,
            }
            for ue in user_enterprises
        ]

    @route.get('/enterprise/{enterprise_id}', response={200: List[UserEnterpriseListSchema]})
    def list_by_enterprise(self, request, enterprise_id: int):
        """
        Retorna todas as relações UserEnterprise associadas a uma empresa específica.
        """
        user_enterprises = self.repository.list_by_enterprise(enterprise_id=enterprise_id)
        return [
            {
                "ue_id": ue.ue_id,
                "user_id": ue.user.id,
                "username": ue.user.username,
                "enterprise_id": ue.enterprise.enterprise_id,
                "enterprise_name": ue.enterprise.name,
                "role": ue.role,
                "status": ue.status,
            }
            for ue in user_enterprises
        ]
