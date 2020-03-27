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
	type=db.Column(db.Enum("visitor","admin"),nullable=False,server_default="visitor")
	articles=db.relationship("Articles", backref='users')

	#Aqui iniciamos nuestro construtor para q tenga los datos
	def __init__(self, username, password, email,type):
		self.username=username
		self.password=self.__create_passwoord(password)
		self.email=email
		self.type=type
	#Aqui creamos este metodo para encriptar contraseñña
	def __create_passwoord(self, secret):
		return bcrypt.generate_password_hash(secret)
	#Aqui creamos otro metodo para verificar la contraseña encriptada
	def verify_password(self, secret):
		return bcrypt.check_password_hash(self.password,secret)

class Categories(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(50),nullable=True)
	articles=db.relationship("Articles", backref='categories')

	"""docstring for ClassName"""
	def __init__(self, name):
		self.name=name

class Articles(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	title=db.Column(db.String(50),nullable=True)
	content=db.Column(db.Text())

	user_id=db.Column(db.Integer,db.ForeignKey("users.id",ondelete='CASCADE'),nullable=True)
	category_id=db.Column(db.Integer,db.ForeignKey("categories.id",ondelete='CASCADE'),nullable=True)

	def __init__(self, title, content,user_id,category_id):		
		self.title = title
		self.content = content
		self.user_id = user_id
		self.category_id = category_id
		

		
		
