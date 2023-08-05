from sqlalchemy import Table, Column

from atod.db import Base
from atod.db.schemas import get_abilities_schema
from atod.db_models.common_table import CommonTable


class AbilityModel(Base, CommonTable):

    _cols = [Column(**col) for col in get_abilities_schema()]

    __table__ = Table('abilities', Base.metadata, *_cols)

    def __init__(self, attrs):
        self.attrs = set()
        for key, value in attrs.items():
            setattr(self, key, value)
            self.attrs.add(key)

    def __repr__(self):
        return '<AbilityModel::{}>'.format(self.name)
