from typing import Union

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from db_api.db_services import get_user_banned_mark


class IsAdmin(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin: bool):
        self.is_admin = is_admin

    async def check(self, message: Union[types.Message, types.CallbackQuery]):
        message = message.message if isinstance(message, types.CallbackQuery) else message
        admins = [800546705, 320007954]
        if message.from_user.id in admins:
            return True
        return False


class UserNotBanned(BoundFilter):
    key = 'is_banned'

    async def check(self, message: Union[types.Message, types.CallbackQuery]):
        message = message.message if isinstance(message, types.CallbackQuery) else message
        is_banned = await get_user_banned_mark(message.from_user)
        return not is_banned
