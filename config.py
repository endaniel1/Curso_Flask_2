import os

class Config(object):
	pass

class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/flask_2"
	SQLALCHEMY_TRACK_MODIFICATIONS=False