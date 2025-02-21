from decimal import Decimal
from django.http import HttpResponse
from ninja import Query
from ninja_extra import api_controller, route,http_get

from modules.enterprise.models import CompanyMetrics, Enterprise
from .services import DataAnalisysService
from django.db.models.query import QuerySet
from typing import Any
from django.db.models import Sum
from .schemas import CaptableResponse,ErrorResponse
import csv

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
            enterprise = Enterprise.objects.get(enterprise_id=enterprise_id)
            metrics = CompanyMetrics.objects.filter(enterprise=enterprise).order_by("-date_recorded", "-created_time").first()

            if not metrics:
                return 404, ErrorResponse(message="No metrics found for this enterprise")

            if not metrics.investment_round_open:
                return 400, ErrorResponse(message="The investment round for this enterprise is closed.")

            captable_percentage = float(metrics.captable or 0.0)

            value_investment = float(enterprise.investment_value or Decimal(0))

            value_foment_total = float(
                CompanyMetrics.objects.filter(enterprise=enterprise).aggregate(
                    total_foment=Sum('value_foment')
                )['total_foment'] or Decimal(0)
            )

            total_invested = value_investment + value_foment_total  

            capital_needed = float(metrics.capital_needed or Decimal(0))

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
            enterprise = Enterprise.objects.get(enterprise_id=enterprise_id)

            if not enterprise.foundation_year:
                return 400, ErrorResponse(message="Enterprise foundation year is missing.")

            metrics = CompanyMetrics.objects.filter(enterprise=enterprise).order_by("date_recorded")

            if not metrics.exists():
                return 404, ErrorResponse(message="No financial records found for this enterprise.")

            years = [enterprise.foundation_year]  # O primeiro ano sempre será o ano de fundação
            capital_values = [float(enterprise.investment_value or 0)]  # Primeiro valor será o investimento inicial

            for metric in metrics:
                year = metric.date_recorded.year
                if year not in years: 
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
            enterprise = Enterprise.objects.get(enterprise_id=enterprise_id)

            metrics = CompanyMetrics.objects.filter(enterprise=enterprise).order_by("date_recorded")

            if not metrics.exists():
                return 404, ErrorResponse(message="No client data found for this enterprise.")

            years = []
            new_clients_data = []

           
            for metric in metrics:
                year = metric.date_recorded.year
                if year not in years: 
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
           
            enterprise = Enterprise.objects.get(enterprise_id=enterprise_id)
            print("passou até aqui")

           
            metrics = CompanyMetrics.objects.filter(enterprise=enterprise).order_by("date_recorded")

            if not metrics.exists():
                return 404, ErrorResponse(message="No team size data found for this enterprise.")
           
            years = []
            team_size_data = []

            
            for metric in metrics:
                year = metric.date_recorded.year
                if year not in years: 
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

    @http_get("/download-company-data")
    def download_company_data(self, enterprise_id: int = Query(...)):
        try:
           
            enterprise = Enterprise.objects.get(enterprise_id=enterprise_id)
            
           
            metrics = CompanyMetrics.objects.filter(enterprise=enterprise).order_by("date_recorded")
            
           
            response = HttpResponse(content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{enterprise.name}_data.csv"'
            
          
            writer = csv.writer(response)
            
           
            writer.writerow([
                'Date Recorded', 'Current Capital', 'Capital Needed', 'Investment Value', 'Value Foment', 'New Clients', 'Team Size', 'Captable'
            ])
            
           
            for metric in metrics:
                writer.writerow([
                    metric.date_recorded,
                    metric.current_capital or '-',
                    metric.capital_needed or '-',
                    metric.enterprise.investment_value or '-',
                    metric.value_foment or '-',
                    metric.new_clients or '-',
                    metric.team_size or '-',
                    metric.captable or '-'
                ])
            
            return response
        except Enterprise.DoesNotExist:
            return HttpResponse("Enterprise not found", status=404)
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=500)

    @http_get("/partners-history", response={200: Any, 404: ErrorResponse, 500: ErrorResponse})
    def get_partners_history(self, enterprise_id: int = Query(...)):
        """
        Endpoint para retornar a evolução da quantidade de sócios ao longo dos anos.
        """
        try:
            # Buscar a empresa pelo ID
            enterprise = Enterprise.objects.get(enterprise_id=enterprise_id)
            print(f"enterprise: {enterprise.__dict__}")
            # Filtrar os registros de métricas da empresa ordenados por data
            metrics = CompanyMetrics.objects.filter(enterprise=enterprise)


            if not metrics.exists():
                return 404, ErrorResponse(message="No partners data found for this enterprise.")

            # Estruturas para armazenar os anos e quantidade de sócios
            years = []
            partners_data = []
            print(f"metrics: {metrics.__dict__}" )
            # Percorrer os registros e organizar os dados por ano
            for metric in metrics:
                year = metric.date_recorded.year
                if year not in years:
                    years.append(year)
                    partners_data.append(int(metric.partners_count or 0))

            # Retorno dos dados no formato esperado para visualização
            return {
                "xAxis": [{"data": years}],
                "series": [{"data": partners_data}],
                "width": 500,
                "height": 300
            }

        except Enterprise.DoesNotExist:
            return 404, ErrorResponse(message="Enterprise not found")

        except Exception as e:
            return 500, ErrorResponse(message=f"Error: {str(e)}")
