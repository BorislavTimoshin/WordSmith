import requests
import json
from Py_files.config import YNDX_DCT_API_KEY
from Py_files.database import db

with open('data/parts_of_speech.json', 'r', encoding='utf-8') as json_file:
    parts_of_speech = json.load(json_file)


def get_info_about_word(human_id, word: str) -> str:
    language = db.get_language(human_id)
    if language == 'rus':
        language = 'ru-ru'
    elif language == 'eng':
        language = 'en-en'
    url = f"https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key={YNDX_DCT_API_KEY}&lang={language}&text={word}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if not data['def']:
            return "Введите слово корректно"
        part_of_speech = parts_of_speech[data['def'][0]['pos']]
        text = f"<b>{word.capitalize()}</b> — {part_of_speech}\n\n"
        counter = 1
        for mean in data['def'][0]['tr']:
            text += f"<b>Значение {counter}</b> — {mean['text']}\n"
            try:
                synonyms = []
                for synonym in mean['syn']:
                    synonyms.append(synonym['text'])
                text += '<b>Синонимы: </b>' + ', '.join(synonyms) + '\n\n'
            except KeyError:
                text += '<b>Синонимы: </b>' + 'нет\n\n'
            counter += 1
        return text
    if response.status_code == 403:
        return 'Превышено суточное ограничение на количество запросов'
    if response.status_code == 413:
        return 'Превышен максимальный размер текста'
    return 'Бот временно не работает'
