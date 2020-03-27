from app import create_app
from flask_wtf import CsrfProtect 
from models import db

app = create_app()
csrf=CsrfProtect()

if __name__ == '__main__':

	db.init_app(app)#Aqui iniciamos nuestra base de datos
	with app.app_context():#Aqui vemos si tenemos las tablas
		db.create_all()#Aqui con la clase create_all() creamos nuestras tablas

	csrf.init_app(app)
	app.run(debug=True,port= '8080')