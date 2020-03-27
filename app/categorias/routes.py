from flask import Flask,render_template,request,session,url_for,redirect

from . import category #Aqui el blueprints 

from flask import flash #Aqui para los mensajes 

from models import db
from models import Categories
from app import forms


@category.before_request
def before_request():
	if "username" not in session:
		message="Debe de iniciar Sección Primero!"
		flash(message)
		return redirect(url_for("auth.login"))


@category.route("/categorias/",methods=["GET"])
@category.route("/categorias/<int:page>",methods=["GET"])
def categorias(page=1):
	title="Categorias"
	per_page=3
	categories=Categories.query.order_by(Categories.id).paginate(page,per_page,False)

	return render_template("categorias/index.html",title=title,categories=categories)

@category.route("/categorias/create",methods=["GET","POST"])
def create_category():
	title="Categorias Create"
	form_category=forms.CreateCategory(request.form)

	if request.method == "POST" and form_category.validate():

		category=Categories(form_category.name.data)

		db.session.add(category)
		db.session.commit()

		success_message="Categoria Registrada Correctamente! "
		flash(success_message)

		return redirect(url_for("categorias.categorias"))
	return render_template("categorias/create.html",title=title,form=form_category)	


@category.route("/categorias/<int:id>/destroy",methods=["GET"])
def destroy(id=id):
	category=Categories.query.filter_by(id=id).first()

	if category is not None:
		db.session.delete(category)
		db.session.commit()
		message="Categoria Eliminada!"
	else:
		message="Categoria No Existe!"
		
	flash(message)
	return redirect(url_for("categorias.categorias"))

@category.route("/categorias/<int:id>/edit",methods=["GET","POST"])
def edit(id=id):
	title="Categoria Edit"
	category=Categories.query.filter_by(id=id).first()
	form_category=forms.CreateCategory(request.form)

	if request.method == "POST" and form_category.validate():

		categorynuevo=Categories(form_category.name.data)

		db.session.query(Categories).filter(Categories.id==id).update({
				"name":categorynuevo.name
			}, synchronize_session = False)

		db.session.commit()

		message="Categoria Editada!"

		flash(message)
		return redirect(url_for("categorias.categorias"))
	

	return render_template("categorias/edit.html",title=title,form=form_category,category=category)
