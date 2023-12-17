import sqlite3
from loader import bot
from keyboards import main
from config import startmessage
from logger import log_message
from config import re, gr, cy, pu, ye
from datetime import datetime


@bot.message_handler(commands=['start'])
def start(message):
    print(f"{pu}[LOG]{cy} Пользователь {gr}@{message.from_user.username}/{message.from_user.id} ({message.from_user.first_name} {message.from_user.last_name} {cy}использовал команду{re} start")
    log_message(message.from_user.username, message.from_user.id, message.from_user.first_name,
                message.from_user.last_name, 'start')
    user_id = message.from_user.id
    ref_id = message.text.split(' ')[1] if len(message.text.split(' ')) > 1 else None
    conn = sqlite3.connect('referrals.db')
    cursor = conn.cursor()
    referrer1 = None
    referrer2 = None
    referrer3 = None

    cursor.execute("SELECT * FROM referrals WHERE user_id=?", (user_id,))
    user = cursor.fetchone()

    if ref_id is not None:
        cursor.execute("SELECT referrer1, referrer2 FROM referrals WHERE user_id=?", (ref_id,))
        ref = cursor.fetchone()
        if ref:
            referrer1 = ref_id
            referrer2 = ref[0]
            referrer3 = ref[1]
    username = f"@{message.from_user.username}"
    if user:
        if ref_id is not None:
            cursor.execute("UPDATE referrals SET referrer1 = ?, referrer2 = ?, referrer3 = ? WHERE user_id = ?",
                           (referrer1, referrer2, referrer3, user_id))
    else:
        cursor.execute("INSERT INTO referrals (user_id, username, referrer1, referrer2, referrer3, register_date) VALUES (?, ?, ?, ?, ?, ?)",
                       (user_id, username, referrer1, referrer2, referrer3, datetime.now().date()))

    conn.commit()
    conn.close()

    bot.send_message(message.chat.id, startmessage, reply_markup=main.keyboard(), parse_mode="Markdown")
