import re

from aiogram.types import User

from db_api.db_services import is_record_activated, get_record_by_user, get_all_codes


async def code_checker(code: str) -> bool:
    """Проверяет есть ли код в БД и не активирован ли он ранее"""
    pattern = re.compile(r"^((\d|\w){5,6})$")  # шаблон для отсеивания кодов которые не подходят
    if re.match(pattern, code):
        codes = await get_all_codes()
        print(codes)
        if code in codes:
            is_activated = await is_record_activated(code)
            if not is_activated:
                return True
    return False


async def record_view_for_user(user: User) -> str:
    """Представляет данные из БД в виде текста"""
    record = await get_record_by_user(user=user)
    if record:
        return f'<b>ФИО</b>: {record.name}\n' \
               f'<b>Тел.</b>: {record.phone}\n' \
               f'<b>Адрес</b>: {record.address}'
    else:
        return 'Пусто'
