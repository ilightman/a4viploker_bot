from typing import Union

from aiogram import types
from aiogram.dispatcher.handler import current_handler, CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from db_api.db_services import user_is_banned


class BanMiddleware(BaseMiddleware):

    def __init__(self):
        super(BanMiddleware, self).__init__()

    async def cancel_handler(self, message: Union[types.Message, types.CallbackQuery]):
        handler = current_handler.get()
        if not handler:
            return

        print(self)

        message = message.message if isinstance(message, types.CallbackQuery) else message
        if await user_is_banned(message.from_user):
            raise CancelHandler()

    async def on_process_message(self, message: types.Message, data: dict):
        await self.cancel_handler(message)

    async def on_process_callback_query(self, call, data):
        await self.cancel_handler(call)
