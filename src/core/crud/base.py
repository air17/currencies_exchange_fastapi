from typing import Any, Dict, Generic, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, SchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        Args:
            model: The SQLAlchemy model class.
        """
        self.model = model

    async def get(self, db: AsyncSession, idx: Any) -> Optional[ModelType]:
        """
        Returns an object with the given id.

        Args:
            db: The database session.
            idx: The id of the object to get.

        Returns:
            The object with the given id.
        """
        return await db.get(self.model, idx)

    async def create(self, db: AsyncSession, *, obj_in: Union[SchemaType, Dict[str, Any]]) -> ModelType:
        """
        Creates an object.

        Args:
            db: The database session.
            obj_in: The object to create.

        Returns:
            The created object.
        """
        if isinstance(obj_in, dict):
            db_obj = self.model(**obj_in)
        else:
            db_obj = self.model(**obj_in.model_dump())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @staticmethod
    async def update(db: AsyncSession, *, db_obj: ModelType, obj_in: Union[SchemaType, Dict[str, Any]]) -> ModelType:
        """
        Updates an object.

        Args:
            db: The database session.
            db_obj: The object to update.
            obj_in: The object to update with.

        Returns:
            The updated object.
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @staticmethod
    async def delete(db: AsyncSession, *, db_obj: ModelType) -> ModelType:
        """
        Deletes an object.

        Args:
            db: The database session.
            db_obj: The object to delete.

        Returns:
            The deleted object.
        """
        await db.delete(db_obj)
        await db.commit()
        return db_obj
