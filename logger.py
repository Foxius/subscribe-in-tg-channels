import logging
import logging.handlers

# Настройка обработчика для записи всех сообщений в файл
all_messages_handler = logging.handlers.RotatingFileHandler('all_messages.log', backupCount=1)
all_messages_handler.setLevel(logging.INFO)

# Настройка обработчика для записи ошибок в отдельный файл
error_handler = logging.handlers.RotatingFileHandler('errors.log', backupCount=1)
error_handler.setLevel(logging.ERROR)


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [LOG] %(message)s',
    datefmt='[%H:%M:%S]',
    handlers=[all_messages_handler, error_handler]
)


# Функция для логирования
def log_message(username, user_id, first_name, last_name, command):
    message = f"Пользователь @{username} ({user_id}) ({first_name} {last_name}) использовал команду {command}"
    logging.info(message)


# Функция для логирования ошибок
def log_error(username, user_id, error_message):
    message = f"Ошибка у пользователя @{username} ({user_id}): {error_message}"
    logging.error(message)
