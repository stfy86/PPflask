""" Modulo que contiene todos los formularios usados en el sistema """

from wtforms.fields import HiddenField
from wtforms import Form, TextField, FileField, PasswordField, \
     validators, IntegerField, SelectField, SubmitField, DateTimeField, RadioField
#------------------------------------------------------------------------------#
# FORMS
#------------------------------------------------------------------------------#

# Ingreso al Sistema

class LoginForm(Form):
    """ Formulario de logueo """
    username = TextField('Nick', [validators.required(), validators.Length(min=1, max=10)])
    password = PasswordField('Password', [validators.required(), validators.Length(min=1, max=15)])


# Administrar Usuarios

class CreateFormUser(Form):
    """ Formulario para crear un usuario con validaciones"""
    name = TextField('Name', [validators.required(message=":name?:"), validators.Length(min=1, max=15, message=":longitud requerida [1-15]:")])
    password = PasswordField('Password', [validators.required(message=":password?:"), validators.Length(min=1, max=15, message=":longitud requerida [1-15]:")])
    confirmacion = PasswordField('Confirmacion', [validators.EqualTo('password')])
    nombre = TextField('Nombre', [validators.required(message=":nombre?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    apellido = TextField('Apellido', [validators.required(message=":apellido?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    email = TextField('Email', [validators.required(message=":email?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    telefono = IntegerField('Telefono', [validators.required(message=":telefono?:"), validators.NumberRange(min=None, max=None, message=":telefono?:")])
    obs = TextField('Obs', [validators.required(message=":obs?:"), validators.Length(min=1, max=150, message=":longitud requerida [1-150]:")])

class ShowFormUser(Form):
    """ Formulario para mostrar datos de un usuario """
    name = TextField('Name')
    nombre = TextField('Nombre')
    apellido = TextField('Apellido')
    email = TextField('Email')
    telefono = IntegerField('Telefono')
    obs = TextField('Obs')
    estado = TextField('Estado')

# Administrar Proyecto

class CreateFormProject(Form):
    """ Formulario para crear proyecto"""
    nombre = TextField('Nombre', [validators.required( message=":nombre?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    descripcion = TextField('Descripcion', [validators.required(message=":descripcion?:"), validators.Length(min=1, max=150, message=":longitud requerida [1-150]:")])
    presupuesto = IntegerField('Presupuesto', [validators.required(message=":presupuesto?:"), validators.NumberRange(min=1, max=None, message=":presupuesto?:")])

class EditFormProject(Form):
    """ Formulario para editar datos del proyecto """
    descripcion = TextField('Descripcion', [validators.required(message=":descripcion?:"), validators.Length(min=1, max=150, message=":longitud requerida [1-150]:")])
    presupuesto = IntegerField('Presupuesto', [validators.required(message=":presupuesto?:"), validators.NumberRange(min=1, max=None, message=":presupuesto?:")])


class ShowFormProject(Form):
    """ Formulario para mostrar un proyecto"""
    nombre = TextField('Nombre')
    descripcion = TextField('Descripcion')
    fechaDeCreacion = DateTimeField('FechaDeCreacion')
    estado = TextField('Estado')
    presupuesto = IntegerField('Presupuesto')
    
class CreateFormRolProyecto(Form):
    """ Formulario para crear un rol por proyecto"""
    nombre = TextField('Nombre', [validators.required(message=":nombre?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    ambito = TextField('Ambito', [validators.required(message=":ambito?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    descripcion = TextField('Descripcion', [validators.required(message=":descripcion?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
   
class ShowFormRolProyecto(Form):
    """ Formulario para mostrar un rol """
    nombre = TextField('Nombre')
    ambito = TextField('Ambito')
    descripcion = TextField('Descripcion')

class ShowFormUserProyecto(Form):
    """ Formulario para mostrar un usuario de proyecto """
    name = TextField('Name')
    nombre = TextField('Nombre')
    apellido = TextField('Apellido')
    email = TextField('Email')
    telefono = IntegerField('Telefono')
    obs = TextField('Obs')
    estado = TextField('Estado')
    rolNombre = TextField('Rol')

class ShowFormUserComite(Form):
    """ Formulario para mostrar un usuario del comite de proyecto """
    name = TextField('Name')
    nombre = TextField('Nombre')
    apellido = TextField('Apellido')
    email = TextField('Email')
    telefono = IntegerField('Telefono')
    obs = TextField('Obs')
    estado = TextField('Estado')
    comiteNombre = TextField('Comite')
    
# Administrar Fase

class CreateFormFase(Form):
    """ Formulario para crear fase"""
    nombre = TextField('Nombre', [validators.required( message=":nombre?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    descripcion = TextField('Descripcion', [validators.required(message=":descripcion?:"), validators.Length(min=1, max=150, message=":longitud requerida [1-150]:")])

class EditFormFase(Form):
    """ Formulario para editar fase """
    descripcion = TextField('Descripcion', [validators.required(message=":descripcion?:"), validators.Length(min=1, max=150, message=":longitud requerida [1-150]:")])
   
class ShowFormFase(Form):
    """ Formulario para mostrar una fase """
    nombre = TextField('Nombre')
    descripcion = TextField('Descripcion')
    fechaDeCreacion = DateTimeField('FechaDeCreacion')
    orden = IntegerField('Orden')
    estado = TextField('Estado')
    proyectoId = IntegerField('ProyectoId')
    tipoDeItemId = IntegerField('TipoDeItemId')

# Administrar tipo de atributos

class CreateFormAtrib(Form):
    """ Formulario para crear un atributo"""
    nombre = TextField('Nombre', [validators.required(message=":nombre?:"),validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    descripcion = TextField('Descripcion', [validators.required(message=":descripcion?:"), validators.Length(min=1, max=150, message=":longitud requerida [1-150]:")])
    
    
class ShowFormAtrib(Form):
    """ Formulario para mostrar un atributo"""
    nombre = TextField('Nombre')
    tipoDeDato = TextField('Tipo De Dato')
    submit = SubmitField("POST")
    filename = TextField('Nombre de Archivo')
    detalle = IntegerField('Detalle')
    descripcion = TextField('Descripcion')

class EditFormAtrib(Form):
    """ Formulario para editar un atributo"""
    nombre = TextField('Nombre')
    filename = TextField('Nombre de Archivo')
    detalle = IntegerField('Detalle')
    descripcion = TextField('Descripcion')


# Administrar tipo de item

class CreateFormTipoDeItem(Form):
    """ Formulario para crear tipo de item"""
    nombre = TextField('Nombre', [validators.required(message=":nombre?:"),validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    descripcion = TextField('Descripcion', [validators.required(message=":descripcion?:"), validators.Length(min=1, max=150, message=":longitud requerida [1-150]:")])
   
# Administrar item
    
class CreateFormItem(Form):
    """ Formulario para crear un item"""
    nombre = TextField('Nombre', [validators.required(message=":nombre?:"),validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    tipoDeItem = TextField('TipoDeItem')
    version = IntegerField('Version')
    complejidad = IntegerField('Complejidad', [validators.required(message=":complejidad?:"), validators.NumberRange(min=1, max=100, message=":complejidad?:")])
    costo = IntegerField('Costo', [validators.required(message=":costo?:"), validators.NumberRange(min=1, max=100, message=":costo?:")])
        
class ShowFormItem(Form):
    """ Formulario para crear un item"""
    nombre = TextField('Nombre', [validators.required(message=":nombre?:"),validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    version = IntegerField('Version', [validators.required(message=":version?:"), validators.NumberRange(min=None, max=None, message=":version?:")])
    complejidad = IntegerField('Complejidad', [validators.required(message=":complejidad?:"), validators.NumberRange(min=None, max=None, message=":complejidad?:")])
    costo = IntegerField('Costo', [validators.required(message=":costo?:"), validators.NumberRange(min=None, max=None, message=":costo?:")])
    estado = TextField('Estado', [validators.required(message=":estado?:"),validators.Length(min=1, max=45, message=":longitud requerida [1-20]:")])
    fechaDeModif = DateTimeField('FechaDeModif')
    
class EditStateItemForm(Form):
    """ Formulario de modificacion de estado de item """
    estado = SelectField("Estado", choices = [
        ("Activo", "Activo"),
        ("Eliminado", "Eliminado"),
        ("Aprobado", "Aprobado"),
        ("Revision", "Revision")])
    submit = SubmitField("POST")    

# Administrar LB

class CreateFormLineaBase(Form):
    """ Formulario para crear linea base"""
    nombre = TextField('Nombre', [validators.required(message=":nombre?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    descripcion = TextField('Descripcion', [validators.required(message=":descripcion?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    fase = TextField('Fase', [validators.required(message=":fase?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    
class ShowFormLineaBase(Form):
    """ Formulario para mostrar una linea base"""
    nombre = TextField('Nombre')
    descripcion = TextField('Descripcion')
    estado = TextField('Estado')
    
class EditFormLineaBase(Form):
    """ Formulario para editar linea base"""
    nombre = TextField('Nombre', [validators.required(message=":nombre?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    descripcion = TextField('Descripcion', [validators.required(message=":descripcion?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])


# Administrar Comite

class CreateFormComite(Form):
    """ Formulario para crear un comite de cambio """
    nombre = TextField('Nombre', [validators.required(message=":nombre?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    descripcion = TextField('Descripcion', [validators.required(message=":descripcion?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]?:")])
    cantMiembro = IntegerField('CantMiembro', [validators.required(message=":cantMiembro?:"), validators.NumberRange(min=1, max=150, message=":cantMiembro >= 1?:")])
     
class EditFormComite(Form):
    """ Formulario para editar un comite de cambio """
    descripcion = TextField('Descripcion', [validators.required(message=":descripcion?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]?:")])
    cantMiembro = IntegerField('CantMiembro', [validators.required(message=":cantMiembro?:"), validators.NumberRange(min=1, max=150, message=":cantMiembro >= 1?:")])
    
   
class ShowFormComite(Form):
    """ Formulario para mostrar un comite de cambio"""
    descripcion = TextField('Descripcion')
    cantMiembro = IntegerField('CantMiembro')
    proyectoId = TextField('ProyectoId')

# Solicitud

class CreateFormSolicitud(Form):
    """ Formulario para mostrar una solicitud de cambio """
    nombre = TextField('Nombre', [validators.required(message=":nombre?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    descripcion = TextField('Descripcion', [validators.required(message=":descripcion?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]?:")])
    proyecto_nombre = TextField('NombreProyecto', [validators.required(message=":nombre de proyecto?:")])
    
class ShowFormSolicitud(Form):
    """ Formulario para mostrar una solicitud de cambio """
    nombre = TextField('nombre')
    descripcion = TextField('descripcion')
    autor = TextField('autor')
    complejidad = TextField('complejidad')
    costo = TextField('costo')
    a_favor = TextField('Votos a favor')
    en_contra = TextField('Votos en contra')
    aceptar = SelectField('Aceptar Cambio?',choices=[('0','No'),('1','Si')])