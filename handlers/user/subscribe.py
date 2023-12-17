import sqlite3
from datetime import datetime
from config import addonsubscr
from loader import bot
from logger import log_message
from config import re, gr, cy, pu, ye

@bot.message_handler(func=lambda message: message.text == "🏷️ Подписка")
def subscribe(message):
    print(f"{pu}[LOG]{cy} Пользователь {gr}@{message.from_user.username}/{message.from_user.id} ({message.from_user.first_name} {message.from_user.last_name} {cy}использовал команду{re} subscribe")
    log_message(message.from_user.username, message.from_user.id, message.from_user.first_name,
                message.from_user.last_name, "Подписка")
    conn = sqlite3.connect('referrals.db')
    cursor = conn.cursor()

    cursor.execute("SELECT tariff, tariff_end_date FROM referrals WHERE user_id=?", (message.from_user.id,))
    user_tariff_info = cursor.fetchone()
    conn.close()

    if user_tariff_info and user_tariff_info[0] and user_tariff_info[1]:
        tariff_end_date = datetime.strptime(user_tariff_info[1], "%Y-%m-%d")
        remaining_days = (tariff_end_date - datetime.now()).days
        bot.send_message(message.chat.id,
                         f'У вас активен тариф {user_tariff_info[0]}. До его окончания осталось {remaining_days} дней.' + addonsubscr,
                         parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id,
                         '⌛️ У Вас нет действующей подписки' + addonsubscr,
                         parse_mode="Markdown")