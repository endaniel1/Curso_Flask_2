from wtforms import Form 
from wtforms import StringField,TextField,PasswordField,validators
from wtforms.fields.html5 import EmailField


class LoginForm(Form):
	username = StringField("Nombre de Usuario",[
					validators.Required(message="El Username Es Requerido!."),
					validators.length(min=4,max=25,message="Ingrese Un Username Valido!.")
				])
	password=PasswordField("Contraseña",[
				validators.Required(message="El Password Es Requerido!.")
			])

class CreateUser(Form):
	username = StringField("Nombre de Usuario",[
					validators.Required(message="El Username Es Requerido!."),
					validators.length(min=4,max=25,message="Ingrese Un Username Valido!.")
				])
	email =	EmailField("Correo electronico",[
				validators.Required(message="El Email Es Requerido!."),
				validators.Email(message="Ingrese Un Email Valido")
			])
	password=PasswordField("Contraseña",[
				validators.Required(message="El Password Es Requerido!.")
			])
		