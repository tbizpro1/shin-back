from ninja import Swagger
from ninja_extra import NinjaExtraAPI
from ninja_jwt.authentication import JWTAuth
from django.contrib.admin.views.decorators import staff_member_required


from modules.enterprise.controllers import EnterpriseController, RecordController
from modules.user_enterprise.controllers import UserEnterpriseController
from modules.user.controllers import UsersController
from modules.token.controllers import TokenController
from modules.logs.controllers import LogController
from modules.enterprise.controllers import CompanyMetricsController
from modules.data_analisys.controllers import DataAnalisysController
api = NinjaExtraAPI(
    title="Shin API V1",
    version="1.0.0",
    description="Nossa API",
    app_name="shin",
    auth=JWTAuth(),
    urls_namespace="shin-api-v1",  
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

# Log Controllers
api.register_controllers(LogController)

# Core Controllers
api.register_controllers(TokenController)

# Enterprise Controllers
api.register_controllers(EnterpriseController)

# User_Enterprise Controllers
api.register_controllers(UserEnterpriseController)

#CompanyMetrics Controllers
api.register_controllers(CompanyMetricsController)

#Record Controllers
api.register_controllers(RecordController)

#DataAnalisys Controllers
api.register_controllers(DataAnalisysController)