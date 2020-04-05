from flask import Flask,render_template,request,session,url_for,redirect
from . import tags
 
from flask import flash #Aqui para los mensajes 

from models import db
from models import Tags
from app import forms

@tags.route("/tags/create",methods=["GET","POST"])
def create_category():
	title="Tag Create"
	form_tag=forms.CreateTag(request.form)

	if request.method == "POST" and form_tag.validate():

		tag=Tags(form_tag.name.data)

		db.session.add(tag)
		db.session.commit()

		success_message="Tag Registrado Correctamente! "
		flash(success_message)

		return redirect(url_for("tags.tags"))
	return render_template("tags/create.html",title=title,form=form_tag)


@tags.route("/tags/<int:id>/destroy",methods=["GET"])
def destroy(id=id):
	tag=Tags.query.filter_by(id=id).first()

	if tag is not None:
		db.session.delete(tag)
		db.session.commit()
		message="Tag Eliminado!"
	else:
		message="Tag No Existe!"
		
	flash(message)
	return redirect(url_for("tags.tags"))

@tags.route("/tags/<int:id>/edit",methods=["GET","POST"])
def edit(id=id):
	title="Tag Edit"
	tag=Tags.query.filter_by(id=id).first()
	form_tag=forms.CreateTag(request.form)

	if request.method == "POST" and form_tag.validate():		

		db.session.query(Tags).filter(Tags.id==id).update({
				"name":form_tag.name.data
			}, synchronize_session = False)

		db.session.commit()

		message="Tag Editado!"

		flash(message)
		return redirect(url_for("tags.tags"))
	

	return render_template("tags/edit.html",title=title,form=form_tag,tag=tag)

@tags.route("/tags/",methods=["GET"])
@tags.route("/tags/<int:page>",methods=["GET"])
def tags(page=1):
	title="Tag"
	per_page=3
	tags=Tags.query.order_by(Tags.id).paginate(page,per_page,False)

	return render_template("tags/index.html",title=title,tags=tags)


