from ninja_extra import api_controller, route
from typing import List
from ..logs.services import LogService
from ..logs.schemas import LogSchema, ErrorResponse


@api_controller(
    '/logs',
    tags=['Rota - Logs'],
)
class LogController:
    """
    Controller para gerenciar operações relacionadas ao modelo Log.
    """

    log_service = LogService()

    @route.get('/{user_id}', response=List[LogSchema], summary="Listar Logs de um Usuário")
    def list_user_logs(self, user_id: int):
        """
        Lista todos os logs associados a um usuário específico pelo ID.
        """
        try:
            logs = self.log_service.get_logs_by_user_id(user_id)
            serialized_logs = [
            {
                "user_id": log.user.id,  # Mapear explicitamente o user para user_id
                "description": log.description,
                "change_type": log.change_type,
                "created_at": log.created_at.isoformat(),
            }
            for log in logs
        ]

            return serialized_logs
        except Exception as e:
            return ErrorResponse(message=f"Erro ao listar logs: {str(e)}", status_code=400)
