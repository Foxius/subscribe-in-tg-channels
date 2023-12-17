from config import channelslistsub
from loader import bot
from logger import log_message
from config import re, gr, cy, pu, ye


@bot.message_handler(commands=['channels'])
def channels(message):
    print(f"{pu}[LOG]{cy} Пользователь {gr}@{message.from_user.username}/{message.from_user.id} ({message.from_user.first_name} {message.from_user.last_name} {cy}использовал команду{re} channels")
    log_message(message.from_user.username, message.from_user.id, message.from_user.first_name,
                message.from_user.last_name, 'channels')
    bot.send_message(message.chat.id, channelslistsub, parse_mode="Markdown")