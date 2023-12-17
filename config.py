import sqlite3


def get_admins():
    conn = sqlite3.connect('referrals.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT tgid FROM admins''')
    rows = cursor.fetchall()
    admin_list = []
    for row in rows:
        admin_list.append(row[0])
    return admin_list


TOKEN = ''
admin_id = -864926434
channelsid = [-100***********, -100***********, -100***********, -100***********,-100***********]
requizit = 'b289208430r0jif00MF0j0f3onwe20'
tariffc1 = 50
tariffc2 = 120
tariffc3 = 200


admins = get_admins()
tariff_info_dict = {}
re = "\033[1;31m"
gr = "\033[1;32m"
cy = "\033[1;36m"
pu = "\033[1;35m"
ye = "\033[1;33m"

startmessage = """*Добро пожаловать в [NAME].* 

▫️Мы отобрали лучшие приватные телеграмм каналы/чаты о [TOPIC OF THE CHANNELS]

— *[NAME OF THE CHANNEL]*
— *[NAME OF THE CHANNEL]*
— *[NAME OF THE CHANNEL]*
— *[NAME OF THE CHANNEL]*
— *[NAME OF THE CHANNEL]*

—  *И другие. Полный список тут - /channels *

☑️ Предоставляем бесплатный доступ на сутки, далее необходимо приобрести подписку. 

💭*Продолжим в разделе тарифы*"""

channelslist = """**Полный список каналов**: 
— *[NAME OF THE CHANNEL]*
— *[NAME OF THE CHANNEL]*
— *[NAME OF THE CHANNEL]*
— *[NAME OF THE CHANNEL]*
— *[NAME OF THE CHANNEL]*
— *[NAME OF THE CHANNEL]*
— *[NAME OF THE CHANNEL]*
— *[NAME OF THE CHANNEL]*
"""
channelslistsub = """**Полный список каналов**: 
- [NAME OF THE CHANNEL](LINK OF THE CHANNEL)
- [NAME OF THE CHANNEL](LINK OF THE CHANNEL)
- [NAME OF THE CHANNEL](LINK OF THE CHANNEL)
- [NAME OF THE CHANNEL](LINK OF THE CHANNEL)
- [NAME OF THE CHANNEL](LINK OF THE CHANNEL)
- [NAME OF THE CHANNEL](LINK OF THE CHANNEL)
- [NAME OF THE CHANNEL](LINK OF THE CHANNEL)
- [NAME OF THE CHANNEL](LINK OF THE CHANNEL)
- [NAME OF THE CHANNEL](LINK OF THE CHANNEL)
- [NAME OF THE CHANNEL](LINK OF THE CHANNEL)
- [NAME OF THE CHANNEL](LINK OF THE CHANNEL)
- [NAME OF THE CHANNEL](LINK OF THE CHANNEL)
- [NAME OF THE CHANNEL](LINK OF THE CHANNEL)"""
addonsubscr = """

▪️Полный список всех доступных каналов тут /channels

▪️Инструкция, как пользоваться ботом 

▪️Ознакомьтесь с тарифами, нажав на соответствующую кнопку"""

channelsdict = {
    "NAME OF THE CHANNEL": "LINK OF THE CHANNEL",
    "NAME OF THE CHANNEL": "LINK OF THE CHANNEL",
    "NAME OF THE CHANNEL": "LINK OF THE CHANNEL",
    "NAME OF THE CHANNEL": "LINK OF THE CHANNEL",
    "NAME OF THE CHANNEL": "LINK OF THE CHANNEL",
    "NAME OF THE CHANNEL": "LINK OF THE CHANNEL",
    "NAME OF THE CHANNEL": "LINK OF THE CHANNEL",
    "NAME OF THE CHANNEL": "LINK OF THE CHANNEL",
    "NAME OF THE CHANNEL": "LINK OF THE CHANNEL",
    "NAME OF THE CHANNEL": "LINK OF THE CHANNEL",
    "NAME OF THE CHANNEL": "LINK OF THE CHANNEL",
    "NAME OF THE CHANNEL": "LINK OF THE CHANNEL",
    "NAME OF THE CHANNEL": "LINK OF THE CHANNEL"
}
