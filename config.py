import redis,datetime

class Config(object):
    SECRET_KEY = "dafjdskdfja89a8*(0()&*&^&"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:mysql@127.0.0.1/flaskIhome"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    #flalsk session
    SESSION_TYPE = "redis"
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT,db=1)
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=2)


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    pass


config_map = {
    "develop": DevelopmentConfig,
    "product": ProductionConfig
}