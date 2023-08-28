from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

admin_record_change_cb_data = CallbackData('change', 'field', 'code')


async def record_change_inl_kb(code: str) -> InlineKeyboardMarkup:
    inl_kb = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [
            InlineKeyboardButton('Доб/изм имя', callback_data=f'change:name:{code}')
        ],
        [
            InlineKeyboardButton('Доб/изм телефон', callback_data=f'change:phone:{code}')
        ],
        [
            InlineKeyboardButton('Доб/изм адрес', callback_data=f'change:address:{code}')
        ],
        [
            InlineKeyboardButton('Доб/изм дату отправки', callback_data=f'change:date_of_shipping:{code}')
        ],
        [
            InlineKeyboardButton('Доб/изм трек-номер', callback_data=f'change:track_number:{code}')
        ],
        [
            InlineKeyboardButton('Доб/изм дату получения', callback_data=f'change:date_of_receiving:{code}')
        ],
        [
            InlineKeyboardButton('Доб/изм telegram_id', callback_data=f'change:telegram_id:{code}')
        ],
        [
            InlineKeyboardButton('Доб/изм username', callback_data=f'change:username:{code}')
        ],

        [
            InlineKeyboardButton('Деактивировать', callback_data=f'change:deactivate_code:{code}')
        ],
        [
            InlineKeyboardButton('Отмена/закрыть', callback_data=f'change:cancel:cancel')
        ],
    ])
    return inl_kb


async def activate_code_inl_kb(code: str) -> InlineKeyboardMarkup:
    inl_kb = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [
            InlineKeyboardButton('Активировать?', callback_data=f'change:activate_code:{code}')
        ],
        [
            InlineKeyboardButton('Отмена/закрыть', callback_data=f'change:cancel:cancel')
        ],
    ])
    return inl_kb


cancel_inl_kb = InlineKeyboardMarkup(row_width=1,
                                 inline_keyboard=[
                                     [InlineKeyboardButton('Отмена/закрыть', callback_data='change:cancel:cancel')]])
