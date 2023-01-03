from collections import namedtuple
from typing import Union

from aiogram.types import User

from db_api.db_config import db

Record = namedtuple('Record',
                    ['key', 'is_activated', 'telegram_id', 'username',
                     'name', 'phone', 'address',
                     'date_of_shipping', 'track_number', 'date_of_receiving',
                     'code_number', 'activation_date'])


async def get_record_by_code(code: str) -> Union[Record, None]:
    """Возвращает запись в БД если она есть или None"""
    record = db.get_record(code=code)
    if record:
        return Record(**record)
    return None


async def update_record_by_code(code: str, update_field: str, value: str) -> Union[Record, None]:
    """Обновляет запись в БД с указанным update_field и value"""
    db.update_record_by_code(code=code, update_field=update_field, value=value)
    record = db.get_record(code=code)
    if record:
        return Record(**record)
    return None


async def get_record_part_by_code(code: str, part: str) -> Union[str, None]:
    """Получает один из пунктов записи в БД"""
    return db.get_record_part_by_code(code=code, value=part)


async def add_user_to_second_db(user: User):
    """Добавляет пользователя во вторую БД"""
    user_in_db = db.get_user(str(user.id))
    if not user_in_db:
        record = db.add_user(str(user.id))


async def user_is_banned(user: User) -> bool:
    """Проверяет в БД забанен ли пользователь"""
    banned = db.get_user_banned_mark(str(user.id))
    return banned


async def get_record_by_user(user: User) -> Record:
    """Получает пользователя из БД через """
    record = db.get_record_by_telegram_id(str(user.id))
    return Record(**record)


async def get_all_records() -> list[Record]:
    """Получает список всех записей из БД"""
    records = db.get_all_records()
    return [Record(**record) for record in records]


async def get_all_codes() -> list[str]:
    """Получает список всех кодов из БД"""
    codes = db.get_all_codes()
    return codes


async def activate_record_by_code(code: str):
    """Активирует код в БД"""
    db.activate_record_by_code(code=code)


async def deactivate_record_by_code(code: str):
    """Деактивирует код в БД"""
    db.deactivate_record_by_code(code=code)


async def is_record_activated(code: str) -> bool:
    """Проверяет в БД активировался ли ранее код"""
    record = db.get_record(code)
    return record.get('is_activated')


async def is_user_already_in_base(user: User) -> bool:
    """Проверяет есть ли уже пользователь в БД"""
    record = db.get_record_by_telegram_id(str(user.id))
    if record:
        return True
    return False


async def add_user_with_code(user: Union[User, None], code: str):
    """Добавляет пользователя с указанным кодом в БД, а также отмечает что код активирован"""
    if user:
        db.add_user_with_code(username=user.username, telegram_id=str(user.id), code=code)
    else:
        db.add_user_with_code(username=None, telegram_id=None, code=code)


async def add_name_to_record_by_telegram_id(user: User, name: str) -> dict:
    """Обновляет имя и фамилию пользователя с указанным telegram_id в БД"""
    record = db.add_name_to_record_by_telegram_id(telegram_id=str(user.id), name=name.title())
    return record


async def add_phone_to_record_by_telegram_id(user: User, phone: str) -> dict:
    """Обновляет номер телефона пользователя с указанным telegram_id в БД"""
    record = db.add_phone_to_record_by_telegram_id(telegram_id=str(user.id), phone=phone)
    return record


async def add_address_to_record_by_telegram_id(user: User, address: str) -> dict:
    """Обновляет адрес пользователя с указанным telegram_id в БД"""
    record = db.add_address_to_record_by_telegram_id(telegram_id=str(user.id), address=address)
    return record


async def add_name_to_record_by_code(code: str, name: str) -> dict:
    """Обновляет имя и фамилию пользователя с указанным telegram_id в БД"""
    record = db.add_name_to_record_by_code(code=code, name=name.title())
    return record


async def add_phone_to_record_by_code(code: str, phone: str) -> dict:
    """Обновляет номер телефона пользователя с указанным кодом в БД"""
    record = db.add_phone_to_record_by_code(code=code, phone=phone)
    return record


async def add_address_to_record_by_code(code: str, address: str) -> dict:
    """Обновляет адрес пользователя с указанным кодом в БД"""
    record = db.add_address_to_record_by_code(code=code, address=address)
    return record


async def get_attempts_number(user: User) -> int:
    """Получает счетчик попыток ввода кода из БД"""
    attempts = db.get_attempts_number(str(user.id))
    return attempts


async def get_user_banned_mark(user: User):
    """Проверяет не в бане ли пользователь"""
    return db.get_user_banned_mark(str(user.id))


async def set_user_ban(user: User):
    """Ставит отметку о том что пользователь забанен в БД"""
    db.set_user_ban(str(user.id))


async def increase_user_attempts_number(user: User) -> int:
    """Добавляет к счетчику попыток единицу, возвращает текущее значение"""
    attempts = db.increase_user_attempts_number(str(user.id))
    return attempts
