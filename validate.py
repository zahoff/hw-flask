from pydantic import BaseModel, ValidationError
from sqlalchemy import DateTime

from errors import ApiException


class CreateUserSchema(BaseModel):
    email: str
    password: str


class CreateAdvtSchema(BaseModel):
    title: str
    description: str
    # created_at: DateTime
    user_id: int

    class Config:
        arbitrary_types_allowed = True


def validate(data: dict, schema_class):
    try:
        return schema_class(**data).dict()
    except ValidationError as er:
        return ApiException(400, er.errors())