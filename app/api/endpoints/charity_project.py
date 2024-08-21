from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (
    CharityProjectsRead, CharityProjectsCreate, CharityProjectsUpdate
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.api.validators import (
    project_exist, project_name_exist, project_with_donations,
    full_amount_lower_then_invested, ensure_project_open
)
from app.models import Donation

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectsRead],
    response_model_exclude_none=True,
)
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session)
):
    """Возвращает список всех проектов."""

    return await charity_project_crud.read_all(session)


@router.post(
    '/',
    response_model=CharityProjectsRead,
    response_model_exclude_none=True,
    dependencies=(Depends(current_superuser),),
)
async def create_new_charity_projects(
    charity_project: CharityProjectsCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперюзеров.

    Создаёт благотворительный проект.
    """

    await project_name_exist(charity_project.name, session)

    new_charity_project = await charity_project_crud.create(
        charity_project, session
    )
    new_donate = await donation_crud.get_invested_charity_projects(
        Donation, session
    )

    await donation_crud.distribution_of_resources(
        new_donate, new_charity_project, session
    )

    return new_charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectsRead,
    response_model_exclude_none=True,
    dependencies=(Depends(current_superuser),),
)
async def update_charity_project(
    project_id: int,
    new_data: CharityProjectsUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперюзеров.

    Обновление данных в проекте.
    Закрытый проект нельзя.
    Нельзя установить требуемую сумму меньше уже вложенной.
    """

    charity_project = await project_exist(project_id, session)
    await ensure_project_open(project_id, session)

    if new_data.name:
        await project_name_exist(new_data.name, session)

    if new_data.full_amount:
        await full_amount_lower_then_invested(
            project_id, new_data.full_amount, session
        )

    if charity_project.invested_amount >= charity_project.full_amount:
        charity_project.fully_invested = True
        await session.commit()
        await session.refresh(charity_project)

    charity_project = await charity_project_crud.update(
        charity_project, new_data, session
    )

    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectsRead,
    dependencies=(Depends(current_superuser),),
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперюзеров.

    Удаляет проект.
    Нельзя удалить проект, в который уже были инвестированы средства,
    его можно только закрыть.
    """

    charity_project = await project_exist(project_id, session)
    await project_with_donations(charity_project)

    charity_project = await charity_project_crud.delete(
        charity_project, session
    )

    return charity_project