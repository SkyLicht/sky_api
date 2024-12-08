from core.data.models.user_model import UserModel
from core.data.schemas.hour_by_hour_schema import HourByHourSchema
from core.data.models.hour_by_hour_model import HourByHourModel
from core.data.schemas.user_schema import UserSchema


def translate_hour_by_hour_schema_to_model(schema) -> HourByHourModel:
    return HourByHourModel(
        id=schema.id,
        factory=schema.factory,
        line=schema.line,
        date=schema.date,
        hour=schema.hour,
        smt_in=schema.smt_in,
        smt_out=schema.smt_out,
        packing=schema.packing
    )


def translate_hour_by_hour_model_to_schema(model) -> HourByHourSchema:
    return HourByHourSchema(
        line=model.line,
        factory=model.factory,
        date=model.date,
        hour=model.hour,
        smt_in=model.smt_in,
        smt_out=model.smt_out,
        packing=model.packing)

def translate_hour_by_hour_schema_list_to_model_list(schema_list) -> list[HourByHourModel]:
    return [translate_hour_by_hour_schema_to_model(schema) for schema in schema_list]

def translate_hour_by_hour_model_list_to_schema_list(model_list) -> list[HourByHourSchema]:
    return [translate_hour_by_hour_model_to_schema(model) for model in model_list]



def translate_user_schema_to_model(user_schema: UserSchema) -> UserModel:
    """
    Converts a SQLAlchemy UserSchema object to a Pydantic User model.

    Args:
        user_schema (UserSchema): The SQLAlchemy schema object.

    Returns:
        User: The Pydantic model object.
    """
    return UserModel(
        id=user_schema.id,
        username=user_schema.username,
        is_active=user_schema.is_active,
        roles=[role.name for role in user_schema.roles],
        routes=[route.path for route in user_schema.routes]
    )