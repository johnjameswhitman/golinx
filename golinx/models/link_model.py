"""This represents a short-link."""
import dataclasses
import enum
import re
from typing import ClassVar, Iterable, Optional, Union
from urllib import parse

from golinx.models import base_model
from golinx.models import user_model


class LinkType(enum.Enum):
    UNKNOWN = 0
    CUSTOM = 1
    SHORT = 2

    @classmethod
    def coerce(cls, val: Union[int, str, 'LinkType']) -> 'LinkType':
        if type(val) in [int, cls]:
            return cls(val)
        elif type(val) == str:
            return cls[val]

        raise ValueError('Trying to coerce from invalid type {}.'.format(type(val)))

    def __repr__(self) -> str:
        """Provides a more application-specific serialization."""
        return self.name


@dataclasses.dataclass
class LinkModel(base_model.BaseModel):
    table_name: ClassVar[str] = 'link'
    # Below allows alphanumeric and dots or dashes.
    disallowed_path_chars: ClassVar[re.Pattern] = re.compile(r'[^0-9A-Za-z\.\-]')
    # The canonical path is alphanumeric.
    canonical_path_ignored_chars: ClassVar[re.Pattern] = re.compile(r'[^0-9A-Za-z]')
    owner_id: int = None
    link_type: str = 'CUSTOM'
    original_path: str = None
    canonical_path: str = None
    destination: str = None
    other_owners: Optional[str] = None
    readers: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None

    def validate(self):
        """Validates the fields on the link. Does not check ACLs."""
        # Delegated checks:
        # - The canonical_path must be unique (enforced by schema).
        # - Types must be correct (enforced by schema).
        # Owned checks:
        # - Destination must be a valid URL.
        url = parse.urlparse(self.destination)
        if not all([url.scheme, url.netloc]):
            raise base_model.ModelError(
                'Destination must be a valid URL, e.g. https://example.com/some/path.')

        # - Custom links cannot start with a dash, which is used to indicate shortlink.
        if LinkType.coerce(self.link_type) == LinkType.CUSTOM and self.original_path.startswith('-'):
            raise base_model.ModelError(
                'Custom golinx may not start with a dash. This is reserved for short links.')

        # - The original_path can only contain [0-9A-Za-z\-\.].
        if self.disallowed_path_chars.match(self.original_path):
            raise base_model.ModelError(
                'Custom golinx may only consist of alphanumeric characters, dots and dashes.')

        # - The canonical_path can only contain [0-9A-Za-z] (basically, drops dots and dashes).
        if self.disallowed_path_chars.match(self.original_path):
            raise base_model.ModelError(
                'Custom golinx canonical path may only consist of alphanumeric characters.')

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
