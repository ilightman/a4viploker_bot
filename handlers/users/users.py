import re
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from db_api.db_services import add_user_with_code, add_name_to_record_by_telegram_id, \
    add_phone_to_record_by_telegram_id, add_address_to_record_by_telegram_id, \
    is_user_already_in_base, increase_user_attempts_number, add_user_to_second_db
from filters import UserNotBanned
from misc.admin_functions import export_records_to_admin, export_to_backup
from misc.anti_spam import is_user_banned, rate_limit
from misc.messages import START_MESSAGE, SUPPORT_MSG, ENTER_CODE_MSG, ENTER_CODE_ERROR_MSG, ENTER_NAME_ERROR_MSG, \
    ENTER_PHONE_MSG, ENTER_ADDRESS_MSG, ENTER_PHONE_ERROR, FINAL_SUCCESS, \
    ENTER_ADDRESS_ERROR_MSG, ENTER_NAME_MSG, ENTER_ADDRESS_MSG_OST, ENTER_PHONE_MSG_OST, BANNED_MSG, \
    START_MESSAGE_FOR_USERS_IN_BASE, CONGRATS_PHOTO_ID, ENTER_CODE_SUCCESS
from misc.user_functions import code_checker, record_view_for_user
from .keyboards import start_message_inl_kb, start_cb_data, change_record_cb_data, record_change_inl_kb


class UserStates(StatesGroup):
    enter_code = State()
    enter_name = State()
    re_enter_name = State()
    enter_phone = State()
    re_enter_phone = State()
    enter_address = State()
    confirm = State()


@rate_limit(3, 'start')
# @is_banned(key=True)
async def start_command(message: types.Message, state: FSMContext):
    """Акция кончилась, базовый ответ"""
    await state.finish()
    await add_user_to_second_db(message.from_user)
    msg = "К сожалению, акция подошла к концу. Впереди вас ждут и другие интересные акции! Оставайтесь на связи!"
    await message.answer(text=msg)


# @rate_limit(3, 'start')
# # @is_banned(key=True)
# async def start_command(message: types.Message, state: FSMContext):
#     """Обрабатывает стартовую команду, присылает текст приветствия и две инлайн кнопки"""
#     await state.finish()
#     await add_user_to_second_db(message.from_user)
#     # user_banned = await is_user_banned(message.from_user)
#     # if not user_banned:
#     user_in_base = await is_user_already_in_base(message.from_user)
#
#     inl_kb = await start_message_inl_kb(user_in_base)
#     msg = START_MESSAGE_FOR_USERS_IN_BASE if user_in_base else START_MESSAGE
#     await message.answer(text=msg, reply_markup=inl_kb)


@rate_limit(2)
async def start_choice(cb: types.CallbackQuery, callback_data: dict, state: FSMContext):
    """Обрабатывает нажатия одной из двух кнопок стартового сообщения"""
    await cb.answer()
    choice = callback_data.get('choice')
    if choice == 'has_code':
        # await cb.message.answer_photo(WHERE_CODE_PHOTO_ID, caption=ENTER_CODE_MSG)
        await cb.message.answer(ENTER_CODE_MSG)
        await cb.message.delete_reply_markup()
        await UserStates.enter_code.set()
    elif choice == 'support':
        await cb.message.answer(SUPPORT_MSG)
        await cb.message.delete_reply_markup()
        await state.finish()


@rate_limit(2)
async def enter_code_handler(message: types.Message, state: FSMContext):
    """Обрабатывает сообщение с введенным кодом"""
    code = message.text
    await increase_user_attempts_number(message.from_user)
    user_banned = await is_user_banned(message.from_user)
    if not user_banned and await code_checker(code):
        await add_user_with_code(message.from_user, code)
        await message.answer_photo(CONGRATS_PHOTO_ID, caption=ENTER_CODE_SUCCESS)
        await message.answer(ENTER_NAME_MSG)
        await UserStates.enter_name.set()
    elif user_banned:
        await message.answer(BANNED_MSG)
        await state.finish()
    else:
        await message.answer(ENTER_CODE_ERROR_MSG)


