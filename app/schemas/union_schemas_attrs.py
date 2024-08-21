from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class UnionAttrsInSchemas(BaseModel):
    """Схема совподающих полей."""

    invested_amount: int = Field(..., title='Сколько вложено')
    fully_invested: bool = Field(False, title='Вложена полная сумма')
    close_date: Optional[datetime] = Field(None, title='Дата вложения')

    class Config:

        title = 'Совпадающие поля для схем charity project и donation'