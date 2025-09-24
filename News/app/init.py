from flask import Flask, render_template
from config import config

def createApp():
    """
        Фабричная функция для создания и настройки Flask приложения.

        Этот подход позволяет создавать несколько экземпляров приложения
        с разными конфигурациями (например, для тестирования).

        Returns:
            Flask: Настроенный экземпляр Flask приложения

        Steps:
            1. Создает экземпляр Flask приложения
            2. Загружает конфигурацию из класса config
            3. Регистрирует blueprint'ы (модули маршрутов)
            4. Возвращает готовое приложение
        """
    app = Flask(__name__)
    app.config.from_object(config)
    from routes import bp
    app.register_blueprint(bp)

    return app


