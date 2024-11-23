from typing import Optional

from pydantic import BaseModel


class TokenModel(BaseModel):
    access_token: str
    token_type: str

class TokenDataModel(BaseModel):
    username: Optional[str] = None