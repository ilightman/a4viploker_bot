from typing import Union

from aiogram import types
from aiogram.dispatcher.handler import current_handler, CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from db_api.db_services import user_is_banned


class BanMiddleware(BaseMiddleware):

    def __init__(self, key: bool = False):
        self.key = key
        super(BanMiddleware, self).__init__()

    async def cancel_handler(self, message: Union[types.Message, types.CallbackQuery]):
        handler = current_handler.get()
        if not handler:
            return

        key = getattr(handler, 'throttling_key', f'key_{self.key}')

        message = message.message if isinstance(message, types.CallbackQuery) else message
        user_banned = await user_is_banned(message.from_user)
        if user_banned:
            await message.delete()
            raise CancelHandler()

    async def on_process_message(self, message: types.Message, data: dict):
        await self.cancel_handler(message)

    async def on_process_callback_query(self, call, data):
        await self.cancel_handler(call)
