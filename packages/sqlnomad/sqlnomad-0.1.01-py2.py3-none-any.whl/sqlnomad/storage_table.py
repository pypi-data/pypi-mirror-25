# coding=utf-8
from typing import Sequence

from sqlnomad.subquery import Subquery
from .custom_types import (
    TableStorageName,
    TableDisplayName,
    SqlDialect,
    FieldDisplayName,
    SQL
)
from .sql_field import SqlField
from .iqueryable import IQueryable
from .storage_field import StorageField
from .utils import rebracket


class StorageTable(IQueryable):
    """Value-object representing a table in a relational database"""

    def __init__(self,
        storage_name: TableStorageName,
        display_name: TableDisplayName,
        fields: Sequence[StorageField],
        dialect: SqlDialect,
        schema: str=None
    ):
        self._storage_name = storage_name
        self._display_name = display_name
        self._fields = fields
        self._dialect = dialect
        self._schema = schema

    @property
    def alias(self) -> FieldDisplayName:
        return rebracket(self._display_name)

    @property
    def dialect(self) -> SqlDialect:
        return self._dialect

    @property
    def fields(self) -> Sequence[SqlField]:
        return [
            SqlField(
                alias=rebracket(fld.display_name),
                definition=f"{rebracket(self.alias)}.{rebracket(fld.display_name)}",
            )
            for fld in self._fields
        ]

    @property
    def root_alias(self) -> str:
        return rebracket(self._display_name)

    @property
    def schema(self) -> str:
        return rebracket(self._schema)

    @property
    def sql(self) -> SQL:
        if self._schema:
            full_table_name = f"{rebracket(self._schema)}.{rebracket(self._storage_name)}"
        else:
            full_table_name = rebracket(self._storage_name)

        qualify_field = lambda fld: f"{rebracket(fld.storage_name)} AS {rebracket(fld.display_name)}"
        select_fields = ", ".join(qualify_field(fld) for fld in self._fields)

        return f"SELECT {select_fields} FROM {full_table_name}"

    @property
    def suffix(self) -> int:
        return 1

    def field(self, field_alias: FieldDisplayName) -> SqlField:
        try:
            return next(
                fld for fld in self.fields
                if fld.alias == rebracket(field_alias)
            )
        except StopIteration:
            raise ValueError(f"No field named {field_alias!r} was found on {self._display_name!r}.")

    def __repr__(self):
        return f"""
        StorageTable(
            storage_name={self._storage_name!r},
            display_name={self._display_name!r},
            fields={self._fields!r},
            dialect={self._dialect!r},
            schema={self._schema!r}
        )
        """

    def __str__(self):
        return f"""
        StorageTable
            storage_name: {self._storage_name!s}
            display_name: {self._display_name!s}
            fields: {self._fields!s}
            dialect: {self._dialect!s}
            schema: {self._schema!s}
        """

