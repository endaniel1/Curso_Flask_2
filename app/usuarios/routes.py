from flask import Flask,render_template,request,session,url_for,redirect
from . import users
 
from flask import flash #Aqui para los mensajes 

from models import db
from models import Users
from app import forms

from app import helpers

@users.before_request
def before_request():
	if "username" not in session:
		message="Debe de iniciar Sección Primero!"
		flash(message)
		return redirect(url_for("auth.login"))
	elif session["type"] == "visitor" and request.endpoint in ["usuarios.usuarios","usuarios.create_user","usuarios.edit","usuarios.destroy"]:
		message="Usted No Tine Acceso!"
		flash(message)
		return redirect(url_for("usuarios.home"))

@users.route("/home")
def home():	
	title="Home"
	return render_template("home.html",title=title)	

@users.route("/usuarios/",methods=["GET"])
@users.route("/usuarios/<int:page>",methods=["GET"])
def usuarios(page=1):
	title="Usuarios"
	per_page=3
	users=Users.query.order_by(Users.id).paginate(page,per_page,False)
	return render_template("usuarios/index.html",title=title,users=users)	

@users.route("/usuarios/create",methods=["GET","POST"])
def create_user():
	title="Usuarios Create"
	form_createAdmin=forms.CreateUserAdmin(request.form)

	if request.method == "POST" and form_createAdmin.validate():

		user=Users(form_createAdmin.username.data,
					form_createAdmin.password.data,
					form_createAdmin.email.data,
					form_createAdmin.type.data)

		db.session.add(user)
		db.session.commit()

		success_message="Usuario Registrado Correctamente! "
		flash(success_message)

		return redirect(url_for("usuarios.usuarios"))
	return render_template("usuarios/create.html",title=title,form=form_createAdmin)	

@users.route("/usuarios/<int:id>/destroy",methods=["GET"])
def destroy(id=id):
	user=Users.query.filter_by(id=id).first()

	if user is not None:
		helpers.deleteImagen(user.articles)		
		db.session.delete(user)
		db.session.commit()
		message="Usuario Eliminado!"
	else:
		message="Usuario No Existe!"
		
	flash(message)
	return redirect(url_for("usuarios.usuarios"))


@users.route("/usuarios/<int:id>/edit",methods=["GET","POST"])
def edit(id=id):
	title="Usuario Edit"
	user=Users.query.filter_by(id=id).first()
	form_createAdmin=forms.CreateUserAdmin(request.form)

	if request.method == "POST" and form_createAdmin.validate():

		usernuevo=Users(form_createAdmin.username.data,
					form_createAdmin.password.data,
					form_createAdmin.email.data,
					form_createAdmin.type.data)

		db.session.query(Users).filter(Users.id==id).update({
				"username":usernuevo.username,
				"password":usernuevo.password,
				"email":usernuevo.email,
				"type":usernuevo.type
			}, synchronize_session = False)

		db.session.commit()

		message="Usuario Editado!"

		flash(message)
		return redirect(url_for("usuarios.usuarios"))


	form_createAdmin.type.default=user.type
	form_createAdmin.process()	

	return render_template("usuarios/edit.html",title=title,form=form_createAdmin,user=user)

@users.route("/logout")
def logout():
	if "username" in session:
		session.pop("username","type")

	mensajes="Cierre de Sección Correctamente!"
	flash(mensajes)
	return redirect(url_for("auth.login"))
