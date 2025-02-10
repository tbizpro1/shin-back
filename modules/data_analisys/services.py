from ninja_extra import status
from django.db import transaction
from typing import List, Optional, Dict, Any, Tuple, Union
from django.db import IntegrityError, models
from django.http import Http404
from ..enterprise.repository import RecordRepository,EnterpriseRepository
from .repository import DataAnalisysRepository

class DataAnalisysService:
    
    repositoryEnterprise = EnterpriseRepository
    
    # repositoryMetrics = MetricsRepository

    repositoryRecord = RecordRepository

    @staticmethod
    def discovery_source_distribution():
        """
        Retorna a distribuição de startups por fonte de descoberta no formato adequado.
        """
        data_discovery = DataAnalisysRepository.get_discovery_source_distribution()
        print(f"Dataaa: {data_discovery}")

        data_initial_maturity = DataAnalisysRepository.get_initial_maturity_distribution()
        print(f"Dataaa: {data_initial_maturity}")
        # Formata os dados para o frontend
        return {
            "labels": [item["discovered_startup"] for item in data_discovery],
            "data": [item["count"] for item in data_discovery],
        }