from loader import bot
from config import re, gr, cy, pu, ye
@bot.message_handler(commands=['ahelp'])
def ahelp(message):
    print(f"{pu}[LOG]{cy} Пользователь {gr}@{message.from_user.username}/{message.from_user.id} ({message.from_user.first_name} {message.from_user.last_name} {cy}использовал команду{re} ahelp")
    msg = '''/bc или /broadcast - Отправить массовое сообщение
/conversion - посмотреть конверсию
/delete - удалить пользователя из БД
/referrals - список рефералов
/refdelete - удалить баланс реферала
/stats - статистика
/status - статус
/deletechannels - удалить человека из каналов
/add_admins - добавить администратора
    '''
    bot.send_message(message.chat.id, msg)

