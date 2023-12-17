import sqlite3
from datetime import datetime
from config import channelsid
from loader import bot


def check_subscriptions():
    conn = sqlite3.connect('referrals.db')
    cursor = conn.cursor()

    cursor.execute("SELECT user_id, tariff_end_date, tariff FROM referrals WHERE tariff_end_date <= ?",
                   (datetime.now().strftime("%Y-%m-%d"),))
    expired_subscriptions = cursor.fetchall()
    for subscription in expired_subscriptions:
        try:
            user_id = subscription[0]

            for chat_id in channelsid:
                bot.kick_chat_member(chat_id, user_id)
                bot.unban_chat_member(chat_id, user_id)
                print(f"{user_id} удален из {chat_id}")
            cursor.execute("UPDATE referrals SET tariff = NULL, tariff_end_date = NULL WHERE user_id = ?", (user_id,))
        except Exception as e:
            print(e)
            continue

    conn.commit()
    conn.close()
