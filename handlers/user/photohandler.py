from telebot import types
from loader import bot
from config import admin_id
from logger import log_message, log_error
from config import re, gr, cy, pu, ye

@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    try:
        print(f"[LOG] Пользователь @{message.from_user.username}/{message.from_user.id} ({message.from_user.first_name} {message.from_user.last_name} использовал команду photo")
        log_message(message.from_user.username, message.from_user.id, message.from_user.first_name,
                    message.from_user.last_name, 'photo')
        chat_id = message.chat.id

        bot.forward_message(admin_id, chat_id, message.message_id)

        bot.send_message(admin_id,
                         f"ID пользователя: {chat_id}, имя пользователя: @{message.from_user.username}, {chat_id}")

        keyboard = types.InlineKeyboardMarkup()
        confirm_button = types.InlineKeyboardButton(text="✅ Подтвердить оплату", callback_data=f"confirm_{chat_id}")
        keyboard.add(confirm_button)
        bot.send_message(admin_id, "Пожалуйста, подтвердите оплату", reply_markup=keyboard)

        bot.reply_to(message, "Фотография принята, ожидайте подтверждения администратора.")

    except Exception as e:
        log_error(message.from_user.username, message.from_user.id, e)
        bot.reply_to(message, e)