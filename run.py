from app import create_app
from flask_wtf import CsrfProtect 
from models import db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager,Server

app = create_app()
csrf=CsrfProtect()
migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command("runserver", Server(port=8080))

if __name__ == '__main__':

	db.init_app(app)#Aqui iniciamos nuestra base de datos
	with app.app_context():#Aqui vemos si tenemos las tablas
		db.create_all()#Aqui con la clase create_all() creamos nuestras tablas
	
	csrf.init_app(app)
	manager.run()