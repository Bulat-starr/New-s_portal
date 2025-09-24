from flask import Flask, render_template
from config import config

def createApp():
    app = Flask(__name__)
    app.config.from_object(config)
    from routes import bp
    app.register_blueprint(bp)

    return app


