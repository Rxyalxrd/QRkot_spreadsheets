from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, Extra

from .union_schemas_attrs import UnionAttrsInSchemas


class BaseDonationsSchemas(BaseModel):
    """Базовая схема пожертвований."""

    full_amount: PositiveInt = Field(..., title='Сумма пожертвования')
    comment: Optional[str] = Field(None, title='Комментарий к пожертвоанию')

    class Config:
        extra = Extra.forbid
        title = 'Базовая схема для пожертвований'


class DonationCreate(BaseDonationsSchemas):
    """Схема пожертвования для создания."""

    class Config:
        title = 'Схема пожертвования для создания'
        extra = Extra.forbid
        schema_extra = {
            'example': {
                'comment': 'От всей души',
                'full_amount': 450
            }
        }


class UserDonationsRead(BaseDonationsSchemas):
    """Схема для получения списка пожертвований пользователя."""

    id: int = Field(..., title='id пожертвования')
    create_date: datetime = Field(..., title='Дата внесения пожертвования')

    class Config:
        title = 'Схема пожертвования для получения'
        orm_mode = True
        schema_extra = {
            'example': {
                'full_amount': 450,
                'comment': 'От всей души',
                'id': 2,
                'create_date': '2023-07-21T23:54:05.177Z'
            }
        }


class SuperUserDonationRead(UserDonationsRead, UnionAttrsInSchemas):
    """
    Только для суперюзеров.

    Схема для возврата списока всех пожертвований.
    """

    user_id: int = Field(None, title='ID пользователя')

    class Config:
        title = 'Схема пожертвования для получения (advanced)'
        orm_mode = True
        schema_extra = {
            'example': {
                'comment': 'От всей души',
                'full_amount': 450,
                'id': 2,
                'create_date': '2023-07-21T23:54:05.177Z',
                'user_id': 1,
                'invested_amount': 200,
                'fully_invested': 0
            }
        }
