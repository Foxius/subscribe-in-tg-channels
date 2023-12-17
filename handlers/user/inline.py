from telebot import types
import sqlite3
from datetime import datetime, timedelta
from loader import bot
from config import tariffc1, tariffc2, tariffc3, requizit, tariff_info_dict, admin_id, channelsdict
from handlers.admins.status import get_users_list_by_category, generate_markup

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "1m":
        details = f"Тариф на 1 месяц - {tariffc1} USDT. Реквизиты для оплаты: `{requizit}` USDT BEP 20"
        tariff_info_dict[call.message.chat.id] = {"tariff": "1m"}
    elif call.data == "3m":
        details = f"Тариф на 3 месяца - {tariffc2} USDT. Реквизиты для оплаты: `{requizit}` USDT BEP 20"
        tariff_info_dict[call.message.chat.id] = {"tariff": "3m"}
    elif call.data == "6m":
        details = f"Тариф на 6 месяцев - {tariffc3} USDT. Реквизиты для оплаты: `{requizit}` USDT BEP 20"
        tariff_info_dict[call.message.chat.id] = {"tariff": "6m"}
    elif call.data == "free":
        details = f"Бесплатный тариф. Длительность 1 сутки"
        tariff_info_dict[call.message.chat.id] = {"tariff": "free"}

    if call.data in ["1m", "3m", "6m"]:
        keyboard = types.InlineKeyboardMarkup()
        pay_button = types.InlineKeyboardButton(text="✅ Я оплатил", callback_data="paid")
        keyboard.add(pay_button)
        bot.send_message(call.message.chat.id, details, reply_markup=keyboard, parse_mode='Markdown')
    elif call.data == "free":
        keyboard = types.InlineKeyboardMarkup()
        pay_button = types.InlineKeyboardButton(text="✅ Подтвердить",
                                                callback_data=f"freebutton_{call.message.chat.id}_{call.message.from_user.username}")
        keyboard.add(pay_button)
        bot.send_message(call.message.chat.id, details, reply_markup=keyboard, parse_mode='Markdown')
    elif call.data == "paid":
        bot.send_message(call.message.chat.id, "Пожалуйста, отправьте скриншот оплаты.")
    elif "freebutton" in call.data:
        try:
            user_id = call.data.split('_')[1]
        except IndexError:
            user_id = call.message.chat.id  # Fallback to chat id if user_id is not present in call.data
        end_date = datetime.now() + timedelta(days=1)
        conn = sqlite3.connect('referrals.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT use_free FROM referrals WHERE user_id = ?''', (user_id,))
        result = cursor.fetchone()
        conn.close()
        if result[0] in ['True', True, 1, "1"]:
            bot.send_message(call.message.chat.id, "Вы уже использовали бесплатную подписку!")

        else:
            tariff_price = 0
            tariff_name = "Бесплатный"
            try:
                conn = sqlite3.connect('referrals.db')
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE referrals SET balance = balance + ?, tariff = ?, tariff_end_date = ?, use_free = ? WHERE "
                    "user_id = ?",
                    (tariff_price, tariff_name, end_date.strftime("%Y-%m-%d"), True, user_id))

                conn.commit()
                conn.close()
            except Exception as e:
                print(e)
            bot.send_message(admin_id,
                             f"Пользователь {call.data.split('_')[1]} (@{call.from_user.username}) активировал "
                             f"бесплатную подписку")

            keyboard = types.InlineKeyboardMarkup()
            for channelname, link in channelsdict.items():
                button = types.InlineKeyboardButton(text=f"{channelname}", url=link)
                keyboard.add(button)
            bot.send_message(user_id, "Присоединяйтесь к нашим каналам:", reply_markup=keyboard)
    elif "confirm" in call.data:
        bot.send_message(admin_id, "Оплата Подтверждена. Спасибо!")
        user_id = call.data.split('_')[1]
        tariff = tariff_info_dict[int(user_id)]["tariff"]

        if tariff == "1m":
            end_date = datetime.now() + timedelta(days=30)
            tariff_price = tariffc1
            tariff_name = "1 месяц"
        elif tariff == "3m":
            end_date = datetime.now() + timedelta(days=90)
            tariff_price = tariffc2
            tariff_name = "3 месяца"
        elif tariff == "6m":
            end_date = datetime.now() + timedelta(days=180)
            tariff_price = tariffc3
            tariff_name = "6 месяцев"

        conn = sqlite3.connect('referrals.db')
        cursor = conn.cursor()

        cursor.execute("UPDATE referrals SET balance = balance + ?, tariff = ?, tariff_end_date = ? WHERE user_id = ?",
                       (tariff_price, tariff_name, end_date.strftime("%Y-%m-%d"), user_id))

        cursor.execute("SELECT referrer1, referrer2, referrer3 FROM referrals WHERE user_id=?", (user_id,))
        referrers = cursor.fetchone()

        if referrers:
            if referrers[0]:
                cursor.execute("UPDATE referrals SET balance = balance + ? WHERE user_id = ?",
                               (tariff_price * 0.3, referrers[0]))
            if referrers[1]:
                cursor.execute("UPDATE referrals SET balance = balance + ? WHERE user_id = ?",
                               (tariff_price * 0.2, referrers[1]))
            if referrers[2]:
                cursor.execute("UPDATE referrals SET balance = balance + ? WHERE user_id = ?",
                               (tariff_price * 0.1, referrers[2]))

        conn.commit()
        conn.close()
        bot.send_message(user_id, "Ваша оплата была подтверждена. Спасибо!")

        keyboard = types.InlineKeyboardMarkup()
        for channelname, link in channelsdict.items():
            button = types.InlineKeyboardButton(text=f"{channelname}", url=link)
            keyboard.add(button)
        bot.send_message(user_id, "Присоединяйтесь к нашим каналам:",
                         reply_markup=keyboard)  # Add a 1 second delay between each request

    if call.data in ["activated", "trial", "subscribed"]:
        users_list = get_users_list_by_category(call.data)
        response = "\n".join([f"Пользователь {user_id}" for user_id in users_list])
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=response, reply_markup=generate_markup())
    elif call.data == "back":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите категорию:", reply_markup=generate_markup())

    bot.answer_callback_query(call.id)
