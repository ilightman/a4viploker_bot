import asyncio
from typing import Union

from aiogram import Dispatcher, types
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import current_handler, CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled


class ThrottlingMiddleware(BaseMiddleware):
    """
    Simple middleware
    """

    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def throttle(self, target_message: Union[types.Message, types.CallbackQuery]):
        handler = current_handler.get()
        if not handler:
            return

        dispatcher = Dispatcher.get_current()
        limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
        key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")

        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            # Execute action
            await self.message_throttled(target_message, t, dispatcher, key)

            # Cancel current handler
            raise CancelHandler()

    async def on_process_message(self, message: types.Message, data: dict):
        await self.throttle(message)

    async def on_process_callback_query(self, call, data):
        await self.throttle(call)

    @staticmethod
    async def message_throttled(message: Union[types.Message, types.CallbackQuery],
                                throttled: Throttled, dispatcher: Dispatcher, key: str):
        message = message.message if isinstance(message, types.CallbackQuery) else message
        delta = throttled.rate - throttled.delta

        # Prevent flooding
        if throttled.exceeded_count == 1:
            await message.answer(f'Не торопись! подожди {delta}')
            # await message.delete()
        elif throttled.exceeded_count >1:
            await message.delete()
        # elif throttled.exceeded_count == 5:
        #     await message.answer(f'Превышено количество возможных сообщений, ожидайте разблокировки!')
        #     return
        # Sleep.
        await asyncio.sleep(delta)

        # Check lock status
        thr = await dispatcher.check_key(key)

        # If current message is not last with current key - do not send message
        if thr.exceeded_count == throttled.exceeded_count:
            await message.answer('Не отправляй сообщения так часто! Сейчас можно')
