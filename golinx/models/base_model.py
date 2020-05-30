import csv
import dataclasses
import datetime
import sqlite3
from typing import Any, ClassVar, Dict, IO, Iterable, Optional, Type, Union


DbConnection = Union[sqlite3.Connection]


class ModelError(Exception):
    """Class to handle issues with records."""


@dataclasses.dataclass
class BaseModel(object):
    table_name: ClassVar[str] = None
    db: dataclasses.InitVar[DbConnection] = None
    id: int = None
    created_at: datetime.datetime = dataclasses.field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = dataclasses.field(default_factory=datetime.datetime.now)
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    is_deleted: Optional[bool] = False

    def __post_init__(self, db: Optional[DbConnection] = None):
        if db:
            self.db = db

    def validate(self):
        """Raises an error if record is not in good shape."""
        raise NotImplementedError('{} must implement!'.format(type(self)))

    @classmethod
    def from_csv(
        cls, f: IO, **kwargs: Optional[Dict[str, Any]]
    ) -> Iterable[Type['Model']]:
        """Seeds database with values from a CSV."""
        reader = csv.DictReader(f)
        for row in reader:
            if kwargs:
                kwargs.update(**row)
                yield cls(**kwargs)
            else:
                yield cls(**row)

    @classmethod
    def all(cls, db: DbConnection) -> Iterable[Type['BaseModel']]:
        query = 'SELECT * FROM {t} WHERE is_deleted = 0 ORDER BY id;'.format(t=cls.table_name)
        x = 0
        for row in db.execute(query):
            print(x)
            x += 1
            item = cls(**row)
            print(item)
            item.db = db
            yield item

    @classmethod
    def get(cls, db: DbConnection, id: int) -> Type['BaseModel']:
        """Fetches an instance of the class on which this is called."""
        query = 'SELECT * FROM {t} WHERE is_deleted = 0 and id = ?'
        item = cls(**db.execute(
            query.format(t=cls.table_name), (id,)).fetchone())
        item.db = db
        return item

    def as_dict(self, serialize_date=False) -> Dict[str, Any]:
        """Returns self as a dict."""
        item = dataclasses.asdict(self)
        if serialize_date:
          item['created_at'] = str(item['created_at'])
          item['updated_at'] = str(item['updated_at'])

        return item

    def save(self) -> int:
        """Given a DBAPI2 compliant connection, updates or inserts a record and returns ID."""
        self.validate()
        item = dataclasses.asdict(self)
        item_id = item['id']
        del item['id']
        if item_id is None:
            # Then Create
            statement = 'INSERT INTO {t} ({f}) VALUES ({p})'.format(
                    t=self.table_name,
                    f=', '.join(item.keys()),
                    p=', '.join('?' for _ in range(len(item))))
        else:
            self.updated_at = datetime.datetime.now()
            # TODO(john): Also set `self.updated_by` once we create users.
            # TODO(john): Find a better way to handle keys and values to avoid interpolation.
            statement = 'UPDATE {t} SET {kv} WHERE id = {i}'.format(
                    t=self.table_name,
                    kv=', '.join('{} = ?'.format(k) for k in item.keys()),
                    i=int(item_id))

        print(statement)
        with self.db:
            cursor = self.db.cursor()
            try:
                cursor.execute(statement, tuple(item.values()))
                if item_id is None:
                    self.id = cursor.lastrowid
            except sqlite3.IntegrityError as e:
                raise ModelError(str(e))
    
        return self.id

    def soft_delete(self) -> None:
        """Sets the is_deleted flag on a resource record."""
        statement = 'UPDATE {t} SET is_deleted = 1 WHERE id = ?'.format(t=self.table_name)
        with self.db:
            cursor = self.db.cursor()
            try:
                cursor.execute(statement, (self.id,))
            except sqlite3.IntegrityError as e:
                raise ModelError(str(e))