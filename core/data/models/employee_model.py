from pydantic import BaseModel

from core.data.schemas.all_schemas import LineSchema


class LineModel(BaseModel):
    id: str
    name: str
    factory: str
    is_active: bool

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "factory": self.factory,
            "is_active": self.is_active
        }

    def __str__(self):
        return str(self.to_dict())

    def to_schema(self) -> LineSchema:
        return LineSchema(
            name=self.name,
            factory=self.factory,
            is_active=self.is_active
        )

    @classmethod
    def from_schema(cls, schema: LineSchema) -> 'LineModel':
        return cls(
            id=schema.id,
            name=schema.name,
            factory=schema.factory,
            is_active=schema.is_active
        )
