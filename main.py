from flask import Flask,render_template

from config import DevelopmentConfig #Aqui importamos este archivo con esta clase para hacer las configuraciones para nuestrso servidor
from models import db #Aqui importamos nuestra conexion

app = Flask(__name__)

app.config.from_object(DevelopmentConfig)

@app.route('/')
def index():
	title="Home"
	return render_template("index.html",title=title)


if __name__ == '__main__':
	db.init_app(app)#Aqui iniciamos nuestra base de datos
	with app.app_context():#Aqui vemos si tenemos las tablas
		db.create_all()#Aqui con la clase create_all() creamos nuestras tablas

	app.run(debug=True,port= '8080')