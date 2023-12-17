from loader import bot
from logger import log_message
from config import re, gr, cy, pu, ye


@bot.message_handler(func=lambda message: message.text == "🚨 Поддержка")
def support(message):
    print(f"{pu}[LOG]{cy} Пользователь {gr}@{message.from_user.username}/{message.from_user.id} ({message.from_user.first_name} {message.from_user.last_name} {cy}использовал команду{re} support")
    log_message(message.from_user.username, message.from_user.id, message.from_user.first_name,
                message.from_user.last_name, 'support')
    bot.send_message(message.chat.id,
                     '▫️Подробно опишите свой вопрос в аккаунт поддержки, рабочее время с 10 до 20 по МСК @privat_service')