from flask import Flask,render_template,request,session,url_for,redirect

from . import article #Aqui el blueprints 

from flask import flash #Aqui para los mensajes 

from models import db
from models import Articles
from models import Users
from models import Categories
from app import forms

@article.route("/articulos/",methods=["GET"])
@article.route("/articulos/<int:page>",methods=["GET"])
def articulos(page=1):
	title="Articulos"
	per_page=3
	articles=Articles.query.join(Users).join(Categories).add_columns(Users.username,
																	Categories.name,
																	Articles.title,
																	Articles.content).paginate(page,per_page,False)

	return render_template("articles/index.html",title=title,articles=articles)


@article.route("/articulos/create",methods=["GET","POST"])
def create_article():
	title="Articulos Create"
	form_article=forms.CreateArticle(request.form)
	#Aqui le envios las categoria a mi select	
	form_article.category.choices = [(category.id, category.name) for category in Categories.query.all()]

	#print(form_article.category.data)
	if request.method == "POST" and form_article.validate():

		"""article=Articles(form_article.name.data)

		db.session.add(article)
		db.session.commit()
		"""
		success_message="Articulo Registrada Correctamente! "
		flash(success_message)

		return redirect(url_for("categorias.categorias"))
	
	
	return render_template("articles/create.html",title=title,form=form_article)	
