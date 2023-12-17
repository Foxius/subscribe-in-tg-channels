import sqlite3

from loader import bot
import config


@bot.message_handler(commands=['add_admins'])
def add_admins(message):

    if message.chat.id in config.admins:
        msg = bot.send_message(message.chat.id, 'Введите id нового администратора')
        bot.register_next_step_handler(msg, add_admins_final)


def add_admins_final(message):
    new_admin = int(message.text)
    add_admin_to_db(new_admin)
    bot.send_message(message.chat.id, f'Администратор {new_admin} добавлен')


def add_admin_to_db(new_admin):
    conn = sqlite3.connect("referrals.db")
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO admins (tgid) VALUES (?)''', (new_admin,))
    conn.commit()
    conn.close()

