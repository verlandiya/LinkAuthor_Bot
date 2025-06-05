
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from database.db_funcs import add_user, list_of_users, process_delete_user_db, complete_deletion
from database.init_db import init_db
import config

bot = Bot(token=config.API_TOKEN)
Storage = MemoryStorage()
dp = Dispatcher(bot, storage=Storage)
init_db()


def is_admin(user_id: int):
    return True


class Form(StatesGroup):
    name = State()
    user_to_delete = State()


@dp.message_handler(Command("users"))
async def users_panel(message: types.Message):
    if is_admin(message.from_user.id):
        build = types.InlineKeyboardMarkup(row_width=1)
        build.add(
            types.InlineKeyboardButton("Добавить пользователя", callback_data="add_user"),
            types.InlineKeyboardButton("Список пользователей", callback_data="users_list"),
            types.InlineKeyboardButton("Удалить пользователя", callback_data="delete_user")
        )
        await message.answer(
            "Панель управления пользователями:",
            reply_markup=build
        )


@dp.callback_query_handler(lambda cb: cb.data == "add_user")
async def add_user_cb(cb: types.CallbackQuery, state: FSMContext):
    await cb.answer()
    await cb.message.edit_text("Введите имя нового пользователя:")
    await Form.name.set()


@dp.message_handler(state=Form.name)
async def on_name_input(message: types.Message, state: FSMContext):
    user_name = message.text
    res = add_user(user_name)
    if res:
        await message.answer("Пользователь успешно добавлен")
    else:
        await message.answer("При добавлении пользователя произошла ошибка")
    await state.finish()


@dp.callback_query_handler(lambda cb: cb.data == "users_list")
async def users_list_cb(cb: types.CallbackQuery):
    text = list_of_users()
    await cb.message.edit_text(text, parse_mode=types.ParseMode.HTML)


@dp.callback_query_handler(lambda cb: cb.data == "delete_user")
async def delete_user_cb(cb: types.CallbackQuery, state: FSMContext):
    text = list_of_users()
    await cb.message.edit_text(text, parse_mode=types.ParseMode.HTML)
    if not(text == "Нет пользователей"):
        await cb.message.reply("Введите ID пользователя, которого вы хотите удалить")
        await Form.user_to_delete.set()


@dp.message_handler(state=Form.user_to_delete)
async def process_delete_user_id(message: types.Message, state: FSMContext):
    uid = message.text.strip()
    if uid.isdigit():
        uid = int(uid)
        user = process_delete_user_db(uid)
        if not user:
            await message.answer(f"User with ID {uid} did not found")
            await state.finish()
        else:
            confirmation = types.InlineKeyboardMarkup(row_width=2)
            confirmation.add(
                types.InlineKeyboardButton("Подтвердить", callback_data="confirm_delete"),
                types.InlineKeyboardButton("Отмена", callback_data="cancel_delete")
            )

            await message.answer(f"Вы действительно хотите удалить пользователя {user[0]}?\n ID: {uid}",
                                 reply_markup=confirmation)
            await state.update_data(user_to_delete=uid)
    else:
        await message.answer("Ошибка: UserID должен быть числом. Попробуйте снова")


@dp.callback_query_handler(lambda cb: cb.data == "confirm_delete", state=Form.user_to_delete)
async def delete_confirmation(cb: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    uid = data.get("user_to_delete")
    res = complete_deletion(uid)
    if res:
        await cb.message.edit_text("Пользователь успешно удален")
    else:
        await cb.message.edit_text("При удалении пользователя произошла ошибка")
    await state.finish()


@dp.callback_query_handler(lambda cb: cb.data == "cancel_delete", state=Form.user_to_delete)
async def cancel_delete_cb(cb: types.CallbackQuery, state: FSMContext):
    await cb.message.edit_text("Удаление пользователя отменено")
    await state.finish()


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp)
