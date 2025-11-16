import requests

from config_reader import config
from settings import API_URL, MODEL


def get_answer_with_messages(messages: list) -> str:
	"""
	Функция принимает на вход текст и контекст. И возвращает ответ 

	:param message: list. {"role": "user", "content": user_message}
	
	:return : dict. Ответ API. Или ошибку
	"""
	API_KEY = config.api_token.get_secret_value()

	headers = {
		"Content-Type": "application/json",
		"Authorization": f"Bearer {API_KEY}"
	}

	data = {
		"model": MODEL,
		"messages": messages
	}

	response = requests.post(API_URL, headers=headers, json=data)
	try:
		response.raise_for_status()
	except requests.HTTPError as e:
		print(f"HTTP error: {e}, статус: {response.status_code}, ответ: {response.text}")
		return {"error": str(e), "status_code": response.status_code, "response": response.text}

	return response.json()
