from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject


async def project_name_exist(
        project_name: str,
        session: AsyncSession
) -> None:
    """Проверка уникальности названия проекта."""

    project_id: int | None = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )

    if project_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Проект с таким именем уже существует!"
        )


async def project_exist(
        project_id: int,
        session: AsyncSession
) -> CharityProject:
    """Проверка существования проекта."""

    charity_project: CharityProject = await charity_project_crud.read(
        project_id, session
    )

    if not charity_project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Проект не найден."
        )

    return charity_project


async def project_with_donations(
        charity_project: CharityProject
) -> CharityProject:
    """Проверка на удаление проекта, который начал сбор средств."""

    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="В проект были внесены средства, не подлежит удалению!"
        )

    return charity_project


async def full_amount_lower_then_invested(
        project_id: int,
        amount: int,
        session: AsyncSession
) -> CharityProject:
    """Проверка на изменение суммы сбора средтсв."""

    charity_project: CharityProject = await charity_project_crud.read(
        project_id, session
    )

    if charity_project.invested_amount > amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                "Нельзя установить значение full_amount "
                "меньше уже вложенной суммы."
            )
        )

    return charity_project


async def ensure_project_open(
        project_id: int,
        session: AsyncSession
) -> CharityProject:
    """Проверка на изменения закрытого проекта."""

    charity_project: CharityProject = await charity_project_crud.read(
        project_id, session
    )

    if charity_project.close_date:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Закрытый проект нельзя редактировать!"
        )

    return charity_project
