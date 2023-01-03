from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from misc.messages import FIRST_BUTTON_TEXT, SECOND_BUTTON_TEXT, CHANGE_ADDRESS_TEXT, NO_CHANGES_TEXT, CHANGE_NAME_TEXT, \
    CHANGE_PHONE_TEXT

start_cb_data = CallbackData('start', 'choice')
change_record_cb_data = CallbackData('change_kb', 'choice')


async def start_message_inl_kb(already_claimed=False) -> InlineKeyboardMarkup:
    inl_kb = InlineKeyboardMarkup(row_width=1)
    if not already_claimed:
        inl_kb.add(InlineKeyboardButton(text=FIRST_BUTTON_TEXT, callback_data=start_cb_data.new('has_code')))
    inl_kb.add(InlineKeyboardButton(text=SECOND_BUTTON_TEXT, callback_data=start_cb_data.new('support')))
    return inl_kb


async def record_change_inl_kb() -> InlineKeyboardMarkup:
    inl_kb = InlineKeyboardMarkup(row_width=1)
    inl_kb.add(InlineKeyboardButton(text=NO_CHANGES_TEXT,
                                    callback_data=change_record_cb_data.new('no_changes')))
    inl_kb.add(InlineKeyboardButton(text=CHANGE_NAME_TEXT,
                                    callback_data=change_record_cb_data.new('change_name')))
    inl_kb.add(InlineKeyboardButton(text=CHANGE_PHONE_TEXT,
                                    callback_data=change_record_cb_data.new('change_phone')))
    inl_kb.add(InlineKeyboardButton(text=CHANGE_ADDRESS_TEXT,
                                    callback_data=change_record_cb_data.new('change_address')))
    return inl_kb
