import sqlalchemy
from flask import Flask, render_template
from config import config
from flask_sqlalchemy import SQLAlchemy

from News.app.app_logging.logger import logger, log_exceptions

db = SQLAlchemy()

def createApp():
    """
        Фабричная функция для создания и настройки Flask приложения.
    """
    logger.info("Начало инициализации Flask приложения")

    app = Flask(__name__)
    app.config.from_object(config)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    try:
        db.init_app(app)
        logger.info("База данных успешно инициализирована")
    except Exception as e:
        logger.error(f"Ошибка инициализации БД: {e}", exc_info=True)
        raise

    try:
        from routes import bp
        app.register_blueprint(bp)
        logger.info("Blueprints успешно зарегистрированы")
    except Exception as e:
        logger.error(f"Ошибка регистрации blueprints: {e}", exc_info=True)
        raise

    logger.info("Flask приложение успешно создано")
    return app