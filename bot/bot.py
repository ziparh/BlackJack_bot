import logging
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import BotCommand
from aiogram_dialog import DialogManager, setup_dialogs, Dialog, StartMode
from aiogram_dialog.api.exceptions import NoContextError
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from option import TOKEN
from windows import main_dialog
from states import MainDialog
from database import DataBase

logging.basicConfig(level=logging.INFO)


async def set_commands(bot: Bot):
    commands = [BotCommand(command="/start", description="Запустить бота")]
    await bot.set_my_commands(commands)


# Обработчик для команды /start
async def cmd_start(message: types.Message, dialog_manager: DialogManager):
    try:
        if dialog_manager.current_context().state == MainDialog.game:
            await message.delete()
            await message.answer("Вы неможете перейти в меню пока находитесь в игре")
        else:
            async with DataBase() as db:
                user = await db.get_user(message.from_user.id)
                if not user:
                    await db.add_user(user_id=message.from_user.id,
                                name=message.from_user.username,
                                )
            await dialog_manager.start(MainDialog.menu, mode=StartMode.RESET_STACK)

    except NoContextError:
        async with DataBase() as db:
            user = await db.get_user(message.from_user.id)
            if not user:
                await db.add_user(user_id=message.from_user.id,
                                  name=message.from_user.username,
                                  )
        await message.delete()
        await dialog_manager.start(MainDialog.menu, mode=StartMode.RESET_STACK)


async def main():
    logging.info("Bot is starting...")
    async with DataBase() as db:
        await db.create_db()

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    setup_dialogs(dp)
    dp.include_router(main_dialog)

    # Регистрация команд
    dp.message.register(cmd_start, Command(commands="start"))

    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
