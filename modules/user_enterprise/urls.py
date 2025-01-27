from django.urls import path
from .controllers import UserEnterpriseController

urlpatterns = [
    path("response-invite/<str:token>/", UserEnterpriseController.handle_invitation, name="accept_email"),
]
