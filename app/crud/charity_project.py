from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .base_crud import CRUD
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUD):
    """Расширенный CRUD класс для проектов."""

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        """Поиск id проекта по имени."""

        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )

        return db_project_id.scalars().first()

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> list[CharityProject]:
        """Сортировка всех закрытых проектов по количеству времени."""

        difference_in_days = (
            func.julianday(CharityProject.close_date) -
            func.julianday(CharityProject.create_date)
        )

        projects = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested.is_(True)
            ).order_by(difference_in_days)
        )

        return projects.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)
