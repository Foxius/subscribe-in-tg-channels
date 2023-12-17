from telebot import types


def keyboard():
    keyboards = types.ReplyKeyboardMarkup(resize_keyboard=True)
    tarifs = types.KeyboardButton("💲 Тарифы")
    subscr = types.KeyboardButton("🏷️ Подписка")
    affiliate = types.KeyboardButton("📝 Партнёрская Программа")
    support = types.KeyboardButton("🚨 Поддержка")
    keyboards.row(tarifs, subscr)
    keyboards.row(affiliate, support)
    return keyboards
