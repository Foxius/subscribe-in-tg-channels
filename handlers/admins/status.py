import sqlite3
from telebot import types

import config
from loader import bot
from config import re, gr, cy, pu, ye

def get_users_list_by_category(category):
    connection = sqlite3.connect('referrals.db')
    cursor = connection.cursor()

    if category == 'activated':
        cursor.execute("SELECT user_id FROM referrals WHERE tariff IS NULL")
    elif category == 'trial':
        cursor.execute("SELECT user_id FROM referrals WHERE tariff = 'Бесплатный'")
    elif category == 'subscribed':
        cursor.execute("SELECT user_id FROM referrals WHERE tariff NOT NULL AND tariff != 'Бесплатный'")

    users = cursor.fetchall()
    connection.close()
    return [user[0] for user in users]


def generate_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        types.InlineKeyboardButton("Активировали бота", callback_data="activated"),
        types.InlineKeyboardButton("Тестовый период", callback_data="trial"),
        types.InlineKeyboardButton("Купили подписку", callback_data="subscribed"),
    ]
    markup.add(*buttons)
    return markup

@bot.message_handler(commands=['status'])
def send_welcome(message):
    print(f"{pu}[LOG]{cy} Пользователь {gr}@{message.from_user.username}/{message.from_user.id} ({message.from_user.first_name} {message.from_user.last_name} {cy}использовал команду{re} status")
    if message.chat.id in config.admins:
        markup = generate_markup()
        bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=markup)
