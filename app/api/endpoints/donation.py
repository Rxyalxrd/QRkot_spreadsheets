from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.donation import donation_crud
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.schemas.donation import (
    DonationCreate, UserDonationsRead, SuperUserDonationRead
)
from app.models import User, CharityProject

router = APIRouter()


@router.get(
    '/',
    response_model=list[SuperUserDonationRead],
    response_model_exclude_none=True,
    dependencies=(Depends(current_superuser),)
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперюзеров.

    Возвращает список всех пожертвований.
    """

    return await donation_crud.read_all(session)


@router.get(
    '/my',
    response_model=list[UserDonationsRead],
    response_model_exclude_none=True,
)
async def get_my_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Вернуть список пожертвований пользователя, выполняющего запрос."""

    return await donation_crud.get_user_donations(user.id, session)


@router.post(
    '/',
    response_model=UserDonationsRead,
    response_model_exclude_none=True
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Создание пожертвования."""

    new_donation = await donation_crud.create(donation, session, user)
    open_charity_project = await donation_crud.get_invested_charity_projects(
        CharityProject, session
    )

    await donation_crud.distribution_of_resources(
        open_charity_project, new_donation, session
    )

    return new_donation
