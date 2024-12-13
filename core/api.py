from ninja import Swagger
from ninja_extra import NinjaExtraAPI
from ninja_jwt.authentication import JWTAuth
from django.contrib.admin.views.decorators import staff_member_required



from modules.user.controllers import UsersController
from modules.token.controllers import TokenController


api = NinjaExtraAPI(
    title="Shin API V1",
    version="1.0.0",
    description="Nossa API",
    app_name="shin",
    auth=JWTAuth(),
    urls_namespace="shin-api-v1",  # Evita conflitos
    docs=Swagger(
        settings={
            'docExpansion': 'none',
            'tagsSorter': 'alpha',
            'filter': True,
            'syntaxHighlight': {
                'theme': 'monokai',
                'activate': True,
            },
            'persistAuthorization': True,
        }
    )
)

# User Controllers
api.register_controllers(UsersController)

# Core Controllers
api.register_controllers(TokenController)