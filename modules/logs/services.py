from .models import Log

class LogService:
    @staticmethod
    def create_log(user_id, description, change_type):
        """
        Cria um log no sistema. Se houver mais de 10 logs, remove o mais antigo antes de criar um novo.
        
        Args:
            user_id (int): ID do usuário relacionado ao log.
            description (str): Descrição da ação.
            change_type (str): Tipo de mudança ('create', 'update', etc.).
        """
        logs = Log.objects.filter(user_id=user_id).order_by("created_at")  # Ordena do mais antigo para o mais novo
        if logs.count() >= 10:
            logs.first().delete()  # Exclui o log mais antigo

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

