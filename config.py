# config.py

class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments

class DevelopmentConfig(Config):
    """
    Development configurations
    """

    FLASK_DEBUG = True
    

class ProductionConfig(Config):
    """
    Production configurations
    """

    FLASK_DEBUG = False

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
