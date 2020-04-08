import os
from werkzeug.utils import secure_filename

from flask import Flask,render_template,request,session,url_for,redirect

from . import article #Aqui el blueprints 

from flask import flash #Aqui para los mensajes 

from models import db
from models import Articles
from models import Users
from models import Categories
from models import Tags
from models import Images
from app import forms

from werkzeug.datastructures import CombinedMultiDict
from run import app
import datetime

@article.route("/articulos/",methods=["GET"])
@article.route("/articulos/<int:page>",methods=["GET"])
def articulos(page=1):
	title="Articulos"
	per_page=3
	articles=Articles.query.join(Users).join(Categories).add_columns(Users.username,
																	Categories.name,
																	Articles.title,
																	Articles.content,
																	Articles.id).paginate(page,per_page,False)

	return render_template("articles/index.html",title=title,articles=articles)


@article.route("/articulos/create",methods=["GET","POST"])
def create_article():
	title="Articulos Create"
	form_article=forms.CreateArticleImagen(CombinedMultiDict((request.files, request.form)))

	#Aqui le envios las categoria y tag a mi select	
	form_article.category.choices = [(category.id, category.name) for category in Categories.query.all()]
	form_article.tag.choices = [(tag.id, tag.name) for tag in Tags.query.all()]
		
	if request.method == "POST" and form_article.validate():
		user_id=session["id"]		
		
		article=Articles(form_article.title.data,
							form_article.content.data,
							user_id,
							form_article.category.data)

		db.session.add(article)#Creamos nuestro articulo
		#Aqui lo asocioamos a nuestros tags
		for tag in form_article.tag.data:
			article.tag_id.append(Tags.query.get(tag))
		#Aqui  guardamos y creamos nuestra imagenes de nuestro articulo
		for imagen in form_article.image.data:
			time = datetime.datetime.today()#Obtenemos la fecha y hora 
			hora = "{}-{}-{}-{}".format(time.hour,
										time.minute,
										time.second,
										time.microsecond)#Formatemos la hora
			file=imagen #Guardmos nuestra imagen
			#Aqui creamos el nombre de la imagen nueva
			image_name = "ImagenFlask_{}_{}.{}".format(datetime.date.today(),hora,
														file.filename.split(".")[1])

			#Aqui creamos la ruta en donde va a estar la imagen y la guardarmos posteriormente 
			images_dir = os.path.dirname(os.path.abspath(__file__))+"/templates/images"
			os.makedirs(images_dir, exist_ok=True)
			file_path = os.path.join(images_dir, image_name)
			file.save(file_path)
			#Creamos Aqui nuestra imagen para guardarla en la base de datos
			image=Images(image_name,article.id)
			db.session.add(image)
		
		db.session.commit()
		success_message="Articulo Registrada Correctamente! "
		flash(success_message)

		return redirect(url_for("articulos.articulos"))
	
	
	return render_template("articles/create.html",title=title,form=form_article)	



@article.route("/articulos/<int:id>/destroy",methods=["GET"])
def destroy(id=id):
	article=Articles.query.filter_by(id=id).first()	
	
	if article is not None:
		images=article.images
		db.session.delete(article)
		#Directorio en donde se encuentra sus imagenes		
		dir_imagenes=os.path.dirname(os.path.abspath(__file__))+"/templates/images/"
		#Aqui las buscamos y la eliminamos
		for image in images:
			#Aqui eliminamos las imagenes
			os.remove("{}{}".format(dir_imagenes,image.name))
			
		db.session.commit()#Guardamos los cambio q hacemos en nuestra base de datos
		message="Articulo Eliminado!"
	else:
		message="Articulo No Existe!"

	flash(message)
	return redirect(url_for("articulos.articulos"))

@article.route("/articulos/<int:id>/edit",methods=["GET","POST"])
def edit(id=id):
	title="Articulos Edit"
	article=Articles.query.filter(Articles.id==id).first()
	form_article=forms.CreateArticleAdmin(request.form)
	#Aqui le envios las categoria y tag a mi select	
	form_article.category.choices = [(category.id, category.name) for category in Categories.query.all()]
	form_article.tag.choices = [(tag.id, tag.name) for tag in Tags.query.all()]
	
	if request.method == "POST" and form_article.validate():
		
		db.session.query(Articles).filter(Articles.id==id).update({
				"title":form_article.title.data,
				"content":form_article.content.data,
				"category_id":form_article.category.data
			}, synchronize_session = False)
		

		article.tag_id.clear()		

		for tag in form_article.tag.data:
			article.tag_id.append(Tags.query.get(tag))
	
		db.session.commit()
		
		message="Articulo Editado!"

		flash(message)
		return redirect(url_for("articulos.articulos"))
	
	#Aqui añado las cartegoria y los tags
	form_article.category.default=article.category_id
	form_article.content.default=article.content
	form_article.tag.default=[(tag.id) for tag in article.tag_id]
	form_article.process()

	return render_template("articles/edit.html",title=title,form=form_article,article=article)
