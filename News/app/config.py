from News.app.app_logging.logger import logger, log_exceptions


class config:
    """
    Конфигурационный класс для Flask приложения.
    """

    # Секретный ключ для подписи сессий и токенов
    SECRET_KEY = 'secret'

    # Режим отладки
    # В продакшене должен быть установлен в False
    DEBUG = True

    @classmethod
    @log_exceptions
    def validate_config(cls):
        """
        Проверка конфигурации приложения
        """
        logger.info("Проверка конфигурации приложения ")

        if not cls.SECRET_KEY or cls.SECRET_KEY == 'secret':
            logger.warning("Используется стандартный SECRET_KEY")

        if cls.DEBUG:
            logger.info("Приложение запущено в режиме DEBUG")
        else:
            logger.info("Приложение запущено в продакшене")

        logger.info("Конфигурация проверена успешно")


config.validate_config()