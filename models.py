from flask_sqlalchemy import SQLAlchemy

import datetime

from flask_bcrypt import Bcrypt

db=SQLAlchemy()#Aqui creamos una instancia de la clase SQLAlchemy
bcrypt = Bcrypt()#Aqui creamos una instancia para encriptar cosan con bcrypt

class Users(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String(50),nullable=True)
	password=db.Column(db.String(80),nullable=True)
	email=db.Column(db.String(50),unique=True,nullable=True)
	#Aqui iniciamos nuestro construtor para q tenga los datos
	def __init__(self, username, password, email):
		self.username=username
		self.password=self.__create_passwoord(password)
		self.email=email
	#Aqui creamos este metodo para encriptar contraseñña
	def __create_passwoord(self, secret):
		return bcrypt.generate_password_hash(secret)
	#Aqui creamos otro metodo para verificar la contraseña encriptada
	def verify_password(self, secret):
		return bcrypt.check_password_hash(self.password,secret)

