"""This represents a short-link."""
import dataclasses
import enum
from typing import ClassVar, Iterable, Optional

from golinx.models import base_model
from golinx.models import user_model


class LinkType(enum.Enum):
    UNKNOWN = 0
    CUSTOM = 1
    SHORT = 2


@dataclasses.dataclass
class LinkModel(base_model.BaseModel):
    table_name: ClassVar[str] = 'link'
    owner_id: Optional[int] = None
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

    @property
    def owner(self) -> user_model.UserModel:
        """Fetches the user record associated with the owner_id."""
        # TODO(john): Find a good way to cache this result but make it update
        # with changes to the associated owner and owner_id.
        if not self.db:
            raise ValueError('Set a valid db instance variable.')

        if self.owner_id:
            return user_model.UserModel.get(self.db, self.owner_id)

    @owner.setter
    def owner(self, owner: user_model.UserModel) -> None:
        """Sets the owner ID."""
        self.owner_id = owner.id
