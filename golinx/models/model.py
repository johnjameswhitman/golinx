import csv
import dataclasses
import datetime
import sqlite3
from typing import IO, Iterable


@dataclasses.dataclass
class Model(object):
    id: int = None
    created_at: datetime.datetime = dataclasses.field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = dataclasses.field(default_factory=datetime.datetime.now)
    db: dataclasses.InitVar[sqlite3.Connection] = None

    def validate(self):
        """Raises an error if record is not in good shape."""
        raise NotImplementedError('{} must implement!'.format(type(self)))

    def save(self) -> bool:
        """Given a DBAPI2 compliant connection, saves if."""
        self.validate()
        item = dataclasses.asdict(self)
        item_id = item['id']
        del item['id']
        if item_id is None:
            # Then Create
            statement = 'INSERT INTO {t} ({f}) VALUES ({p})'.format(
                    t=self.table_name,
                    f=', '.join(item.keys()),
                    p=', '.join('?' for _ in item.keys()))
        else:
            statement = 'UPDATE {t} SET {kv} WHERE id = {i}'.format(
                    t=self.table_name,
                    kv=', '.join('{} = ?'.format(k) for k in item.keys()),
                    i=item_id)

        self.db.execute(statement, tuple(item.values()))
        self.db.commit()


    @classmethod
    def from_csv(cls, f: IO) -> Iterable['Model']:
        reader = csv.DictReader(f)
        for row in reader:
            yield cls(**row)


