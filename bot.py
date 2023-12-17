import logging
import threading
import time
import traceback
import schedule
from tasks import checksub
from loader import bot
import importlib
import os
from logger import log_error
from config import re, gr, cy, pu, ye
from config import get_admins
def import_recursive(package_name):
    # Импортируем основной пакет
    globals()[package_name] = importlib.import_module(package_name)

    # Определяем путь к пакету на основе его __path__
    package_path = globals()[package_name].__path__[0]

    # Получаем список всех файлов и директорий внутри пакета
    for name in os.listdir(package_path):
        path = os.path.join(package_path, name)

        # Если это директория и есть __init__.py внутри, то это подпакет
        if os.path.isdir(path) and '__init__.py' in os.listdir(path):
            import_recursive(f"{package_name}.{name}")

        # Если это .py файл (исключая __init__.py), то это модуль
        elif name.endswith('.py') and name != '__init__.py':
            module_name = f"{package_name}.{name[:-3]}"
            print(module_name)
            globals()[module_name] = importlib.import_module(module_name)


import_recursive('handlers')

os.system('clear')

print(f"""
{re}╔═╗{cy}┌─┐{re}═╦═
{re}╚═╗{cy}├─┤{re} ║
{re}╚═╝{cy}┴ ┴{re}═╩═
by https://github.com/foxius
""")


def run_bot_polling():
    while True:
        try:
            bot.polling(none_stop=True, timeout=666)
        except Exception as e:
            print(f'Произошла ошибка: {traceback.format_exc()}')
            log_error('none', 'none', e)


bot_polling_thread = threading.Thread(target=run_bot_polling)
bot_polling_thread.start()
checksub.check_subscriptions()
schedule.every(23).hours.do(checksub.check_subscriptions)

while True:
    try:
        schedule.run_pending()
        time.sleep(1)
    except KeyboardInterrupt:
        bot_polling_thread.join()
        break
    except Exception as e:
        logging.error(f"Error in schedule: {e}")
        continue
