import logging
import colorlog
import os
import functools
from logging.handlers import RotatingFileHandler

from colorlog import ColoredFormatter


class newsLogger():
    def __init__(self):
        """
        Инициализация логгера
        """

        # Создание папки logs
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
        log_dir = os.path.abspath(log_dir)
        os.makedirs(log_dir, exist_ok=True)

        # Создание логгера
        self.logger = logging.getLogger('NewsAggregator')
        self.logger.setLevel(logging.DEBUG)

        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Определение формата логгера
        console_formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s - %(name)s - %(levelname)-8s - %(module)s:%(lineno)d - %(message)s%(reset)s',
            reset=True,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red'
            },
        )
        # Создание основного обработчика
        main_log_path = os.path.join(log_dir, 'app.log')
        file_handler = RotatingFileHandler(
            main_log_path,
            maxBytes=1000000,
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)

        # Создание обработчика для консоли
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)

        # Добавление всех обработчиков к логгеру
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        """Возвращает настроенный логгер"""
        return self.logger


def log_exceptions(func):
    """
    Декоратор для автоматического логирования исключений
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(
                f"Ошибка в {func.__module__}.{func.__name__}: {str(e)}",
                exc_info=True
            )
            raise

    return wrapper


# Создание глобального экземпляра класса
news_logger = newsLogger()
logger = news_logger.get_logger()




