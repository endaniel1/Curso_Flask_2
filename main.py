from flask import Flask,render_template,request,session,url_for,redirect
from flask import flash #Aqui para los mensajes 

from config import DevelopmentConfig #Aqui importamos este archivo con esta clase para hacer las configuraciones para nuestrso servidor
from models import db #Aqui importamos nuestra conexion

from models import Users

from flask_wtf import CsrfProtect 

import forms #Aqui para los formularios

app = Flask(__name__)

app.config.from_object(DevelopmentConfig)

csrf=CsrfProtect()

@app.before_request
def before_request():
	if "username" not in session and request.endpoint in ["home","logout"]:
		error_message="Debe de iniciar Sección Primero!"
		flash(error_message)
		return redirect(url_for("login"))
	elif "username" in session and request.endpoint in ["login","register"]:
		error_message="Usted no Tiene acceso!"
		flash(error_message)
		return redirect(url_for("home"))

@app.route('/')
def index():
	title="Home"
	return render_template("index.html",title=title)

@app.route('/login',methods=["GET","POST"])
def login():
	title="Login"
	form_login=forms.LoginForm(request.form)

	if request.method == "POST" and form_login.validate():
		username=form_login.username.data 
		password=form_login.password.data 

		user=Users.query.filter_by(username=username).first()

		if user is not None and user.verify_password(password):	
			session["username"]=user.username
			success_message="Inicio de Sección Correctamente!"
			flash(success_message)
			return redirect(url_for("home"))
		else:
			error_message="Usuario Ó Contraseña No Valida!"
			flash(error_message)

	return render_template("login.html",title=title,form=form_login)

@app.route("/register",methods=["POST","GET"])
def register():
	title="Registre User"
	form_create=forms.CreateUser(request.form)

	if request.method == "POST" and form_create.validate():

		user=Users(form_create.username.data,
				form_create.password.data,
				form_create.email.data)

		db.session.add(user)
		db.session.commit()

		success_message="Usuario Registrado Correctamente! "
		flash(success_message)
		
		session["username"]=user.username
		return redirect(url_for("home"))

	return render_template("register.html",title=title,form=form_create)

@app.route("/home")
def home():
	title="Home"
	return render_template("home.html",title=title)	

@app.route("/logout")
def logout():
	if "username" in session:
		session.pop("username")

	mensajes="Cierre de Sección Correctamente!"
	flash(mensajes)
	return redirect(url_for("login"))

@app.route("/usuarios/")
def usuarios():
	title="Usuarios"
	return render_template("usuarios/index.html",title=title)	

@app.route("/usuarios/create")
def create_user():
	title="Usuarios Create"
	return 'render_template("usuarios/create.html",title=title)'	

if __name__ == '__main__':
	db.init_app(app)#Aqui iniciamos nuestra base de datos
	csrf.init_app(app)
	with app.app_context():#Aqui vemos si tenemos las tablas
		db.create_all()#Aqui con la clase create_all() creamos nuestras tablas

	app.run(debug=True,port= '8080')