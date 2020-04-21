from flask import Flask,render_template,request,session,url_for,redirect,send_from_directory
from os.path import dirname,abspath,join

from . import front #Aqui el blueprints 
from flask.views import MethodView

from models import Articles
from models import Users
from models import Categories
from models import Tags


@front.route("/front/",methods=["GET"])
@front.route("/front/<int:page>",methods=["GET"])
def index(page=1):
	title="Home"
	per_page=3
	articles=Articles.query.order_by(Articles.id).join(Users,Categories).add_columns(Users.username,
																					Categories.name).paginate(page,per_page,False)
	categories=Categories.query.order_by(Categories.id).all()
	tags=Tags.query.order_by(Tags.id).all()	

	return render_template("index.html",
							title=title,
							articles=articles,
							categories=categories,
							tags=tags)

@front.route('/<filename>')
def send_file(filename):
	dir_image=dirname(dirname(abspath(__file__)))+"/articulos/templates/images/"
	return send_from_directory(dir_image, filename)

@front.route('/front/article/<slug>')
def viewarticles(slug):	
	article=Articles.query.filter_by(slug=slug).first()
	title="Article {}".format(article.title)

	categories=Categories.query.order_by(Categories.id).all()
	tags=Tags.query.order_by(Tags.id).all()	

	return render_template("article.html",
							article=article,
							title=title,
							categories=categories,
							tags=tags)

class CategoryScope(MethodView):
	def get(self, category,page=1):
		title="Category"
		per_page=3
		category=Categories.query.filter_by(name=category).first()
		articles=category.articles
		articles=articles.join(Categories).add_columns(Categories.name).paginate(page,per_page,False)
		
		categories=Categories.query.order_by(Categories.id).all()
		tags=Tags.query.order_by(Tags.id).all()	

		return render_template('index.html',
								title=title, 
								articles=articles,
								categories=categories,
								tags=tags)

class TagScope(MethodView):
	def get(self, tag,page=1):
		title="Tag"
		per_page=3
		tag=Tags.query.filter_by(name=tag).first()
		articles=tag.articles
		articles=articles.join(Categories).add_columns(Categories.name).paginate(page,per_page,False)
		
		categories=Categories.query.order_by(Categories.id).all()
		tags=Tags.query.order_by(Tags.id).all()	

		return render_template('index.html',
								title=title, 
								articles=articles,
								categories=categories,
								tags=tags)

front.add_url_rule('/front/category/<category>/', view_func=CategoryScope.as_view('category'),methods=['GET'])
front.add_url_rule('/front/category/<category>/<int:page>', view_func=CategoryScope.as_view('categoryScope'),methods=['GET'])

front.add_url_rule('/front/tag/<tag>/', view_func=TagScope.as_view('tag'),methods=['GET'])
front.add_url_rule('/front/tag/<tag>/<int:page>', view_func=TagScope.as_view('tagScope'),methods=['GET'])