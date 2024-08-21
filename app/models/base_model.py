from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.db import Base
from app.constants import DEFAULT_INVESTED_AMOUNT


class BaseModel(Base):
    """
    Мета модель.

    Базовая абстрактная модель родителя
    для моделей проекта и пожертвования.
    """

    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(
        Integer,
        nullable=False,
        default=DEFAULT_INVESTED_AMOUNT,
    )
    fully_invested = Column(Boolean, nullable=False, default=False)
    create_date = Column(DateTime, nullable=False, default=datetime.now)
    close_date = Column(DateTime, default=None)
