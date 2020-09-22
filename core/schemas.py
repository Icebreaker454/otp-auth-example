from typing import Any

from pydantic import BaseModel


class CommonErrorSchema(BaseModel):
    code: str
    message: str
    additional_info: Any
