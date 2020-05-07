import csv
import dataclasses
import datetime
import enum

from golinx.models import model

@dataclasses.dataclass
class User(model.Model):
    table_name: dataclasses.InitVar[str] = 'user'
    username: str = None
    password: str = None

    def validate(self):
        pass

