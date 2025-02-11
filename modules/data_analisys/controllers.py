from decimal import Decimal
from ninja_extra import api_controller, route

from modules.enterprise.models import CompanyMetrics, Enterprise
from .services import DataAnalisysService
from django.db.models.query import QuerySet
from typing import Any
from django.db.models import Sum
from .schemas import CaptableResponse,ErrorResponse
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
    
    @route.get("/captable", response={200: CaptableResponse, 404: ErrorResponse, 500: ErrorResponse})
    def get_captable_data(self, request, enterprise_id: int):
        try:
            # Obter dados da empresa
            enterprise = Enterprise.objects.get(enterprise_id=enterprise_id)
            metrics = CompanyMetrics.objects.filter(enterprise=enterprise).last()

            if not metrics:
                return 404, ErrorResponse(message="No metrics found for this enterprise")

            # Valores do modelo
            value_investment = float(enterprise.investment_value or Decimal(0))  # Novo nome do campo
            value_foment_total = float(
                CompanyMetrics.objects.filter(enterprise=enterprise).aggregate(
                    total_foment=Sum('value_foment')
                )['total_foment'] or Decimal(0)
            )
            total_invested = value_investment + value_foment_total  # Soma investimento + fomento

            # Meta de capital
            capital_needed = float(metrics.capital_needed or Decimal(0))

            # Progresso (evitar divisão por zero)
            progress_percentage = (total_invested / capital_needed * 100) if capital_needed > 0 else 0

            # Retorna os dados formatados no esquema CaptableResponse
            return CaptableResponse(
                enterprise_id=enterprise.enterprise_id,
                capital_needed=capital_needed,
                value_investment=value_investment,  # Nome correto agora
                value_foment_total=value_foment_total,
                total_invested=total_invested,
                progress_percentage=round(progress_percentage, 2),
            )
        except Enterprise.DoesNotExist:
            return 404, ErrorResponse(message="Enterprise not found")
        except Exception as e:
            return 500, ErrorResponse(message=f"Error: {str(e)}")
