from flask import Flask,render_template,request,session,url_for,redirect
from . import auth
from app import forms

from flask import flash #Aqui para los mensajes 

from models import db
from models import Users

@auth.route('/login',methods=["GET","POST"])
def login():
	title="Login"
	form_login=forms.LoginForm(request.form)

	if request.method == "POST" and form_login.validate():
		username=form_login.username.data 
		password=form_login.password.data 

		user=Users.query.filter_by(username=username).first()

		if user is not None and user.verify_password(password):	
			session["id"]=user.id
			session["username"]=user.username
			session["type"]=user.type
			success_message="Inicio de Sección Correctamente!"
			flash(success_message)
			return redirect(url_for("usuarios.home"))
		else:
			error_message="Usuario Ó Contraseña No Valida!"
			flash(error_message)

	return render_template("auth/login.html",title=title,form=form_login)

@auth.route("/register",methods=["POST","GET"])
def register():
	title="Registre User"
	form_create=forms.CreateUser(request.form)

	if request.method == "POST" and form_create.validate():
		
		user=Users(form_create.username.data,
				form_create.password.data,
				form_create.email.data,"visitor")

		db.session.add(user)
		db.session.commit()

		success_message="Usuario Registrado Correctamente! "
		flash(success_message)
		
		session["username"]=user.username
		session["type"]=user.type
		return redirect(url_for("usuarios.home"))

	return render_template("auth/register.html",title=title,form=form_create)

