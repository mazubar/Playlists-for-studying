import telebot
bot = telebot.TeleBot()#token from BotFather

from telebot import types

import random

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials 

import requests
import json

cid = #developer id
secret = #secret id
user_id= #user id
token = #Spotify API token

def get_link(json_response,token):
	uris=[]
	for i,j in enumerate(json_response['tracks']):
		uris.append(j['uri'])

	endpoint_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"

	request_body = json.dumps({"name": "Playlist for studying",
								"description": "Auto generated playlist",
								"public": True})

	response = requests.post(url = endpoint_url, data = request_body, headers={"Content-Type":"application/json", "Authorization":f"Bearer {token}"})

	url = response.json()['external_urls']['spotify']

	playlist_id = response.json()['id']

	endpoint_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

	request_body = json.dumps({"uris" : uris})
	response = requests.post(url = endpoint_url, data = request_body, headers={"Content-Type":"application/json", "Authorization":f"Bearer {token}"})

	return url


def relaxation():

    endpoint_url = "https://api.spotify.com/v1/recommendations?"
    limit=20

    seed_genres="classic,indie,ambient"
    max_danceability=0.3
    max_energy=0.1

    query = f'{endpoint_url}limit={limit}&seed_genres={seed_genres}&max_energy={max_energy}&max_danceability={max_danceability}'
    response=requests.get(query, headers={"Content-Type":"application/json", 
                            "Authorization":f"Bearer {token}"})
    return get_link(response.json(),token)

def concentration():

    endpoint_url = "https://api.spotify.com/v1/recommendations?"
    limit=20
    
    seed_genres="ambient,new wave,indie"
    min_danceability=0.2
    max_danceability=0.5
    min_energy=0.1
    max_energy=0.25
    min_tempo=110

    query = f'{endpoint_url}limit={limit}&seed_genres={seed_genres}&max_energy={max_energy}&min_danceability={min_danceability}&max_danceability={max_danceability}&max_speechiness=0.3'

    response=requests.get(query, 
                   headers={"Content-Type":"application/json", 
                            "Authorization":f"Bearer {token}"})
    return get_link(response.json(),token)

def engagement():

    endpoint_url = "https://api.spotify.com/v1/recommendations?"
    limit=20
    
    seed_genres="alternative, indie"
    min_danceability=0.4
    max_danceability=0.7
    min_energy=0.2
    max_energy=0.6
    min_tempo=120

    query = f'{endpoint_url}limit={limit}&seed_genres={seed_genres}&max_energy={max_energy}&min_danceability={min_danceability}&max_danceability={max_danceability}&max_speechiness=0.3'

    response=requests.get(query, 
                   headers={"Content-Type":"application/json", 
                            "Authorization":f"Bearer {token}"})
    url=get_link(response.json(),token)
    return (url)

def hello():
	hello = ['Привет! Я помогу тебе создать плейлист для учебы.', "Рад тебя видеть! Готов создавать плейлист?"]
	return random.choice(hello)

def goodbye():
	goodbye = ['Пока!', "Приходи ко мне еще!", "Уже уходишь? :( Ну давай, удачи!", "Пока! Надеюсь, я тебе помог!"]
	return random.choice(goodbye)

def thanks():
	thanks = ['Обращайся!', "Не за что.", "Всегда пожалуйста!", "Надеюсь, я тебе помог!"]
	return random.choice(thanks)

def hope():
	hello = ['Надеюсь, тебе понравится!', "Приятного прослушивания :)", "А вот и плейлист! Наслаждайся."]
	return random.choice(hello)

def undefined():
	undefined = ['Не понимаю тебя :( ', "О чем ты? "]
	return random.choice(undefined) + " Чтобы получить плейлист, поздоровайся со мной."

def intent(text):
    text = text.lower()
    
    for word in ['прив', 'здравствуй', 'добр', 'hi', 'хай']:
        if word in text:
            return 'hello'
        
    for word in ['пок', 'до свидан', 'спокойной', "увидимся"]:
        if word in text:
            return 'goodbye'

    for word in ["спасибо", "спс", "благодарю"]:
        if word in text:
            return 'thanks'
    for word in ["еще", "друго", "повтор"]:
        if word in text:
            return 'more'

    return 'undefined'

def send_intent(text):
    if intent(text)=='hello':
        return hello()
    elif intent(text)=='goodbye':
        return goodbye()
    elif intent(text)=='thanks':
        return thanks()
    else:
        return undefined()

@bot.message_handler(commands=['start'])
def welcome_start(message):
    bot.send_message(message.chat.id, 'Привет! Я могу сгенерировать для тебя плейлист для учебы!\nP.S. Я дам тебе ссылку на созданный плейлист на платформе Spotify :)\nПроверь меня.')
 
# Тут работаем с командой help
@bot.message_handler(commands=['help'])
def welcome_help(message):
    bot.send_message(message.chat.id, 'Чтобы получить плейлист поздоровайся со мной, и я помогу!')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if intent(message.text) == 'hello':

    	bot.send_message(message.from_user.id, send_intent(message.text))

    	keyboard = types.InlineKeyboardMarkup()

    	key_relaxation = types.InlineKeyboardButton(text='Расслабиться', callback_data='relax')
    	keyboard.add(key_relaxation)

    	key_concentration = types.InlineKeyboardButton(text='Сконцентрироваться', callback_data='concentrate')
    	keyboard.add(key_concentration)

    	key_engagement = types.InlineKeyboardButton(text='Избавиться от скуки', callback_data='engage')
    	keyboard.add(key_engagement)

    	bot.send_message(message.from_user.id, text='Что тебе сейчас хочется?', reply_markup=keyboard)

    elif intent(message.text) == 'more':

    	bot.send_message(message.from_user.id, "Хочешь еще плейлист? Ладушки.")

    	keyboard = types.InlineKeyboardMarkup()

    	key_relaxation = types.InlineKeyboardButton(text='Расслабиться', callback_data='relax')
    	keyboard.add(key_relaxation)

    	key_concentration = types.InlineKeyboardButton(text='Сконцентрироваться', callback_data='concentrate')
    	keyboard.add(key_concentration)

    	key_engagement = types.InlineKeyboardButton(text='Избавиться от скуки', callback_data='engage')
    	keyboard.add(key_engagement)

    	bot.send_message(message.from_user.id, text='Что тебе сейчас хочется?', reply_markup=keyboard)
    else:
    	bot.send_message(message.from_user.id, send_intent(message.text))

@bot.callback_query_handler(func=lambda call: True)

def callback_worker(call):
	if call.data == "relax": 
		msg = relaxation()
		bot.send_message(call.message.chat.id, msg)
		bot.send_message(call.message.chat.id, hope())
	if call.data == "concentrate":
		msg = concentration()
		bot.send_message(call.message.chat.id, msg)
		bot.send_message(call.message.chat.id, hope())
	if call.data == "engage":
		msg = engagement()
		bot.send_message(call.message.chat.id, msg)
		bot.send_message(call.message.chat.id, hope())


bot.polling(none_stop=True, interval=0)
