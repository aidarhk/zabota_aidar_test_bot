from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def make_column_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
	"""
	Создаёт реплай-клавиатуру с кнопками в один столбец
	:param items: список текстов для кнопок
	:return: объект реплай-клавиатуры
	"""
	keyboard = [[KeyboardButton(text=item)] for item in items]
	return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
