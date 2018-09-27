import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # Check environment variable SECRET_KEY for hash key, or use string
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    # Mail server notification environment variables
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 25)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") is not None
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    DEVBLOG_MAIL_SUBJECT_PREFIX = "[DEVBLOG]"
    DEVBLOG_MAIL_SENDER = "DEVBLOG Admin <devdebugging@gmail.com>"
    DEVBLOG_ADMIN = os.environ.get("DEVBLOG_ADMIN")
    SSL_REDIRECT = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB_HOST = os.environ.get("DEV_MONGODB_HOST") or "localhost"
    MONGODB_DB = os.environ.get("DEV_MONGODB_DATABASE") or 'DEVBLOGDev'
    MONGODB_USER = os.environ.get("DEV_MONGODB_USER")
    MONGODB_PASSWORD = os.environ.get("DEV_MONGODB_PASSWORD")
    MONGODB_PORT = os.environ.get("DEV_MONGODB_PORT") or 27017


class TestingConfig(Config):
    TESTING = True
    MONGODB_HOST = os.environ.get("TEST_MONGODB_HOST") or "localhost"
    MONGODB_DB = os.environ.get("TEST_MONGODB_DATABASE") or 'test'


class ProductionConfig(Config):
    MONGODB_HOST = os.environ.get("REL_MONGODB_HOST") or "localhost"
    MONGODB_DB = os.environ.get("REL_MONGODB_DATABASE") or "DEVBLOGRelease"
    MONGODB_USER = os.environ.get("REL_MONGODB_USER")
    MONGODB_PASSWORD = os.environ.get("REL_MONGODB_PASSWORD")
    MONGODB_PORT = os.environ.get("REL_MONGODB_PORT")

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler

        credentials = None
        secure = None
        if getattr(cls, "MAIL_USERNAME", None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, "MAIL_USE_TLS", None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.DEVBLOG_MAIL_SENDER,
            toaddrs=[cls.DEVBLOG_ADMIN],
            subject=cls.DEVBLOG_MAIL_SUBJECT_PREFIX + " Application Error",
            credentials=credentials,
            secure=secure,
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

class HerokuConfig(ProductionConfig):
    SSL_REDIRECT = True if os.environ.get('DYNO') else False

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # handle reverse proxy server headers
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

class DockerConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to stderr
        import logging
        from logging import StreamHandler

        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "release": ProductionConfig,
    "docker": DockerConfig,
    "heroku": HerokuConfig,
    "default": DevelopmentConfig,
}
