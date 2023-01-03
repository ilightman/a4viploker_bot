import os
from datetime import datetime
from zoneinfo import ZoneInfo

from aiogram import Dispatcher
from deta import Deta

from db_api.db_services import get_all_records, Record
from misc.export import export_records_to_excel


# key +
# address+
# code_number+
# date_of_receiving+
# date_of_shipping+
# is_activated+
# name+
# phone+
# telegram_id+
# track_number+
# username+

async def admin_record_view(record: Record) -> str:
    """Возвращает одну запись пользователя в виде многострочного текста"""
    msg = f'Код: {record.key}, № кода по списку: {record.code_number}\n' \
          f'Статус: {"Активирован" if record.is_activated else "Не активирован"}\n' \
          f'Дата активации: {record.activation_date}\n' \
          f'Имя: {record.name}\n' \
          f'Телефон: {record.phone}\n' \
          f'Адрес: {record.address}\n' \
          f'Дата отправки: {record.date_of_shipping}\n' \
          f'Трек-номер: {record.track_number}\n' \
          f'Дата получения: {record.date_of_receiving}\n' \
          f'TG_id: {record.telegram_id}, @{record.username}\n'
    return msg


async def export_records_to_admin():
    """Отправляет excel файл главному админу"""
    records = await get_all_records()
    file = await export_records_to_excel(records)
    now_time = datetime.now(tz=ZoneInfo('Europe/Moscow')).strftime("%d.%m.%y, %H:%M:%S")
    dispatcher = Dispatcher.get_current()
    admin_id = os.getenv('ADMIN')
    await dispatcher.bot.send_document(chat_id=admin_id, document=file,
                                       caption=f'Выгрузка {now_time}\nДобавлен код!')


async def export_to_backup():
    deta = Deta(os.getenv('PROJECT_KEY'))
    drive = deta.Drive("backup_test")
    records = await get_all_records()
    file = await export_records_to_excel(records)
    now_time = datetime.now(tz=ZoneInfo('Europe/Moscow')).strftime("%d.%m.%y, %H:%M:%S")
    drive.put(f'{now_time}.xlsx', file.read())
