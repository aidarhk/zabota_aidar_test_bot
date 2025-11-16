from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from api_laozhang.api_laozhang import get_answer_with_messages
from keyboards.kb import make_column_keyboard

router = Router()

class Enter(StatesGroup):
	text = State()
	messages = State()

@router.message(Command("start"))
@router.message(F.text == "Новый запрос")
async def cmd_start(message: types.Message, state: FSMContext):
	await state.clear() 
	await message.reply(
		'Введите запрос:',
		reply_markup=make_column_keyboard(["Новый запрос"])
	)

	await state.update_data(messages=[
		{"role": "system", "content": "Вы помощник ChatGPT."}
	])
	await state.set_state(Enter.text)

@router.message(Command("help"))
async def cmd_help(message: types.Message):
	await message.answer(
		"Напишите /start, чтобы начать разговор с ChatGPT\n"
	)

@router.message(Enter.text)
async def enter_answer(message: Message, state: FSMContext):
	waiting = await message.answer("Думаю...")

	user_message = message.text
	data = await state.get_data()
	messages = data.get("messages", [])
	
	messages.append({"role": "user", "content": user_message})
	
	response = api_laozhang.get_answer_with_messages(messages)

	if "error" in response:
		error_text = f"Ошибка API: {response['error']} (status {response.get('status_code', '')})"
		await waiting.edit_text(error_text)
		return
	
	bot_reply = response['choices'][0]['message']['content']
	
	messages.append({"role": "assistant", "content": bot_reply})
	
	await state.update_data(messages=messages)

	await waiting.edit_text(bot_reply, parse_mode=ParseMode.MARKDOWN)