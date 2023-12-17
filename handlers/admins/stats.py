import sqlite3

import config
from config import re, gr, cy, pu, ye
from loader import bot


@bot.message_handler(commands=['stats'])
def send_stats(message):
    print(f"{pu}[LOG]{cy} Пользователь {gr}@{message.from_user.username}/{message.from_user.id} ({message.from_user.first_name} {message.from_user.last_name} {cy}использовал команду{re} stats")
    if message.chat.id in config.admins:
        conn = sqlite3.Connection('referrals.db')
        cursor = conn.cursor()

        cursor.execute("SELECT id, user_id, register_date, tariff, tariff_end_date, username FROM referrals")
        users = cursor.fetchall()

        response = "Список пользователей:\n"
        message_count = 0
        for user in users:
            user_info = f"User ID: `{user[1]}`, Username {user[5]} Зарегистрирован *{user[2]}*{f', Тариф: *{user[3]}*' if user[3] and user[4] else ''}\n\n"
            if len(response) + len(user_info) > 4096:  # Проверка на превышение лимита Telegram
                bot.send_message(message.chat.id, response, parse_mode='Markdown')
                response = user_info
                message_count += 1
            else:
                response += user_info

        if message_count == 0 or len(response) > 0:
            response += f"\nОбщее количество пользователей: {len(users)}"
            bot.send_message(message.chat.id, response, parse_mode='Markdown')

        conn.close()
