from sqlalchemy import Column, String, Text

from .base_model import BaseModel
from app.constants import MAX_LENGTH_FOR_NAME


class CharityProject(BaseModel):
    """Модель проектов, доп. поля наследуются от BaseModel."""

    name = Column(String(MAX_LENGTH_FOR_NAME), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (
            f'Благотворительный проект {self.name}: {self.description}'
        )