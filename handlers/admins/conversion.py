import sqlite3

import config
from loader import bot
from config import re, gr, cy, pu, ye


@bot.message_handler(commands=['conversion'])
def conversion_func(message):
    print(f"{pu}[LOG]{cy} Пользователь {gr}@{message.from_user.username}/{message.from_user.id} ({message.from_user.first_name} {message.from_user.last_name}) {cy}использовал команду{re} conversion")

    if message.chat.id in config.admins:
        conn = sqlite3.Connection('referrals.db')
        cursor = conn.cursor()

        # Получаем общее количество пользователей и их тарифы
        cursor.execute("SELECT user_id, tariff FROM referrals")
        users = cursor.fetchall()

        total_users = len(users)
        paid_users = sum(1 for user in users if user[1] and user[1] != 'Бесплатный')
        free_users = total_users - paid_users

        # Расчет конверсии Зарегистрированных в Тестовых и Платных пользователей
        conversion_reg_to_test = (free_users / total_users) * 100 if total_users else 0
        conversion_reg_to_paid = (paid_users / total_users) * 100 if total_users else 0



        response = (f"*Зарегистрировано в боте:* {total_users} человек\n"
                    f"*Тестовый период:* {free_users}\n"
                    f"*Купили подписку:* {paid_users}\n"
                    f"*Конверсия:*\n"
                    f"Зарег - Тест: {conversion_reg_to_test:.2f}%\n"
                    f"Зарег - Купил: {conversion_reg_to_paid:.2f}%\n")
                    # f"Тест - Купил: {conversion_test_to_paid:.2f}%")

        bot.send_message(message.chat.id, response, parse_mode='Markdown')

        conn.close()


