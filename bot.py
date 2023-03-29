import configparser
import json
import time
from datetime import datetime

import telebot
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from telebot.types import InputMediaPhoto, InputMediaVideo

from parser import get_m

config = configparser.ConfigParser()
config.read('config.ini')
token = ''
if 'AUTH' in config:
    token = config['AUTH']['token']
bot = telebot.TeleBot(token)
url = 'http://joyreactor.cc'


def check_sent_messages(result):
    saved_keys_file = open('dict.json', "r")
    saved_keys_json = set(json.load(saved_keys_file))
    json_keys = json.dumps(list(result.keys()))
    saved_keys_file = open('dict.json', "w")
    saved_keys_file.write(json_keys)
    diff = set(result.keys()) - saved_keys_json
    return diff


def send_message(result, diff):
    for g in diff:
        item_list = []
        text = ""
        url_text = f"{url}{g}"
        for item in result.get(g):
            if 'jpeg' in item:
                media = InputMediaPhoto(media=f'{1}'.format(item))
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
        time.sleep(0.5)


scheduler = BlockingScheduler()


@scheduler.scheduled_job(IntervalTrigger(minutes=10), next_run_time=datetime.now())
def some_job():
    result = get_m()
    send_message(result, check_sent_messages(result))


scheduler.start()