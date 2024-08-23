from copy import deepcopy
from datetime import datetime

from aiogoogle import Aiogoogle
from sqlalchemy import func

from app.constants import FORMAT, SPREADSHEET_BODY, TABLE_VALUES_DRAFT
from app.core.config import settings
from app.models import CharityProject


async def spreadsheets_create(
    wrapper_services: Aiogoogle
) -> str:
    """Создание документа."""

    now_date_time = datetime.now().strftime(FORMAT)

    service = await wrapper_services.discover('sheets', 'v4')

    spreadsheets_body = deepcopy(SPREADSHEET_BODY)
    spreadsheets_body['properties']['title'] += now_date_time

    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheets_body)
    )

    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    """Права доступа."""

    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}

    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        charity_projects: tuple[CharityProject],
        wrapper_services: Aiogoogle
) -> None:
    """Обновление данных."""

    now_date_time = datetime.now().strftime(FORMAT)
    difference_in_days = (
        func.julianday(CharityProject.close_date) -
        func.julianday(CharityProject.create_date)
    )
    service = await wrapper_services.discover('sheets', 'v4')

    table_values = [row for row in TABLE_VALUES_DRAFT]
    table_values[0] = table_values[0] + (now_date_time,)

    for project in charity_projects:
        table_values.append((
            str(project['name']),
            str(difference_in_days),
            str(project['description'])
        ))

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
