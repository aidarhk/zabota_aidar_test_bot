from datetime import datetime, date, time, timedelta
from calendar import monthrange

from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database import *

replacements_month = {
	1: "Январь",
	2: "Февраль",
	3: "Март",
	4: "Апрель",
	5: "Май",
	6: "Июнь",
	7: "Июль",
	8: "Август",
	9: "Сентябрь",
	10: "Октябрь",
	11: "Ноябрь",
	12: "Декабрь",
}

router = Router()

@router.callback_query(F.data.startswith("year"))
async def callback_year(callback):
	type_year = callback.data.split("_")[-2]
	year = callback.data.split("_")[-1]

	if type_year == "next":
		await callback.message.edit_text(
			text="Расписание",
			reply_markup=_create_calendar(int(year) + 1)
		)
	elif type_year == "back":
		await callback.message.edit_text(
			text="Расписание",
			reply_markup=_create_calendar(int(year) - 1)
		)

@router.callback_query(F.data.startswith("month"))
async def callback_month(callback):
	data = callback.data.split("_")

	if data[1] == "next":
		year = int(data[-1])
		mounth = int(data[2]) + 1
		
		if mounth == 13:
			mounth = 1
			year += 1
	elif data[1] == "back":
		year = int(data[-1])
		mounth = int(data[2]) - 1

		if mounth == 0:
			mounth = 12
			year -= 1
	
	await callback.message.edit_text(
		text="Расписание",
		reply_markup=_create_calendar(year, mounth)
	)

@router.callback_query(F.data.startswith("day"))
async def callback_day(callback):
	id_user = get_id_user_from_id_telegram(callback.message.chat.id)
	data_call = callback.data.split("_")

	list_sheldue = get_scheldue_from_user(id_user, data_call[-1], data_call[-2], data_call[-3])

	list_time = [
		["07:00", "➕"],
		["08:30", "➕"],
		["10:00", "➕"],
		["11:30", "➕"],
		["13:00", "➕"],
		["15:00", "➕"],
		["16:30", "➕"],
		["18:00", "➕"],
		["19:30", "➕"],
	]

	for i in list_time:
		for j in list_sheldue:
			if i[0] == j[5]:
				i[1] = j[6] + " ✏️"

	builder = InlineKeyboardBuilder()

	for t, s in list_time:
		builder.button(text=t, callback_data=f"pass")
		builder.button(text=s, callback_data=f"sheldue_{t}_{data_call[-1]}_{data_call[-2]}_{data_call[-3]}")

	builder.adjust(2)

	await callback.message.edit_text(
		text=f"{data_call[-1]}_{data_call[-2]}_{data_call[-3]}",
		reply_markup=builder.as_markup()
	)


def _create_calendar(year, mounth=1):
	# вычисление сколько дней в месяце по году и месяцу
	days_in_month = monthrange(year, mounth)[1]

	mounth_alpha = replacements_month[mounth]

	builder = InlineKeyboardBuilder()

	builder.button(text="<<", callback_data=f"year_back_{year}")
	builder.button(text=str(year), callback_data="pass")
	builder.button(text=">>", callback_data=f"year_next_{year}")

	builder.button(text="<<", callback_data=f"month_back_{mounth}_{year}")
	builder.button(text=mounth_alpha, callback_data="pass")
	builder.button(text=">>", callback_data=f"month_next_{mounth}_{year}")

	for i in range(1, days_in_month + 1):
		builder.button(text=str(i), callback_data=f"day_{i}_{mounth}_{year}")

	if 35 - days_in_month != 7:
		for i in range(35 - days_in_month):
			builder.button(text=" ", callback_data=f"pass")

	builder.adjust(3, 3, 7, 7, 7, 7, 7)

	return builder.as_markup()

def now_calendar():
	now_year = datetime.now().year
	now_month = datetime.now().month
	now_weekday = datetime.now().weekday()
	now_day = datetime.now().day

	return _create_calendar(now_year, now_month)

