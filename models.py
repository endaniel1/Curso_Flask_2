from flask_sqlalchemy import SQLAlchemy

import datetime

from flask_bcrypt import Bcrypt

db=SQLAlchemy()#Aqui creamos una instancia de la clase SQLAlchemy
bcrypt = Bcrypt()#Aqui creamos una instancia para encriptar cosan con bcrypt

class Posts(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	title=db.Column(db.String(50))


