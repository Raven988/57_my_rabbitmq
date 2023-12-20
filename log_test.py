import logging
import logging.config

logging.config.fileConfig('log_conf.ini')

# Выбираем логгер root
# root_logger = logging.getLogger('root')
# root_logger.debug('Это сообщение будет залогировано с использованием root логгера')

# Выбираем логгер sampleLogger
sample_logger = logging.getLogger('sampleLogger')
sample_logger.debug('Это сообщение будет залогировано с использованием sampleLogger логгера')