async def enter_name_handler(message: types.Message, state: FSMContext):
    """Обрабатывает сообщение с именем пользователя"""
    name = message.text
    if len(name.split()) < 2:
        await message.answer(ENTER_NAME_ERROR_MSG)
    else:
        await add_name_to_record_by_telegram_id(user=message.from_user, name=name)
        now_state = await state.get_state()
        if now_state == UserStates.re_enter_name.state:
            msg = await record_view_for_user(user=message.from_user)
            inl_kb = await record_change_inl_kb()
            await message.answer(msg, reply_markup=inl_kb)
            await UserStates.confirm.set()
        else:
            await message.answer(ENTER_PHONE_MSG + ENTER_PHONE_MSG_OST)
            await UserStates.enter_phone.set()


async def enter_phone_handler(message: types.Message, state: FSMContext):
    """Обрабатывает сообщение с номером телефона"""
    phone = message.text
    pattern = re.compile(r'^((8)|(7))(9)([0-9]{9})$')  # шаблон для совпадения только с номером формата 89ХХХХХХХХХ
    if re.match(pattern, phone):
        await add_phone_to_record_by_telegram_id(user=message.from_user, phone=phone)
        now_state = await state.get_state()
        if now_state == UserStates.re_enter_phone.state:
            msg = await record_view_for_user(user=message.from_user)
            inl_kb = await record_change_inl_kb()
            await message.answer(msg, reply_markup=inl_kb)
            await UserStates.confirm.set()
        else:
            await message.answer(ENTER_ADDRESS_MSG + ENTER_ADDRESS_MSG_OST)
            await UserStates.enter_address.set()
    else:
        await message.answer(ENTER_PHONE_ERROR)


async def enter_address_handler(message: types.Message, state: FSMContext):
    """Обрабатывает сообщение с адресом"""
    address = message.text
    if address:
        await add_address_to_record_by_telegram_id(user=message.from_user, address=address)
        msg = await record_view_for_user(user=message.from_user)
        inl_kb = await record_change_inl_kb()
        await message.answer(msg, reply_markup=inl_kb)
        await UserStates.confirm.set()
    else:
        await message.answer(ENTER_ADDRESS_ERROR_MSG)


async def change_choice(cb: types.CallbackQuery, callback_data: dict, state: FSMContext):
    """Обрабатывает нажатия одной из 4-х кнопок при изменении записи пользователя"""
    await cb.answer()
    choice = callback_data.get('choice')
    if choice == 'no_changes':
        await cb.message.delete_reply_markup()
        await cb.message.answer(FINAL_SUCCESS)
        await export_to_backup()
        await export_records_to_admin()
        await state.finish()
    elif choice == 'change_name':
        await cb.message.delete_reply_markup()
        await cb.message.answer(ENTER_NAME_MSG)
        await UserStates.re_enter_name.set()
    elif choice == 'change_phone':
        await cb.message.delete_reply_markup()
        await cb.message.answer(ENTER_PHONE_MSG_OST)
        await UserStates.re_enter_phone.set()
    elif choice == 'change_address':
        await cb.message.delete_reply_markup()
        await cb.message.answer(ENTER_ADDRESS_MSG_OST)
        await UserStates.enter_address.set()


@rate_limit(2)
async def delete_message(message: types.Message):
    """Удаляет бесполезные сообщения, которые не относятся к функционалу бота"""
    await add_user_to_second_db(message.from_user)
    await message.delete()


async def banned_user_handler(*args, **kwargs):
    return True


async def channel_leave_handler(message: types.Message):
    await message.bot.leave_chat(message.chat.id)


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, UserNotBanned(), commands=['start', 'help'], state=['*'])
    dp.register_callback_query_handler(start_choice, UserNotBanned(), start_cb_data.filter())
    dp.register_message_handler(enter_code_handler, UserNotBanned(), state=UserStates.enter_code)

    dp.register_message_handler(enter_name_handler, UserNotBanned(), state=UserStates.enter_name)
    dp.register_message_handler(enter_name_handler, UserNotBanned(), state=UserStates.re_enter_name)

    dp.register_message_handler(enter_phone_handler, state=UserStates.enter_phone)
    dp.register_message_handler(enter_phone_handler, state=UserStates.re_enter_phone)

    dp.register_message_handler(enter_address_handler, state=UserStates.enter_address)
    dp.register_callback_query_handler(change_choice, change_record_cb_data.filter(), state=UserStates.confirm)

    dp.register_channel_post_handler(channel_leave_handler, content_types=types.ContentTypes.ANY)

    dp.register_message_handler(delete_message, UserNotBanned(), state=['*'])
    dp.register_message_handler(banned_user_handler)
