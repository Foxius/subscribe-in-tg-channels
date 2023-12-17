import sqlite3
from loader import bot
from logger import log_message
from config import re, gr, cy, pu, ye


@bot.message_handler(func=lambda message: message.text == "📝 Партнёрская Программа")
def affiliate(message):
    print(f"{pu}[LOG]{cy} Пользователь {gr}@{message.from_user.username}/{message.from_user.id} ({message.from_user.first_name} {message.from_user.last_name} {cy}использовал команду{re} affiliate")
    log_message(message.from_user.username, message.from_user.id, message.from_user.first_name,
                message.from_user.last_name, "Партнёрская Программа")
    conn = sqlite3.connect('referrals.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), COALESCE(SUM(balance), 0) FROM referrals WHERE referrer1=?",
                   (message.from_user.id,))
    stats_level1 = cursor.fetchone() or [0, 0]

    cursor.execute("SELECT COUNT(*), COALESCE(SUM(balance), 0) FROM referrals WHERE referrer2=?",
                   (message.from_user.id,))
    stats_level2 = cursor.fetchone() or [0, 0]

    cursor.execute("SELECT COUNT(*), COALESCE(SUM(balance), 0) FROM referrals WHERE referrer3=?",
                   (message.from_user.id,))
    stats_level3 = cursor.fetchone() or [0, 0]

    conn.close()

    total_balance = int(stats_level1[1]) * 0.3 + int(stats_level2[1]) * 0.2 + int(stats_level3[1]) * 0.1
    total_refs = int(stats_level1[0]) + int(stats_level2[0]) + int(stats_level3[0])
    total_balance_no_percent = int(stats_level1[1]) + int(stats_level2[1]) + int(stats_level3[1])
    stats_message = f"""
    ▪️Ваша реферальная ссылка: 
https://t.me/{bot.getMe().username}?start={message.chat.id}

▪️Сумма к выводу: {total_balance} $
▪️Кол-во зарегистрированных: {total_refs} чел(общее) 

▪️Купили подписки: {total_balance_no_percent}$ (общее) 
1 уровень - {stats_level1[0]} чел
2 уровень - {stats_level2[0]} чел 
3 уровень - {stats_level3[0]} чел 

▪️Условия партнерской программы: 
При оплате и продлении подписок вашими люди либо их приглашенными вы получаете вознаграждение. 

1 уровень - 30% от оплат и продлений 
2 уровень - 20% от оплат и продлений 
3 уровень - 10% от оплат и продлений 

▪️За выводом средств обращайтесь к администратору"""
    bot.send_message(message.chat.id, stats_message)