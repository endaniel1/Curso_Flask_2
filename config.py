import os

class Config(object):
	SECRET_KEY = 'Enrique'

class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/flask_2"
	SQLALCHEMY_TRACK_MODIFICATIONS=False