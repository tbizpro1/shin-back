from ninja import Schema
from ninja.schema import DjangoGetter
from pydantic import model_validator, ValidationInfo
from ninja_jwt.schema import TokenObtainPairInputSchema
from modules.user.schemas import UserListSchema


class CustomTokenOutObtain(Schema):
    token: str
    user: UserListSchema


class CustomTokenObtain(TokenObtainPairInputSchema):
    @model_validator(mode="before")
    def validate_inputs(cls, values: DjangoGetter, info: ValidationInfo) -> DjangoGetter:
        input_values = values._obj
        request = values._context.get('request')
        if isinstance(input_values, dict):
            values._obj.update(
                cls.validate_values(request=request, values=input_values)
            )
            return values
        return values
    
    def output_schema(self) -> CustomTokenOutObtain:
        token = getattr(self.to_response_schema(), 'access', None)
        user_schema = UserListSchema.from_orm(self._user)
        return CustomTokenOutObtain(token=token, user=user_schema)

        