import configparser
import json

import telebot
from telebot.types import InputMediaPhoto, InputMediaVideo

from parser import get_m

config = configparser.ConfigParser()
config.read('config.ini')
token = ''
if 'token' in config:
    token = config['token']
bot = telebot.TeleBot(token)
url = 'http://joyreactor.cc'
result = get_m()
print(result)
saved_keys_file = open('dict.json', "r")
saved_keys_json = set(json.load(saved_keys_file))
json_keys = json.dumps(list(result.keys()))
saved_keys_file = open('dict.json', "w")
saved_keys_file.write(json_keys)
diff = set(result.keys()) - saved_keys_json
for g in diff:
    item_list = []
    text = ""
    url_text = f"{url}{g}"
    for item in result.get(g):
        if 'jpeg' in item:
            media = InputMediaPhoto(media=item)
            item_list.append(media)
        elif 'png' in item:
            media = InputMediaPhoto(media=item)
            item_list.append(media)
        elif 'mp4' in item:
            media = InputMediaVideo(media=item)
            item_list.append(media)
        elif 'gif' in item:
            media = InputMediaVideo(media=item)
            item_list.append(media)
        else:
            text = text + " " + item
    if len(item_list) > 0:
        if len(text) > 1024:
            bot.send_message('@joyreact_channel', text=text, disable_web_page_preview=True)
            item_list[0].caption = url_text
        else:
            item_list[0].caption = text + '\n' + url_text
        bot.send_media_group('@joyreact_channel', item_list)
    else:
        text = text + '\n' + url_text
        bot.send_message('@joyreact_channel', text=text, disable_web_page_preview=True)
