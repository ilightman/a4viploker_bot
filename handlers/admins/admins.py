from datetime import datetime
from zoneinfo import ZoneInfo

from aiogram import types, Dispatcher

from db_api.db_services import get_all_records
from filters import IsAdmin
from misc.admin_functions import export_to_backup
from misc.export import export_records_to_excel


# @dp.message_handler(user_id=800546705)
# async def echo(message: types.Message):
#     await message.answer_photo('AgACAgIAAxkBAAIEp2OoJtayIsvUSfxSjOGAhu-6pwl2AAJHxzEbmt9ISeR8SCSKZzBmAQADAgADeAADLAQ')
#


async def help_command(message: types.Message):
    msg = '<b>/code_status</b> - вывести информацию по коду\n' \
          '<b>/export</b> - экспорт всех записей в excel\n' \
          '<b>/cancel</b> - сброс'
    await message.answer(msg)


async def export_command(message: types.Message):
    records = await get_all_records()
    file = await export_records_to_excel(records)
    await export_to_backup()
    now_time = datetime.now(tz=ZoneInfo('Europe/Moscow')).strftime("%d.%m.%y, %H:%M:%S")
    await message.answer_document(file, caption=f'Выгрузка {now_time}')


async def photo_handler(message: types.Message):
    file_id = message.photo[-1].file_id
    await message.answer(file_id)


def register_admin_common_handlers(dp: Dispatcher):
    dp.register_message_handler(help_command, is_admin=True, commands=['help'])
    dp.register_message_handler(export_command, is_admin=True, commands=['export'])
    dp.register_message_handler(photo_handler, is_admin=True, content_types=types.ContentTypes.PHOTO)
