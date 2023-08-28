from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from db_api.db_services import get_record_by_code, get_record_part_by_code, update_record_by_code, \
    activate_record_by_code, deactivate_record_by_code
from filters import IsAdmin
from handlers.admins.keyboards import record_change_inl_kb, admin_record_change_cb_data, activate_code_inl_kb, \
    cancel_inl_kb
from misc.admin_functions import admin_record_view, export_records_to_admin, export_to_backup
from misc.messages import ENTER_CODE_ERROR_MSG, record_dict


class AdminStates(StatesGroup):
    record_change = State()
    check_code = State()


async def code_status(message: types.Message, state: FSMContext):
    await message.answer('Введите код для проверки ->')  # , reply_markup=cancel_inl_kb)
    await AdminStates.check_code.set()


async def check_code_handler(message: types.Message, state: FSMContext):
    code = message.text
    record = await get_record_by_code(code)
    if record:
        msg = await admin_record_view(record)
        if not record.is_activated:
            await message.answer(msg, reply_markup=await activate_code_inl_kb(code))
        else:
            await message.answer(msg, reply_markup=await record_change_inl_kb(code))
        await AdminStates.record_change.set()
    else:
        await message.answer(ENTER_CODE_ERROR_MSG)


async def record_change_callback(cb: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await cb.answer()
    field, code = callback_data.get('field'), callback_data.get('code')
    if field == 'cancel':
        await cb.message.delete_reply_markup()
        await state.finish()
    elif field == 'activate_code':
        await activate_record_by_code(code=code)
        await export_to_backup()
        await export_records_to_admin()
        record = await get_record_by_code(code)
        await cb.message.answer(await admin_record_view(record), reply_markup=await record_change_inl_kb(code))
        await cb.message.delete()
    elif field == 'deactivate_code':
        await deactivate_record_by_code(code=code)
        record = await get_record_by_code(code)
        await cb.message.answer(await admin_record_view(record), reply_markup=await activate_code_inl_kb(code))
        await cb.message.delete()
    else:
        record_part = await get_record_part_by_code(code, part=field)
        await cb.message.delete_reply_markup()
        await cb.message.answer(f'Текущее значение {record_dict[field]}: {record_part}\n\nВведите новое:')
        await state.update_data(data={'code': code, 'field': field})


async def record_change_message_handler(message: types.Message, state: FSMContext):
    """Изменят запись с указанным кодом на текст в сообщении"""
    cb_data = await state.get_data('code')
    code, field = cb_data.get('code'), cb_data.get('field')
    msg = message.text
    record = await update_record_by_code(code=code, update_field=field, value=msg)
    msg = await admin_record_view(record)
    await message.answer(msg, reply_markup=await record_change_inl_kb(code))


def register_admin_code_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(record_change_callback, admin_record_change_cb_data.filter(),
                                       state=AdminStates.record_change)  # IsAdmin(),
    dp.register_message_handler(code_status, is_admin=True, commands='code_status', state='*')
    dp.register_message_handler(check_code_handler, is_admin=True, state=AdminStates.check_code)
    dp.register_message_handler(record_change_message_handler, is_admin=True, state=AdminStates.record_change)
