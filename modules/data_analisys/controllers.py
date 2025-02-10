from ninja_extra import api_controller, route
from .services import DataAnalisysService
from django.db.models.query import QuerySet
from typing import Any

@api_controller(
    '/data_analisys',
    tags=['Rota - Analise de Dados'],
)
class DataAnalisysController:
    """
    Controller para gerenciar operações relacionadas ao modelo Enterprise.
    """
    @route.get("/discovery-source-distribution")
    def get_discovery_source_distribution(self)-> dict:
        """
        Endpoint para retornar a distribuição de startups por fonte de descoberta.
        """
        return DataAnalisysService.discovery_source_distribution()    
