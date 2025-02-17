from decimal import Decimal
from ninja import Query
from ninja_extra import api_controller, route,http_get

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
    # @route.get("/discovery-source-distribution")
    # def get_discovery_source_distribution(self)-> dict:
    #     """
    #     Endpoint para retornar a distribuição de startups por fonte de descoberta.
    #     """
    #     return DataAnalisysService.discovery_source_distribution()    
    
    @route.get("/captable", response={200: CaptableResponse, 404: ErrorResponse, 500: ErrorResponse, 400: ErrorResponse})
    def get_captable_data(self, request, enterprise_id: int):
        try:
            # Obter dados da empresa
            enterprise = Enterprise.objects.get(enterprise_id=enterprise_id)
            metrics = CompanyMetrics.objects.filter(enterprise=enterprise).order_by("-date_recorded", "-created_time").first()

            if not metrics:
                return 404, ErrorResponse(message="No metrics found for this enterprise")

            # Verifica se a rodada de investimento está aberta
            if not metrics.investment_round_open:
                return 400, ErrorResponse(message="The investment round for this enterprise is closed.")

            # Captable (retorna exatamente o que está armazenado)
            captable_percentage = float(metrics.captable or 0.0)
            print(f"Captable: {metrics.__dict__}")

            # Novo nome do campo de investimento
            value_investment = float(enterprise.investment_value or Decimal(0))

            # Soma do valor de fomento total
            value_foment_total = float(
                CompanyMetrics.objects.filter(enterprise=enterprise).aggregate(
                    total_foment=Sum('value_foment')
                )['total_foment'] or Decimal(0)
            )

            # Soma investimento + fomento
            total_invested = value_investment + value_foment_total  

            # Capital necessário
            capital_needed = float(metrics.capital_needed or Decimal(0))

            # Progresso percentual
            progress_percentage = (total_invested / capital_needed * 100) if capital_needed > 0 else 0

            return CaptableResponse(
                enterprise_id=enterprise.enterprise_id,
                capital_needed=capital_needed,
                value_investment=value_investment,  
                value_foment_total=value_foment_total,
                total_invested=total_invested,
                progress_percentage=captable_percentage
            )

        except Enterprise.DoesNotExist:
            return 404, ErrorResponse(message="Enterprise not found")

        except Exception as e:
            return 500, ErrorResponse(message=f"Error: {str(e)}")
    # @http_get("/partners-distribution")
    # def get_partners_distribution(self):
    #     """
    #     Endpoint para retornar a quantidade de sócios ao longo do tempo.
    #     """
    #     return DataAnalisysService.get_partners_distribution()
    
    @http_get("/team-size-distribution")
    def get_team_size_distribution(self, enterprise_id: int = Query(...)):
        """
        Endpoint para retornar a quantidade de colaboradores ao longo do tempo para uma empresa específica.
        """
        return DataAnalisysService.get_team_size_distribution(enterprise_id)
    
    @http_get("/capital-history")
    def get_capital_history(self, enterprise_id: int = Query(...)):
        """
        Endpoint para retornar a evolução do capital da empresa ao longo dos anos.
        """
        try:
            # Obtém a empresa pelo ID
            enterprise = Enterprise.objects.get(enterprise_id=enterprise_id)

            # Pega o ano de fundação da empresa
            if not enterprise.foundation_year:
                return 400, ErrorResponse(message="Enterprise foundation year is missing.")

            # Obtém todas as métricas ordenadas por ano
            metrics = CompanyMetrics.objects.filter(enterprise=enterprise).order_by("date_recorded")

            if not metrics.exists():
                return 404, ErrorResponse(message="No financial records found for this enterprise.")

            # Lista de anos e capitais
            years = [enterprise.foundation_year]  # O primeiro ano sempre será o ano de fundação
            capital_values = [float(enterprise.investment_value or 0)]  # Primeiro valor será o investimento inicial

            # Adiciona os anos e capitais registrados no CompanyMetrics
            for metric in metrics:
                year = metric.date_recorded.year
                if year not in years:  # Evita duplicar anos
                    years.append(year)
                    capital_values.append(float(metric.current_capital or 0))

            return {
                "xAxis": [{"data": years}],
                "series": [{"data": capital_values}],
                "width": 500,
                "height": 300
            }

        except Enterprise.DoesNotExist:
            return 404, ErrorResponse(message="Enterprise not found")

        except Exception as e:
            return 500, ErrorResponse(message=f"Error: {str(e)}")
        
    @http_get("/new-clients-history")
    def get_new_clients_history(self, enterprise_id: int = Query(...)):
        """
        Endpoint para retornar a evolução do número de novos clientes ao longo dos anos.
        """
        try:
            # Obtém a empresa pelo ID
            enterprise = Enterprise.objects.get(enterprise_id=enterprise_id)

            # Obtém todas as métricas ordenadas por ano
            metrics = CompanyMetrics.objects.filter(enterprise=enterprise).order_by("date_recorded")

            if not metrics.exists():
                return 404, ErrorResponse(message="No client data found for this enterprise.")

            # Lista de anos e número de novos clientes
            years = []
            new_clients_data = []

            # Adiciona os anos e número de novos clientes registrados no CompanyMetrics
            for metric in metrics:
                year = metric.date_recorded.year
                if year not in years:  # Evita duplicar anos
                    years.append(year)
                    new_clients_data.append(int(metric.new_clients or 0))

            return {
                "xAxis": [{"data": years}],
                "series": [{"data": new_clients_data}],
                "width": 500,
                "height": 300
            }

        except Enterprise.DoesNotExist:
            return 404, ErrorResponse(message="Enterprise not found")

        except Exception as e:
            return 500, ErrorResponse(message=f"Error: {str(e)}")

    @http_get("/team-size-history")
    def get_team_size_history(self, enterprise_id: int = Query(...)):
        """
        Endpoint para retornar a evolução do tamanho do time ao longo dos anos.
        """
        try:
            # Obtém a empresa pelo ID
            enterprise = Enterprise.objects.get(enterprise_id=enterprise_id)

            # Obtém todas as métricas ordenadas por ano
            metrics = CompanyMetrics.objects.filter(enterprise=enterprise).order_by("date_recorded")

            if not metrics.exists():
                return 404, ErrorResponse(message="No team size data found for this enterprise.")

            # Lista de anos e tamanho do time
            years = []
            team_size_data = []

            # Adiciona os anos e tamanho do time registrados no CompanyMetrics
            for metric in metrics:
                year = metric.date_recorded.year
                if year not in years:  # Evita duplicar anos
                    years.append(year)
                    team_size_data.append(int(metric.team_size or 0))

            return {
                "xAxis": [{"data": years}],
                "series": [{"data": team_size_data}],
                "width": 500,
                "height": 300
            }

        except Enterprise.DoesNotExist:
            return 404, ErrorResponse(message="Enterprise not found")

        except Exception as e:
            return 500, ErrorResponse(message=f"Error: {str(e)}")
