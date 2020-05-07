import dataclasses
import datetime
import enum
from typing import Iterable, Optional

from golinx.models import model


class LinkType(enum.Enum):
    UNKNOWN = 0
    CUSTOM = 1
    SHORT = 2


@dataclasses.dataclass
class Link(model.Model):
    table_name: dataclasses.InitVar[str] = 'link'
    owner_id: int = -1
    type: Optional[LinkType] = LinkType.CUSTOM
    original_path: str = None
    canonical_path: str = None
    destination: str = None
    other_owners: Optional[Iterable[str]] = dataclasses.field(default_factory=list)
    readers: Optional[Iterable[str]] = dataclasses.field(default_factory=list)
    title: Optional[str] = None
    description: Optional[str] = None

    def validate(self):
        pass
