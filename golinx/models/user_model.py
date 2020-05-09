"""This module represents a user."""
import dataclasses
from typing import ClassVar

from golinx.models import base_model

@dataclasses.dataclass
class UserModel(base_model.BaseModel):
    table_name: ClassVar[str] = 'user'
    username: str = None
    password: str = None

    def validate(self):
        pass

