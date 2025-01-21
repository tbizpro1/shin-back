from .models import Log

class LogService:
    @staticmethod
    def create_log(user_id, description, change_type):
        """
        Cria um log no sistema.
        
        Args:
            user_id (int): ID do usuário relacionado ao log.
            description (str): Descrição da ação.
            change_type (str): Tipo de mudança ('create', 'update', etc.).
        """
        Log.objects.create(
            user_id=user_id,
            description=description,
            change_type=change_type
        )

    @staticmethod
    def get_logs_by_user_id( user_id: int):
        """
        Busca todos os logs associados a um usuário específico pelo ID.
        """
        return Log.objects.filter(user_id=user_id).all()

