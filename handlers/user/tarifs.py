import sqlite3
from datetime import datetime
from telebot import types
from loader import bot
from config import tariffc1, tariffc2, tariffc3
from logger import log_message
from config import re, gr, cy, pu, ye


@bot.message_handler(func=lambda message: message.text == "💲 Тарифы")
def tarifs(message):
    print(f"{pu}[LOG]{cy} Пользователь {gr}@{message.from_user.username}/{message.from_user.id} ({message.from_user.first_name} {message.from_user.last_name} {cy}использовал команду{re} tarifs")
    log_message(message.from_user.username, message.from_user.id, message.from_user.first_name,
                message.from_user.last_name, 'Тарифы')
    conn = sqlite3.connect('referrals.db')
    cursor = conn.cursor()

    cursor.execute("SELECT tariff, tariff_end_date FROM referrals WHERE user_id=?", (message.from_user.id,))
    user_tariff_info = cursor.fetchone()
    conn.close()

    if user_tariff_info and user_tariff_info[0] and user_tariff_info[1]:
        tariff_end_date = datetime.strptime(user_tariff_info[1], "%Y-%m-%d")
        remaining_days = (tariff_end_date - datetime.now()).days
        bot.send_message(message.chat.id,
                         f'У вас уже активна подписка {user_tariff_info[0]}. До ее окончания осталось {remaining_days} дней.')
    else:
        keyboard = types.InlineKeyboardMarkup()
        free = types.InlineKeyboardButton(text=f'Бесплатный тариф на 1 сутки', callback_data='free')
        keyboard.add(free)
        tariff1 = types.InlineKeyboardButton(text=f'Тариф на 1 месяц - {tariffc1} USDT', callback_data='1m')
        keyboard.add(tariff1)
        tariff2 = types.InlineKeyboardButton(text=f'Тариф на 3 месяца - {tariffc2} USDT', callback_data='3m')
        keyboard.add(tariff2)
        tariff3 = types.InlineKeyboardButton(text=f'Тариф на 6 месяцев - {tariffc3} USDT', callback_data='6m')
        keyboard.add(tariff3)
        bot.send_message(message.chat.id, 'Выберите один из наших тарифов:', reply_markup=keyboard)