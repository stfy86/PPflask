from wtforms import Form, TextField, FileField, PasswordField, \
     validators, IntegerField, SelectField, SubmitField, DateTimeField
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
    """ Formulario para crear un usuario"""
    name = TextField('Name', [validators.required(message=":name?:"), validators.Length(min=1, max=15, message=":longitud requerida [1-15]:")])
    password = PasswordField('Password', [validators.required(message=":password?:"), validators.Length(min=1, max=15, message=":longitud requerida [1-15]:")])
    confirmacion = PasswordField('Confirmacion', [validators.EqualTo('password')])
    nombre = TextField('Nombre', [validators.required(message=":nombre?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    apellido = TextField('Apellido', [validators.required(message=":apellido?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    email = TextField('Email', [validators.required(message=":email?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    telefono = IntegerField('Telefono', [validators.required(message=":telefono?:"), validators.NumberRange(min=None, max=None, message=":telefono?:")])
    obs = TextField('Obs', [validators.required(message=":obs?:"), validators.Length(min=1, max=150, message=":longitud requerida [1-150]:")])

class ShowFormUser(Form):
    """ Formulario para crear un usuario"""
    name = TextField('Name', [validators.required(message=":name?:"), validators.Length(min=1, max=15, message=":longitud requerida [1-15]:")])
    password = PasswordField('Password', [validators.required(message=":password?:"), validators.Length(min=1, max=15, message=":longitud requerida [1-15]:")])
    nombre = TextField('Nombre', [validators.required(message=":nombre?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    apellido = TextField('Apellido', [validators.required(message=":apellido?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    email = TextField('Email', [validators.required(message=":email?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    telefono = IntegerField('Telefono', [validators.required(message=":telefono?:"), validators.NumberRange(min=None, max=None, message=":telefono?:")])
    obs = TextField('Obs', [validators.required(message=":obs?:"), validators.Length(min=1, max=150, message=":longitud requerida [1-150]:")])
    estado = TextField('Estado', [validators.required()])

class EditStateForm(Form):
    """ Formulario de modificacion de estado de usuario """
    estado = SelectField("Estado", choices = [
        ("Inactivo", "Inactivo"),
        ("Activo", "Activo")])
    submit = SubmitField("POST")


# Administrar RolXPermiso

class CreateFormRol(Form):
    """ Formulario para crear rol"""
    nombre = TextField('Nombre', [validators.required(message=":nombre?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    ambito = TextField('Ambito', [validators.required(message=":ambito?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    descripcion = TextField('Descripcion', [validators.required(message=":descripcion?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])


# Administrar Proyecto

class CreateFormProject(Form):
    """ Formulario para crear proyecto"""
    nombre = TextField('Nombre', [validators.required( message=":nombre?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    descripcion = TextField('Descripcion', [validators.required(message=":descripcion?:"), validators.Length(min=1, max=150, message=":longitud requerida [1-150]:")])
    presupuesto = IntegerField('Presupuesto', [validators.required(message=":presupuesto?:"), validators.NumberRange(min=None, max=None, message=":presupuesto?:")])

class ShowFormProject(Form):
    """ Formulario para mostrar un proyecto"""
    nombre = TextField('Nombre', [validators.required( message=":nombre?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    descripcion = TextField('Descripcion', [validators.required(message=":descripcion?:"), validators.Length(min=1, max=150, message=":longitud requerida [1-150]:")])
    fechaDeCreacion = DateTimeField('FechaDeCreacion')
    estado = TextField('Estado', [validators.required(message=":estado?:")])
    presupuesto = IntegerField('Presupuesto', [validators.required(message=":presupuesto?:"), validators.NumberRange(min=None, max=None, message=":presupuesto?:")])
    
class EditStateProjectForm(Form):
    """ Formulario de modificacion de estado de proyecto """
    estado = SelectField("Estado", choices = [
        ("Activo", "Activo"),
        ("Pendiente", "Pendiente"),
        ("Finalizado", "Finalizado"),
        ("Inactivo", "Inactivo")])
    submit = SubmitField("POST")

class CreateFormRolProyecto(Form):
    """ Formulario para crear rol por proyecto"""
    nombre = TextField('Nombre', [validators.required(message=":nombre?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    descripcion = TextField('Descripcion', [validators.required(message=":descripcion?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
   
# Administrar Fase

class CreateFormFase(Form):
    """ Formulario para crear fase"""
    nombre = TextField('Nombre', [validators.required( message=":nombre?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    descripcion = TextField('Descripcion', [validators.required(message=":descripcion?:"), validators.Length(min=1, max=150, message=":longitud requerida [1-150]:")])
    orden = IntegerField('Orden',  [validators.required(message=":orden?:"), validators.NumberRange(min=1, max=150, message=":orden>=1:")])
   
class ShowFormFase(Form):
    """ Formulario para mostrar una fase """
    nombre = TextField('Nombre', [validators.required( message=":nombre?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    descripcion = TextField('Descripcion', [validators.required(message=":descripcion?:"), validators.Length(min=1, max=150, message=":longitud requerida [1-150]:")])
    fechaDeCreacion = DateTimeField('FechaDeCreacion')
    orden = IntegerField('Orden',  [validators.required(message=":orden?:"), validators.NumberRange(min=1, max=150, message=":orden>=1:")])
    estado = TextField('Estado', [validators.required(message=":estado?:")])


class EditStateFaseForm(Form):
    """ Formulario de modificacion de estado de fase """
    estado = SelectField("Estado", choices = [
        ("Activo", "Activo"),
        ("Pendiente", "Pendiente"),
        ("Finalizado", "Finalizado")])
    submit = SubmitField("POST")

# Administrar tipo de atributos

class CreateFormAtrib(Form):
    """ Formulario para crear un atributo"""
    nombre = TextField('Nombre', [validators.required(message=":nombre?:"),validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    tipoDeDato = SelectField("Tipo de Dato", choices = [
        ("Numerico", "Numerico"),
        ("Texto", "Texto"),
        ("Booleano", "Booleano"),
        ("Fecha", "Fecha")])
    detalle = IntegerField('Detalle', [validators.required(message=":detalle?:"), validators.NumberRange(min=None, max=None, message=":detalle?:")])
    descripcion = TextField('Descripcion', [validators.required(message=":descripcion?:"), validators.Length(min=1, max=150, message=":longitud requerida [1-150]:")])
    
class ShowFormAtrib(Form):
    """ Formulario para mostrar un atributo"""
    nombre = TextField('Nombre', [validators.required(message=":nombre?:"),validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    tipoDeDato = TextField("Tipo de Dato", [validators.required(message=":tipoDeDato?:"), validators.Length(min=1, max=20, message=":longitud requerida [1-20]:")])
    detalle = IntegerField('Detalle', [validators.required(message=":detalle?:"), validators.NumberRange(min=None, max=None, message=":detalle?:")])
    descripcion = TextField('Descripcion', [validators.required(message=":descripcion?:"),validators.Length(min=1, max=150, message=":longitud requerida [1-150]:")])

# Administrar tipo de item

class CreateFormTipoDeItem(Form):
    """ Formulario para crear tipo de item"""
    nombre = TextField('Nombre', [validators.required(message=":nombre?:"),validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    descripcion = TextField('Descripcion', [validators.required(message=":descripcion?:"), validators.Length(min=1, max=150, message=":longitud requerida [1-150]:")])
   
# Administrar item
    
class CreateFormItem(Form):
    """ Formulario para crear un item"""
    nombre = TextField('Nombre', [validators.required(message=":nombre?:"),validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    version = IntegerField('Version', [validators.required(message=":version?:"), validators.NumberRange(min=None, max=None, message=":version?:")])
    complejidad = IntegerField('Complejidad', [validators.required(message=":complejidad?:"), validators.NumberRange(min=None, max=None, message=":complejidad?:")])
    costo = IntegerField('Costo', [validators.required(message=":costo?:"), validators.NumberRange(min=None, max=None, message=":costo?:")])
        
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
        ("Inactivo", "Inactivo"),
        ("Aprobado", "Aprobado")])
    submit = SubmitField("POST")

class CreateFormLineaBase(Form):
    """ Formulario para crear rol"""
    nombre = TextField('Nombre', [validators.required(message=":nombre?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    descripcion = TextField('Descripcion', [validators.required(message=":descripcion?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    fase = TextField('Fase', [validators.required(message=":fase?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    
class ShowFormLineaBase(Form):
    """ Formulario para crear rol"""
    nombre = TextField('Nombre', [validators.required(message=":nombre?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    descripcion = TextField('Descripcion', [validators.required(message=":descripcion?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    estado = TextField('Estado', [validators.required(message=":estado?:")])
    
class EditFormStateLineaBase(Form):
    """ Formulario de modificacion de estado de linea base """
    estado = SelectField("Estado", choices = [
        ("Activo", "Activo"),
        ("Inactivo", "Inactivo"),
        ("Comprometida", "Comprometida")])
    submit = SubmitField("POST")
    
class EditFormLineaBase(Form):
    """ Formulario para editar linea base"""
    nombre = TextField('Nombre', [validators.required(message=":nombre?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
    descripcion = TextField('Descripcion', [validators.required(message=":descripcion?:"), validators.Length(min=1, max=45, message=":longitud requerida [1-45]:")])
