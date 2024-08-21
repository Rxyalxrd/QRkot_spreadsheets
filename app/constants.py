from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"
SPREADSHEET_ROWCOUNT_DRAFT = 100
SPREADSHEET_COLUMN_COUNT_DRAFT = 11
MAX_LENGTH_FOR_NAME = 100
MIN_LENGTH_FOR_NAME = 1
DEFAULT_INVESTED_AMOUNT = 0
TOKEN_LIFETIME = 3600
PASSWORD_MIN_LENGTH = 3
GOOGLE_SHEETS_URL = 'https://docs.google.com/spreadsheets/d/'


SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
]

INFO = {
    'type': settings.type,
    'project_id': settings.project_id,
    'private_key_id': settings.private_key_id,
    'private_key': settings.private_key,
    'client_email': settings.client_email,
    'client_id': settings.client_id,
    'auth_uri': settings.auth_uri,
    'token_uri': settings.token_uri,
    'auth_provider_x509_cert_url': settings.auth_provider_x509_cert_url,
    'client_x509_cert_url': settings.client_x509_cert_url
}

SPREADSHEET_BODY = dict(
    properties=dict(
        title='Отчет на ',
        locale='ru_RU',
    ),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=0,
        title='Лист1',
        gridProperties=dict(
            rowCount=SPREADSHEET_ROWCOUNT_DRAFT,
            columnCount=SPREADSHEET_COLUMN_COUNT_DRAFT
        )
    ))]
)

TABLE_VALUES_DRAFT = [
    ['Отчет от', ],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]