import sqlite3
from loader import bot
from config import re, gr, cy, pu, ye

@bot.chat_join_request_handler()
def channel_approve(chat_join_request):

    chat_id = chat_join_request.chat.id
    user_chat_id = chat_join_request.user_chat_id

    conn = sqlite3.connect('referrals.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT id FROM referrals WHERE user_id = ? AND tariff IS NOT NULL''', (int(user_chat_id),))

    user = cursor.fetchall()
    if user:
        bot.approve_chat_join_request(chat_id, user_chat_id)
    else:
        bot.send_message(user_chat_id, 'Ваша подписка закончилась. вы не можете вступить в канал!')
        bot.decline_chat_join_request(chat_id, user_chat_id)