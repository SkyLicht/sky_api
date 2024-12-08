from pydantic import BaseModel


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