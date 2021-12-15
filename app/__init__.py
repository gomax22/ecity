from flask import Flask, send_from_directory, request, make_response
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from logging.handlers import RotatingFileHandler
import os
import logging
from flask_mail import Mail
from flask_bootstrap import Bootstrap

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')


@app.route('/static/<path:path>')
def send_images(path):
    return send_from_directory('static', path)


@app.route('/templates/<path:path>')
def send_templates(path):
    return send_from_directory('templates', path)

@app.route('/sw.js')
def service_worker():
    return send_from_directory('templates', 'sw.js')


@app.route('/manifest.json')
def manifest():
    return app.send_static_file('manifest.json')


@app.route('/script.js')
def script():
    return app.send_static_file('script.js')



app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)
bootstrap = Bootstrap(app)


if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/ecity.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('E-City startup')

from app import routes, models, errors
