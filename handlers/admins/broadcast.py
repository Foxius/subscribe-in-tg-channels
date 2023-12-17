import sqlite3

import config
from config import re, gr, cy, pu, ye
from loader import bot


@bot.message_handler(commands=['bc', 'broadcast'])
def broadcast_func(message):
    print(f"{pu}[LOG]{cy} Пользователь {gr}@{message.from_user.username}/{message.from_user.id} ({message.from_user.first_name} {message.from_user.last_name} {cy}использовал команду{re} broadcast")
    if message.chat.id in config.admins:
        msg = bot.send_message(message.chat.id, 'Введите сообщение для рассылки')
        bot.register_next_step_handler(msg, broadcast_func_final)


def broadcast_func_final(message):

    conn = sqlite3.Connection('referrals.db')
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM referrals")
    users = cursor.fetchall()
    msg = bot.send_message(message.chat.id, 'Cообщения отправляются')
    for user in users:
        try:
            bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id,
                                  text=f'Отправлено пользователю с ID {user[0]}')
            bot.send_message(user[0], message.text)
        except Exception as e:
            print(e)
            continue
    bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text=f'Рассылка завершена')
    conn.close()