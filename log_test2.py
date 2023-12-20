import logging
import sys

# Создаем форматтер
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Создаем обработчики
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

file_handler = logging.FileHandler('app.log', mode='a')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Создаем логгеры
root_logger = logging.getLogger('firstLogger')
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(console_handler)
root_logger.addHandler(file_handler)

sample_logger = logging.getLogger('secondLogger')
sample_logger.setLevel(logging.DEBUG)
sample_logger.addHandler(console_handler)
sample_logger.addHandler(file_handler)

# Примеры использования логгеров
root_logger.debug('Это сообщение будет залогировано с использованием root логгера')
sample_logger.debug('Это сообщение будет залогировано с использованием sampleLogger логгера')
