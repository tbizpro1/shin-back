from ninja import Schema

class CaptableResponse(Schema):
    enterprise_id: int
    capital_needed: float
    value_foment_total: float
    total_invested: float
    progress_percentage: float
    value_investment: float 


class ErrorResponse(Schema):
    message: str