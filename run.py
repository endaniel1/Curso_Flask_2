from app import create_app
from flask_wtf import CsrfProtect 
from models import db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager,Server

app = create_app()
csrf=CsrfProtect()
migrate = Migrate(app,db)#Aqui para las migraciones
manager = Manager(app)#Aqui para q tenga los comando
manager.add_command('db', MigrateCommand)#Añadimos aqui el comando db
manager.add_command("runserver", Server(port=8080))#Añadimos aqui el comando runserver

if __name__ == '__main__':

	db.init_app(app)#Aqui iniciamos nuestra base de datos
	with app.app_context():#Aqui vemos si tenemos las tablas
		db.create_all()#Aqui con la clase create_all() creamos nuestras tablas
	
	csrf.init_app(app)
	manager.run()#Aqui de esta manera iniciamos la aplicacion