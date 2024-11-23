from core.data.schemas.hour_by_hour_schema import HourByHourSchema
from core.data.models.hour_by_hour_model import HourByHourModel


def translate_hour_by_hour_schema_to_model(schema) -> HourByHourModel:
    return HourByHourModel(
        id=schema.id,
        line=schema.line,
        date=schema.date,
        hour=str(schema.hour),
        smt_in=schema.smt_in,
        smt_out=schema.smt_out,
        packing=schema.packing
    )


def translate_hour_by_hour_model_to_schema(model) -> HourByHourSchema:
    return HourByHourSchema(
        line=model.line,
        date=model.date,
        hour=str(model.hour),
        smt_in=model.smt_in,
        smt_out=model.smt_out,
        packing=model.packing)

def translate_hour_by_hour_schema_list_to_model_list(schema_list) -> list[HourByHourModel]:
    return [translate_hour_by_hour_schema_to_model(schema) for schema in schema_list]

def translate_hour_by_hour_model_list_to_schema_list(model_list) -> list[HourByHourSchema]:
    return [translate_hour_by_hour_model_to_schema(model) for model in model_list]
