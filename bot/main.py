import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommand
from aiogram_dialog import Dialog, Window, DialogManager, StartMode, setup_dialogs
from aiogram_dialog.widgets.kbd import Button, Start
from aiogram_dialog.widgets.text import Const

from option import TOKEN

async def set_commands(bot: Bot):
    commands = [BotCommand(command="/start", description="Запустить бота")]
    await bot.set_my_commands(commands)


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    setup_dialogs(dp)
    dp.include_router()

    await set_commands(bot)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
