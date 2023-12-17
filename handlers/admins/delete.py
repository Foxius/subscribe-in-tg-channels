import sqlite3
from loader import bot
import config
from config import re, gr, cy, pu, channelsid


@bot.message_handler(commands=['delete'])
def delete_user(message):
    print(
        f"{pu}[LOG]{cy} Пользователь {gr}@{message.from_user.username}/{message.from_user.id} ({message.from_user.first_name} {message.from_user.last_name} {cy}использовал команду{re} delete")
    if message.chat.id in config.admins:
        msg = bot.send_message(message.chat.id, 'Нажмите на user_id пользователя и отправьте его')
        bot.register_next_step_handler(msg, delete_user_final)


def delete_user_final(message):
    conn = sqlite3.Connection('referrals.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM referrals WHERE user_id = ?", (int(message.text),))
    try:
        user_id = message.text
        for chat_id in config.channelsid:
            bot.kick_chat_member(chat_id, user_id)
            bot.unban_chat_member(chat_id, user_id)
            print(f"{user_id} удален из {chat_id}")
    except Exception as e:
        print(e)
    conn.commit()
    conn.close()
    bot.send_message(message.chat.id, f"Пользователь `{message.text}` удалён", parse_mode='Markdown')

    conn.close()


@bot.message_handler(commands=['deletechannels'])
def delete_channels(message):
    msg = bot.send_message(message.chat.id, 'Введите id пользователя для удаления его из каналов')
    bot.register_next_step_handler(msg, delete_channels_final)


def delete_channels_final(message):
    user_id = message.text
    msg = bot.send_message(message.chat.id, 'Начато удаление')
    for chat_id in channelsid:
        try:
            bot.kick_chat_member(chat_id, user_id)
            bot.unban_chat_member(chat_id, user_id)
            bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id,
                                  text=f"{user_id} удален из {chat_id}")
        except:
            continue

    bot.send_message(message.chat.id, 'Удаление завершено')
