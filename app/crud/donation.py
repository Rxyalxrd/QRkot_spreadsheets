from asyncio import get_event_loop
from typing import Optional, Union
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base_crud import CRUD
from app.models import CharityProject, Donation


class CRUDDonation(CRUD):
    """Расширенный CRUD класс для пожертвований."""

    async def get_user_donations(
        self,
        user_id: int,
        session: AsyncSession
    ):
        """Поиск пожертвований по id пользователя."""

        donations = await session.execute(
            select(Donation).where(Donation.user_id == user_id)
        )

        return donations.scalars().all()

    async def distribution_of_resources(
        self,
        project_or_donation: list[Union[CharityProject, Donation]],
        funds: Union[CharityProject, Donation],
        session: AsyncSession
    ) -> Union[CharityProject, Donation]:
        """Распределение средств."""

        if not project_or_donation:
            await session.commit()
            await session.refresh(funds)
            return funds

        for current_project_or_donation in project_or_donation:
            funds_diff = funds.full_amount - funds.invested_amount
            item_diff = (
                current_project_or_donation.full_amount -
                current_project_or_donation.invested_amount
            )

            if funds_diff >= item_diff:
                funds.invested_amount += item_diff
                current_project_or_donation.invested_amount = (
                    current_project_or_donation.full_amount
                )

                await get_event_loop().run_in_executor(
                    None, self.close_invested, current_project_or_donation
                )

                if funds_diff == item_diff:
                    await get_event_loop().run_in_executor(
                        None, self.close_invested, funds
                    )

                    break
            else:
                current_project_or_donation.invested_amount += funds_diff
                funds.invested_amount = funds.full_amount

                await get_event_loop().run_in_executor(
                    None, self.close_invested, funds
                )

                break

            session.add(current_project_or_donation)
        session.add(funds)
        await session.commit()
        await session.refresh(funds)

        return funds

    def close_invested(
            self,
            project_or_donation: Union[CharityProject, Donation]
    ) -> Union[CharityProject, Donation]:
        """Завершение сбора средств или транзакции."""

        project_or_donation.fully_invested = True
        project_or_donation.close_date = datetime.now()
        return project_or_donation

    async def get_invested_charity_projects(
            self,
            charity_project: Union[type[CharityProject], type[Donation]],
            session: AsyncSession
    ) -> Optional[list[Union[CharityProject, Donation]]]:
        """
        Получение всех проектов.

        Получение всех проектов, в которые нужно инвестировать
        или средств, которые не были проинвестированны.
        """

        invested_projects = await session.execute(
            select(charity_project).where(
                charity_project.fully_invested.is_(False)
            ).order_by(charity_project.create_date)
        )
        return invested_projects.scalars().all()


donation_crud = CRUDDonation(Donation)
