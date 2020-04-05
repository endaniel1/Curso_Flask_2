from wtforms import Form 
from wtforms import StringField,TextField,PasswordField,validators,TextAreaField
from wtforms import SelectMultipleField,SelectField,MultipleFileField
from wtforms.fields.html5 import EmailField
from flask_wtf.file import FileField,FileAllowed

from models import Categories

class LoginForm(Form):
	username = StringField("Nombre de Usuario",[
					validators.Required(message="El Username Es Requerido!."),
					validators.length(min=3,max=25,message="Ingrese Un Username Valido!.")
				])
	password=PasswordField("Contraseña",[
				validators.Required(message="El Password Es Requerido!.")
			])

class CreateUser(Form):
	username = StringField("Nombre de Usuario",[
					validators.Required(message="El Username Es Requerido!."),
					validators.length(min=3,max=25,message="Ingrese Un Username Valido!.")
				])
	email =	EmailField("Correo electronico",[
				validators.Required(message="El Email Es Requerido!."),
				validators.Email(message="Ingrese Un Email Valido!.")
			])
	password = PasswordField("Contraseña",[
				validators.Required(message="El Password Es Requerido!."),
				validators.length(min=3,max=25,message="Ingrese Una Password Valido!.")
			])	

class CreateUserAdmin(CreateUser):

	type = SelectField("Tipo", choices=[('visitor', 'Visitate'),("admin","Administrador")],validators=[validators.Required(message=('El Type Es Requerido!.'))])
	
class CreateCategory(Form):
	name = StringField("Nombre de Categoria",[
			validators.Required(message="El Name Es Requerido!."),
			validators.length(min=3,max=25,message="Ingrese Un Name Valido!.")
		])

class CreateArticle(Form):
	title =	StringField("Titulo",[
			validators.Required(message="El Title Es Requerido!."),
			validators.length(min=3,max=25,message="Ingrese Un Title Valido!.")
		])
	content = TextAreaField("Contenido",[
				validators.length(min=3,message="Ingrese Un content Más Largo!.")
			])

	#Aqui las categoria en un select	
	category = SelectField("Tipo",choices=[],coerce=int)
	#Aqui los Tags en un select	
	tag = SelectMultipleField("Tipo",choices=[],coerce=int)

	image = MultipleFileField('Imagen', validators=[
		FileAllowed(['jpg', 'png'], 'Solo se permiten imágenes')
    ])
class CreateTag(Form):
	name = StringField("Nombre de Tag",[
			validators.Required(message="El Name Es Requerido!."),
			validators.length(min=3,max=25,message="Ingrese Un Name Valido!.")
		])
		
