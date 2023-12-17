import sqlite3

import config
from config import re, gr, cy, pu, ye
from loader import bot


def get_referral_list():
    connection = sqlite3.connect('referrals.db')
    cursor = connection.cursor()

    cursor.execute('''
    SELECT user_id, 
           (SELECT COUNT(*) FROM referrals r1 WHERE r1.referrer1 = referrals.user_id) +
           (SELECT COUNT(*) FROM referrals r2 WHERE r2.referrer2 = referrals.user_id) +
           (SELECT COUNT(*) FROM referrals r3 WHERE r3.referrer3 = referrals.user_id) AS total_invites,
           SUM(balance) as total_rewards
    FROM referrals
    GROUP BY user_id
    HAVING total_rewards > 0
    ''')

    referral_list = cursor.fetchall()
    connection.close()
    return referral_list


def reset_user_balance(user_id):
    connection = sqlite3.connect('referrals.db')
    cursor = connection.cursor()

    cursor.execute('''
    UPDATE referrals
    SET balance = 0
    WHERE user_id = ?
    ''', (user_id,))

    connection.commit()
    connection.close()


@bot.message_handler(commands=['referrals'])
def referrals(message):
    print(f"{pu}[LOG]{cy} Пользователь {gr}@{message.from_user.username}/{message.from_user.id} ({message.from_user.first_name} {message.from_user.last_name} {cy}использовал команду{re} referrals")
    if message.chat.id in config.admins:
        data = get_referral_list()
        msg = ''
        for user in data:
            if user[1] > 0:
                msg += f"Пользователь `{user[0]}` пригласил {user[1]}. Баланс {user[2]}\n\n"

        bot.send_message(message.chat.id, msg, parse_mode='Markdown')


@bot.message_handler(commands=['refdelete'])
def refdelete(message):
    if message.chat.id in config.admins:
        msg = bot.send_message(message.chat.id, 'Введите id пользователя для обнуление баланса')
        bot.register_next_step_handler(msg, refdelete_final)


def refdelete_final(message):
    user_id = message.text
    reset_user_balance(user_id)
    bot.reply_to(message, f"Баланс пользователя {user_id} обнулен.")
