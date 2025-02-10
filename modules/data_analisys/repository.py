from django.db.models import Count,Sum
from ..enterprise.models import Enterprise, Record
from django.db.models.functions import TruncDate

class DataAnalisysRepository:
    """
    Repositório para operações relacionadas ao análise de dados.   
    """

    @staticmethod
    def get_discovery_source_distribution():
        """
        Retorna a contagem de startups por fonte de descoberta.
        Substitui valores `None` por 'Desconhecido'.
        """
        queryset = (
            Enterprise.objects.values('discovered_startup')
            .annotate(count=Count('enterprise_id'))
            .order_by('-count')
        )

        # Substituir `None` por "Desconhecido"
        return [
            {"discovered_startup": item["discovered_startup"] or "Desconhecido", "count": item["count"]}
            for item in queryset
        ]
    
    @staticmethod
    def get_initial_maturity_distribution():
        """
        Retorna a contagem de startups por estágio de negócio ('initial_maturity').
        Consolida dados tanto da tabela Enterprise quanto da tabela Record.
        Substitui valores None por 'Desconhecido'.
        """
        enterprise_queryset = (
            Enterprise.objects.values('initial_maturity')
            .annotate(count=Count('enterprise_id'))
        )

        record_queryset = (
            Record.objects.values('initial_maturity')
            .annotate(count=Count('id'))
        )

        # Criar um dicionário consolidado
        maturity_distribution = {}

        for item in enterprise_queryset:
            key = item["initial_maturity"] or "Desconhecido"
            maturity_distribution[key] = maturity_distribution.get(key, 0) + item["count"]

        for item in record_queryset:
            key = item["initial_maturity"] or "Desconhecido"
            maturity_distribution[key] = maturity_distribution.get(key, 0) + item["count"]

        # Converter para lista ordenada por contagem
        return sorted(
            [{"initial_maturity": key, "count": count} for key, count in maturity_distribution.items()],
            key=lambda x: x["count"],
            reverse=True
        )
    
    @staticmethod
    def get_revenue_trend():
        """
        Retorna a evolução da receita ao longo do tempo, agrupada por `date_recorded`.
        """
        queryset = (
            Record.objects.annotate(date=TruncDate('date_recorded'))
            .values('date')
            .annotate(total_revenue=Sum('revenue'))
            .order_by('date')
        )

        return [{"date": item["date"], "total_revenue": item["total_revenue"]} for item in queryset]