from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser

from app.constants import GOOGLE_SHEETS_URL
from app.crud.charity_project import charity_project_crud
from app.google_services.google_api import (
    set_user_permissions, spreadsheets_create, spreadsheets_update_value
)


router = APIRouter()


@router.post(
    '/',
    dependencies=[Depends(current_superuser)]
)
async def get_spreadsheet(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service)
):
    """
    Только для суперпользователей.

    Формирует отчет по закрытым благотворительным проектам.
    """

    projects = await charity_project_crud.get_projects_by_completion_rate(
        session
    )
    spreadsheet_id = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheet_id, wrapper_services)
    await spreadsheets_update_value(spreadsheet_id, projects, wrapper_services)

    return GOOGLE_SHEETS_URL + spreadsheet_id