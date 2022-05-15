import os

class Config:
    SECRET_KEY = 'hithere'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:Gmwangi@localhost/beautiful_musings'


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig
}