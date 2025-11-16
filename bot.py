import asyncio
import logging

from aiogram import F
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config_reader import config
from handlers import cmd_commands

bot = Bot(
	token=config.bot_token.get_secret_value(),
	default=DefaultBotProperties(
		parse_mode=ParseMode.HTML
	)
)
dp = Dispatcher()

async def main():
	logging.basicConfig(
		level=logging.INFO,
		format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
	)

	dp = Dispatcher()

	dp.include_routers(
		cmd_commands.router
	)

	await dp.start_polling(bot)

if __name__ == "__main__":
	asyncio.run(main())