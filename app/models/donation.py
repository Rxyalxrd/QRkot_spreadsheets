from sqlalchemy import Column, ForeignKey, Integer, Text

from .base_model import BaseModel


class Donation(BaseModel):
    """Модель пожертвований, доп. поля наследуются от BaseModel."""

    user_id = Column(
        Integer,
        ForeignKey('user.id', name='fk_donation_user_id_user'),
    )
    comment = Column(Text)

    def __repr__(self):
        return (
            f'Сделано пожертвование {self.full_amount} '
            f'и оставлен комментарий {self.comment}'
        )