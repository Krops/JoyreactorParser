import telebot
import json
from parser import get_m

bot = telebot.TeleBot('424337465:AAF7zdf3_sLe6n6-tibF_iC7ChRYoxl14Sk')

result = get_m()
print(result)
saved_keys_file = open('dict.json', "r")
saved_keys_json = set(json.load(saved_keys_file))
json_keys = json.dumps(list(result.keys()))
saved_keys_file = open('dict.json', "w")
saved_keys_file.write(json_keys)
diff = set(result.keys()) - saved_keys_json
for g in diff:
    for item in result.get(g):
        if 'jpeg' in item or 'png' in item:
            bot.send_photo('@joyreact_channel', photo=item)
        if 'gif' in item:
            bot.send_video('@joyreact_channel', video=item)
        else:
            bot.send_message('@joyreact_channel', text=item)

#bot.send_message('@joyreact_channel', "t")
#bot.send_media_group()
#bot.send_photo('@joyreact_channel', photo='http://img10.joyreactor.cc/pics/post/%D0%AD%D1%80%D0%BE%D1%82%D0%B8%D0%BA%D0%B0-%D0%9C%D0%B0%D1%80%D1%82%D0%B0-%D0%93%D1%80%D0%BE%D0%BC%D0%BE%D0%B2%D0%B0-7481233.jpeg')