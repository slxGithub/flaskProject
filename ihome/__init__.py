import redis
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from config import config_map
from ihome import api_1_0

db = SQLAlchemy()
redis_store = None


def create_app(config_name="develop"):
    """
    创建flask应用对象
    :param config_name:
    :return:
    """
    app = Flask(__name__)

    config_class = config_map.get(config_name)
    app.config.from_object(config_class)

    # 初始化db
    db.init_app(app)

    Session(app)
    CSRFProtect(app)

    # 初始化redis
    global redis_store
    redis_store = redis.StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT)

    # 注册蓝图
    app.register_blueprint(api_1_0.api, url_prefix='/api/v1.0')
    return app
