# coding=utf-8
from abc import abstractmethod, ABC
from typing import Sequence

from .custom_types import FieldDisplayName, SQL, SqlDialect
from .sql_field import SqlField


class IQueryable(ABC):
    """"""

    @property
    @abstractmethod
    def alias(self) -> FieldDisplayName:
        """"""

    @property
    @abstractmethod
    def dialect(self) -> SqlDialect:
        """"""

    @abstractmethod
    def field(self, field_alias: FieldDisplayName) -> SqlField:
        """"""

    @property
    @abstractmethod
    def fields(self) -> Sequence[SqlField]:
        """"""

    @property
    @abstractmethod
    def root_alias(self) -> str:
        """"""

    @property
    @abstractmethod
    def schema(self) -> str:
        """"""

    @property
    @abstractmethod
    def sql(self) -> SQL:
        """"""

    @property
    @abstractmethod
    def suffix(self) -> int:
        """"""
