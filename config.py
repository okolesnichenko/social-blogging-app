import os
'''
Приложения часто нуждаются во множестве параметров настройки.
Отличным примером этого могут служить разные настройки базы
данных для этапов разработки, тестирования и эксплуатации, чтобы
исключить возможность взаимовлияния.

(venv) $ export MAIL_USERNAME=<Gmail username>
'''


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_SLOW_QUERY_TIME = 0.5
    SQLALCHEMY_RECORD_QUERIES = True
    FLASKY_DB_QUERY_TIMEOUT = 0.5
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@ex.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') or 'appleid292@gmail.com'
    FLASKY_POSTS_PER_PAGE = 15
    FLASKY_FOLLOWERS_PER_PAGE = 10
    FLASKY_COMMENTS_PER_PAGE = 10
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'appleid292@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') 
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'postgresql://oleg:test123@localhost:5433/flaskdb'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'postgresql://oleg:test123@localhost:5433/flasktest'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.FLASKY_MAIL_SENDER,
            toaddrs=[cls.FLASKY_ADMIN],
            subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production':ProductionConfig,
    'default': DevelopmentConfig
}