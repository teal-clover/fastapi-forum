from abc import ABC, abstractmethod
from typing import TypeVar

from pydantic import BaseModel

from forum.base import models

Model = TypeVar("Model", bound=models.Base)
Schema = TypeVar("Schema", bound=BaseModel)


class RepositoryBase(ABC):
    @abstractmethod
    async def create(self, item: Schema) -> Model:
        pass

    @abstractmethod
    async def read_one(self, id: int) -> Model:
        pass

    @abstractmethod
    async def read_all(self, skip: int = 0, limit: int = 0) -> list[Model]:
        pass

    @abstractmethod
    async def update(self, item_id, item: Schema) -> Model:
        pass

    @abstractmethod
    async def delete() -> Model:
        pass
