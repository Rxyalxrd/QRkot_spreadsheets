from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, validator, PositiveInt, Extra
from app.constants import MAX_LENGTH_FOR_NAME, MIN_LENGTH_FOR_NAME

from .union_schemas_attrs import UnionAttrsInSchemas


class BaseCharityProjectsSchemas(BaseModel):
    """Базовая схема для проектов."""

    name: str = Field(
        ...,
        title='Название проекта',
        min_length=MIN_LENGTH_FOR_NAME,
        max_length=MAX_LENGTH_FOR_NAME
    )
    description: str = Field(..., title='Описание проекта')
    full_amount: PositiveInt = Field(..., title='Сумма пожертвования')

    class Config:
        extra = Extra.forbid
        title = 'Базовая схема для проектов'


class CharityProjectsCreate(BaseCharityProjectsSchemas):
    """Схема для создания проекта."""

    class Config:
        title = 'Схема проектов для POST запросов'
        extra = Extra.forbid
        schema_extra = {
            'example': {
                'name': 'Котику на курсы',
                'description': 'Курс для обучения на yandex practicum',
                'full_amount': 1000
            }
        }

    @validator('name')
    def name_cannot_be_null(cls, name: str):
        if not name:
            raise ValueError('Название проекта не может быть пустым!')
        return name

    @validator('description')
    def description_cannot_be_null(cls, description: str):
        if not description:
            raise ValueError('Описание проекта не может быть пустым!')
        return description

    @validator('full_amount')
    def full_amount_cannot_be_lt_zero(cls, full_amount: int):
        if full_amount < 0:
            raise ValueError('Сумма пожертвования должна быть > 0')
        return full_amount


class CharityProjectsUpdate(BaseModel):
    """Схема для обновления проекта."""

    name: Optional[str] = Field(
        None,
        title='Название проекта',
        min_length=MIN_LENGTH_FOR_NAME,
        max_length=MAX_LENGTH_FOR_NAME
    )
    description: Optional[str] = Field(None, title='Описание проекта')
    full_amount: Optional[PositiveInt] = Field(
        None, title='Сумма пожертвования'
    )

    class Config:
        title = 'Схема проектов для POST запросов'
        orm_mode = True
        extra = Extra.forbid
        schema_extra = {
            'example': {
                'name': '2 котикам на курсы',
                'description': 'Курс для обучения на yandex practicum',
                'full_amount': 100000
            }
        }

    @validator('name')
    def name_cannot_be_empty(cls, name: Optional[str]):
        if name is not None and not name.strip():
            raise ValueError('Название проекта не может быть пустым!')
        return name

    @validator('description')
    def description_cannot_be_empty(cls, description: Optional[str]):
        if description is not None and not description.strip():
            raise ValueError('Описание проекта не может быть пустым!')
        return description


class CharityProjectsRead(BaseCharityProjectsSchemas, UnionAttrsInSchemas):
    """Схема для чтения проекта."""

    id: int = Field(..., title='id пользователя')
    create_date: datetime = Field(..., title='Время создания')

    class Config:
        title = 'Схема проекта для получения'
        orm_mode = True
        schema_extra = {
            'example': {
                'name': 'Песики - наше все',
                'description': 'очень хочу им помочь',
                'full_amount': 1500,
                'id': 19,
                'invested_amount': 360,
                'fully_invested': 0,
                'create_date': '2023-07-22T02:18:40.662286'
            }
        }
