from flask import Flask,render_template,request,session,url_for,redirect
from config import DevelopmentConfig
from flask import flash #Aqui para los mensajes 

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    @app.before_request
    def before_request():

    	"""if "username" not in session and request.endpoint in ["usuarios.home","usuarios.logout"]:
    		error_message="Debe de iniciar Sección Primero!"
    		flash(error_message)
    		return redirect(url_for("auth.login"))
    	el"""
    	if "username" in session and request.endpoint in ["auth.login","auth.register"]:
    		error_message="Usted no Tiene acceso!"
    		flash(error_message)
    		return redirect(url_for("usuarios.home"))

    @app.route("/")
    def index():
    	title="Home"
    	return render_template("index.html",title=title)

    # Configuracion de los BluePrints
	# BluePrints usuarios
    from .usuarios import users as users
    app.register_blueprint(users)

    # BluePrints auth
    from .auth import auth as auth
    app.register_blueprint(auth)

    # BluePrints category
    from .categorias import category as category
    app.register_blueprint(category)

    # BluePrints article
    from .articulos import article as article
    app.register_blueprint(article)

    # BluePrints tag
    from .tags import tags as tags
    app.register_blueprint(tags)


    return app