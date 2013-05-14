
#------------------------------------------------------------------------------#
# IMPORTS
#------------------------------------------------------------------------------#
from flask import Flask, render_template, request, redirect, url_for, g, \
     session, flash, escape, request
from werkzeug.routing import Rule
from werkzeug.datastructures import CallbackDict
from flaskext.sqlalchemy import SQLAlchemy

#------------------------------------------------------------------------------#
# FLASK APP
#------------------------------------------------------------------------------#
# Flask application and config
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

#------------------------------------------------------------------------------#
# MIDDLEWARE (to serve static files)
#------------------------------------------------------------------------------#
# Middleware to serve the static files
from werkzeug import SharedDataMiddleware
import os
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        '/': os.path.join(os.path.dirname(__file__), 'templates',
        app.config['DEFAULT_TPL'])
})
 

#------------------------------------------------------------------------------#
# CONTROLLERS
#------------------------------------------------------------------------------#

# INGRESO AL SISTEMA

@app.before_request
def check_user_status():
    """ Checkea estatus """
    from models import User
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])


@app.route('/')
def index():
    """ Pagina Principal """
    from models import User
    return render_template(app.config['DEFAULT_TPL']+'/index.html',
			    conf = app.config,
			    users = User.query.order_by(User.name.desc()).all(),)
                            

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Logueo al sistema """
    from models import User
    from form import LoginForm
    if g.user is None:
        error = None
        if request.method=='POST':
            u = User.query.filter(User.name == request.form['username'], 
                                  User.passwd == request.form['password']).first()
            if u is None:
                error = 'Nick o Password incorrecto.'
            else:
                print u.idUser
                session['logged_in'] = True
                session['user_id'] = u.idUser
                session['user_name'] = u.name
                flash('Usted se ha conectado')
                return redirect(url_for('index'))
            
        return render_template(app.config['DEFAULT_TPL']+'/login.html',
                               conf = app.config,
                               form = LoginForm(request.form),
                               error = error)
    else:
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    """ Logout del sistema """
    if g.user is not None:
        session.pop('logged_in', None)
        session.pop('user_id', None)
        session.pop('user_name', None)
        session["__invalidate__"] = True
        flash('Usted se ha desconectado')
    return redirect(url_for('index'))



#  MODULO DE SISTEMA

@app.route('/administracion', methods=['GET','POST'])
def administracion():
    """ Modulo Administracion """
    return render_template(app.config['DEFAULT_TPL']+'/administracion.html',
			    conf = app.config,)                                             

@app.route('/gestion', methods=['GET','POST'])
def gestion():
    """ Modulo Gestion """
    return render_template(app.config['DEFAULT_TPL']+'/gestion.html',
			    conf = app.config,)

@app.route('/desarrollo', methods=['GET','POST'])
def desarrollo():
    """ Modulo Desarrollo """
    return render_template(app.config['DEFAULT_TPL']+'/desarrollo.html',
			    conf = app.config,)
# ADMINISTRAR USUARIO


@app.route('/addUser', methods=['GET','POST'])
def addUser():
    """Controlador para crear usuario"""
    from models import User
    from form import CreateFormUser
    from ctrl.mgrUser import MgrUser
    if g.user is None:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            form = CreateFormUser(request.form, name = request.form['name'],
                        password = request.form['password'],
                        confirmacion = request.form['confirmacion'],
                        nombre = request.form['nombre'],
                        apellido = request.form['apellido'],
                        email = request.form['email'],
                        telefono = request.form['telefono'],
                        obs = request.form['obs'])
            if form.validate():
                user = User(name = request.form['name'],
                            passwd = request.form['password'],
                            nombre = request.form['nombre'],
                            apellido = request.form['apellido'],
                            email = request.form['email'],
                            telefono = request.form['telefono'],
                            obs = request.form['obs'])
                MgrUser().guardar(user)
                flash('Se ha creado correctamente el usuario')
                return redirect(url_for('listEdit'))
            else:
                return render_template(app.config['DEFAULT_TPL']+'/formUser.html',
                            conf = app.config,
                            form = form)
    return render_template(app.config['DEFAULT_TPL']+'/formUser.html',
                conf = app.config,
                form = CreateFormUser())


@app.route('/deleteUser/<path:nombre>.html')
def deleteUser(nombre):
    """ Elimina un usuario """
    from ctrl.mgrUser import MgrUser
    if g.user is None:
        return redirect(url_for('login'))   
    else:
        MgrUser().borrar(nombre)
        flash('Se ha borrado correctamente')
        return redirect(url_for('listEdit'))
                             

@app.route('/edit/<path:nombre>.html', methods=['GET','POST'])
def editState(nombre):
    """ Modifica el estado de un usuario """
    from form import EditStateForm
    from ctrl.mgrUser import MgrUser
    if g.user is None:
        return redirect(url_for('login'))
    else:
        user = MgrUser().filtrar(nombre)
        form = EditStateForm(request.form, estado = user.estado)
	if request.method == 'POST' and form.validate(): 
                MgrUser().estado(nombre, request.form['estado'])
		return redirect(url_for('listEdit'))
	return render_template(app.config['DEFAULT_TPL']+'/editState.html',
			       conf = app.config,
			       form = EditStateForm())


@app.route('/listEdit')
def listEdit():
    """ Lista los datos de un usuario """
    from ctrl.mgrUser import MgrUser
    if g.user is None:
        return redirect(url_for('login'))   
    list = MgrUser().listar()
    return render_template(app.config['DEFAULT_TPL']+'/listEdit.html',
                           conf = app.config,
                           list = list) 


@app.route('/editUser/<path:nombre>.html', methods=['GET','POST'])
def editUser(nombre):
    """ Modifica los datos de un usuario """
    from form import CreateFormUser
    from ctrl.mgrUser import MgrUser
    if g.user is None:
        return redirect(url_for('login'))
    else:
        user = MgrUser().filtrar(nombre)
        form = CreateFormUser(request.form, name = user.name,
                        password = user.passwd,
                        confirmacion = user.passwd,
                        nombre = user.nombre,
                        apellido = user.apellido,
                        email = user.email,
                        telefono = user.telefono,
                        obs = user.obs)
	if request.method == 'POST' and form.validate():
            MgrUser().modificar(nombre, request.form['name'], 
            request.form['password'], request.form['nombre'],
            request.form['apellido'], request.form['email'],
            request.form['telefono'], request.form['obs'])
            flash('Se ha modificado correctamente el usuario')
            return redirect(url_for('listEdit'))
    return render_template(app.config['DEFAULT_TPL']+'/editUser.html',
			       conf = app.config,
			       form = form)
                               

@app.route('/showUser/<path:nombre>.html', methods=['GET','POST'])
def showUser(nombre):
    """ Muestra los datos de un usuario """
    from ctrl.mgrUser import MgrUser
    from form import ShowFormUser
    if g.user is None:
        return redirect(url_for('login'))
    else:
        user = MgrUser().filtrar(nombre)
        form = ShowFormUser(request.form, name = user.name, 
               password = user.passwd, nombre = user.nombre,
               apellido = user.apellido, email = user.email,
               telefono = user.telefono, obs = user.obs,
               estado = user.estado)
        if request.method == 'POST':
            if request.form.get('edit', None) == "Modificar Usuario":
                return redirect(url_for('editUser', nombre = user.name))
            elif request.form.get('delete', None) == "Eliminar Usuario":
                return redirect(url_for('deleteUser', nombre = user.name))
            elif request.form.get('state', None) == "Modificar Estado de Usuario":
                return redirect(url_for('editState', nombre = user.name))
	return render_template(app.config['DEFAULT_TPL']+'/showUser.html',
			       conf = app.config,
			       form = form)


# ADMINISTRAR ROL


@app.route('/listRolPermiso', methods=['GET','POST'])
def listRolPermiso():
    from ctrl.mgrRol import MgrRol
    if g.user is None:
        return redirect(url_for('login'))
    else:
        return render_template(app.config['DEFAULT_TPL']+'/listRolPermiso.html',
                           conf = app.config,
                           list = MgrRol().listar())


@app.route('/addRol', methods=['GET','POST'])
def addRol():
    from models import Rol
    from form import CreateFormRol
    from ctrl.mgrRol import MgrRol
    if g.user is None:
        return redirect(url_for('login'))
    else:
	if request.method == 'POST':
            form = CreateFormRol(request.form, nombre = request.form['nombre'], 
                        ambito = request.form['ambito'],
                        descripcion = request.form['descripcion'])
            if form.validate():
                rol = Rol(nombre = request.form['nombre'],
                        ambito = request.form['ambito'],
                        descripcion = request.form['descripcion'])    
                MgrRol().guardar(rol)
                flash('Se ha creado correctamente el rol')
                return redirect(url_for('listRolPermiso'))
            else:
                return render_template(app.config['DEFAULT_TPL']+'/formRol.html',
			       conf = app.config,
			       form = form)
    return render_template(app.config['DEFAULT_TPL']+'/formRol.html',
			       conf = app.config,
			       form = CreateFormRol())


@app.route('/showRol/<path:nombre>.html', methods=['GET','POST'])
def showRol(nombre):
    from ctrl.mgrRol import MgrRol
    from form import CreateFormRol
    if g.user is None:
        return redirect(url_for('login'))
    else:
        rol = MgrRol().filtrar(nombre)
        form = CreateFormRol(request.form, nombre = rol.nombre, 
                    ambito = rol.ambito,
                    descripcion = rol.descripcion)
        if request.method == 'POST':
            if request.form.get('edit', None) == "Modificar Rol":
                return redirect(url_for('editRol', nombre = rol.nombre))
            elif request.form.get('delete', None) == "Eliminar Rol":
                return redirect(url_for('deleteRol', nombre = rol.nombre))
	return render_template(app.config['DEFAULT_TPL']+'/showRol.html',
			       conf = app.config,
			       form = form)


@app.route('/editRol/<path:nombre>.html', methods=['GET','POST'])
def editRol(nombre):
    from ctrl.mgrRol import MgrRol
    from form import CreateFormRol
    if g.user is None:
        return redirect(url_for('login'))
    else:
        rol = MgrRol().filtrar(nombre)
        form = CreateFormRol(request.form, nombre = rol.nombre, 
                    ambito = rol.ambito,    
                    descripcion = rol.descripcion)
	if request.method == 'POST' and form.validate():
            MgrRol().modificar(nombre, request.form['nombre'],
            request.form['ambito'], request.form['descripcion'])
            flash('Se ha modificado correctamente el rol')
            return redirect(url_for('listRolPermiso'))
    return render_template(app.config['DEFAULT_TPL']+'/editRol.html',
			       conf = app.config,
			       form = form)


@app.route('/deleteRol/<path:nombre>.html')
def deleteRol(nombre):
    from ctrl.mgrRol import MgrRol
    if g.user is None:
        return redirect(url_for('login'))   
    else:
        MgrRol().borrar(nombre)
        flash('Se ha borrado correctamente')
        return redirect(url_for('listRolPermiso'))


# ADMINISTRAR PROYECTO


@app.route('/listEditProject')
def listEditProject():
    """ Lista editable de proyectos que se alojan en la base de datos"""
    from ctrl.mgrProject import MgrProject
    if g.user is None:
        return redirect(url_for('login'))
    else:
        return render_template(app.config['DEFAULT_TPL']+'/listEditProject.html',
                           conf = app.config,
                           list = MgrProject().listar(),) 


@app.route('/showProject/<path:nombre>.html', methods=['GET','POST'])
def showProject(nombre):
    """  Muestra un formulario no editable del proyecto con las opciones de modificar, eliminar proyecto """
    from form import ShowFormProject
    from ctrl.mgrProject import MgrProject
    if g.user is None:
        return redirect(url_for('login'))
    else:
        project = MgrProject().filtrar(nombre)
        form = ShowFormProject(request.form, nombre = project.nombre,
               descripcion = project.descripcion, 
               fechaDeCreacion = project.fechaDeCreacion,
               estado = project.estado)
        if request.method == 'POST':
            if request.form.get('edit', None) == "Modificar Proyecto":
                return redirect(url_for('editProject', nombre = project.nombre))
            elif request.form.get('delete', None) == "Eliminar Proyecto":
                return redirect(url_for('deleteProject', nombre = project.nombre))
            
	return render_template(app.config['DEFAULT_TPL']+'/showProject.html',
			       conf = app.config,
			       form = form)


@app.route('/editProject/<path:nombre>.html', methods=['GET','POST'])
def editProject(nombre):
    """ Muestra el formulario editable del proyecto """
    from form import CreateFormProject
    from ctrl.mgrProject import MgrProject
    if g.user is None:
        return redirect(url_for('login'))
    else:
        project = MgrProject().filtrar(nombre)
        form = CreateFormProject(request.form, nombre = project.nombre,
               descripcion = project.descripcion)
	if request.method == 'POST' and form.validate:
            MgrProject().modificar(nombre, request.form['nombre'],request.form['descripcion'])
            flash('Se ha modificado correctamente el proyecto')
            return redirect(url_for('listEditProject'))
    return render_template(app.config['DEFAULT_TPL']+'/formProject.html',
			       conf = app.config,
			       form = form)


@app.route('/deleteProject/<path:nombre>.html')
def deleteProject(nombre):
    """ Elimina un proyecto """
    from ctrl.mgrProject import MgrProject
    if g.user is None:
        return redirect(url_for('login'))   
    else:
        MgrProject().borrar(nombre)
        flash('Se ha borrado correctamente')
        return redirect(url_for('listEditProject'))
                             

@app.route('/addProject', methods=['GET','POST'])
def addProject():
    """ Agrega un proyecto """
    from models import Proyecto
    from form import CreateFormProject
    from ctrl.mgrProject import MgrProject
    if g.user is None:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            form = CreateFormProject(request.form, 
                                     request.form['nombre'], 
                                     descripcion = request.form['descripcion'])
            if form.validate():
                project = Proyecto(nombre = request.form['nombre'], 
                                   descripcion = request.form['descripcion'])    
                MgrProject().guardar(project)
                flash('Se ha creado correctamente el proyecto')
                return redirect(url_for('listEditProject'))
            else:
                return render_template(app.config['DEFAULT_TPL']+'/formProject.html',
                            conf = app.config,
                            form = form)
                
    return render_template(app.config['DEFAULT_TPL']+'/formProject.html',
                conf = app.config,
                form = CreateFormProject())



# ADMINISTRAR FASE


@app.route('/listEditFase')
def listEditFase():
    """ Lista editable de fase que se alojan en la base de datos"""
    from ctrl.mgrFase import MgrFase
    if g.user is None:
        return redirect(url_for('login'))
    else:
        return render_template(app.config['DEFAULT_TPL']+'/listEditFase.html',
                           conf = app.config,
                           list = MgrFase().listar(),) 

@app.route('/showFase/<path:nombre>.html', methods=['GET','POST'])
def showFase(nombre):
    """  Muestra un formulario no editable de la fase con las opciones de modificar, eliminar fase """
    from ctrl.mgrFase import MgrFase
    from form import ShowFormFase
    if g.user is None:
        return redirect(url_for('login'))
    else:
        fase = MgrFase().filtrar(nombre)
        form = ShowFormFase(request.form, nombre = fase.nombre,
               descripcion = fase.descripcion, 
               fechaDeCreacion = fase.fechaDeCreacion,
               orden = fase.orden,
               estado = fase.estado)
        if request.method == 'POST':
            if request.form.get('edit', None) == "Modificar Fase":
                return redirect(url_for('editFase', nombre = fase.nombre))
            elif request.form.get('delete', None) == "Eliminar Fase":
                return redirect(url_for('deleteFase', nombre = fase.nombre))
            
	return render_template(app.config['DEFAULT_TPL']+'/showFase.html',
			       conf = app.config,
			       form = form)


@app.route('/editFase/<path:nombre>.html', methods=['GET','POST'])
def editFase(nombre):
    """ 
    Muestra el formulario editable de la fase 
      @param nombre atributo de la fase
    """
    from form import CreateFormFase
    from ctrl.mgrFase import MgrFase
    if g.user is None:
        return redirect(url_for('login'))
    else:
        fase = MgrFase().filtrar(nombre)
        form = CreateFormFase(request.form, nombre = fase.nombre,
               descripcion = fase.descripcion, orden = fase.orden)
	if request.method == 'POST' and form.validate:
            fase.nombre = request.form['nombre']
            fase.descripcion = request.form['descripcion']
            fase.orden =  request.form['orden'] 
            MgrFase().modificar(nombre, fase.nombre , fase.descripcion, fase.orden)
            flash('Se ha modificado correctamente el fase')
            return redirect(url_for('listEditFase'))
    return render_template(app.config['DEFAULT_TPL']+'/formFase.html',
			       conf = app.config,
			       form = form)


@app.route('/deleteFase/<path:nombre>.html')
def deleteFase(nombre):
    """ 
    Elimina un fase
    @param nombre elimina un usuario por el atributo nombre
    """
    from ctrl.mgrFase import MgrFase
    if g.user is None:
        return redirect(url_for('login'))   
    else:
        MgrFase().borrar(nombre)
        flash('Se ha borrado correctamente')
        return redirect(url_for('listEditFase'))


@app.route('/addFase', methods=['GET','POST'])
def addFase():
    """ Agrega una fase """
    from models import Fase
    from form import CreateFormFase
    from ctrl.mgrFase import MgrFase
    if g.user is None:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            form = CreateFormFase(request.form, request.form['nombre'], descripcion = request.form['descripcion'], orden = request.form['orden'])
            if form.validate():
                fase = Fase(nombre = request.form['nombre'], descripcion = request.form['descripcion'], orden = request.form['orden'])    
                MgrFase().guardar(fase)
                flash('Se ha creado correctamente la fase')
                return redirect(url_for('listEditFase'))
            else:
                return render_template(app.config['DEFAULT_TPL']+'/formFase.html',
                            conf = app.config,
                            form = form)
    return render_template(app.config['DEFAULT_TPL']+'/formFase.html',
                conf = app.config,
                form = CreateFormFase())
# ADMINISTRAR TIPO DE ATRIBUTO


@app.route('/listAtrib')
def listAtrib():
    """ Lista todos los tipos de atributo """
    from ctrl.mgrTipoDeAtrib import MgrTipoDeAtrib
    if g.user is None:
        return redirect(url_for('login'))
    else:
        return render_template(app.config['DEFAULT_TPL']+'/listAtrib.html',
                           conf = app.config,
                           list = MgrTipoDeAtrib().listar()) 
                           
@app.route('/addAtrib', methods=['GET','POST'])
def addAtrib():
    """ Agrega un nuevo tipo de atributo """
    from form import CreateFormAtrib
    from models import TipoDeAtributo
    from ctrl.mgrTipoDeAtrib import MgrTipoDeAtrib
    if g.user is None:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            form = CreateFormAtrib(request.form, nombre = request.form['nombre'], 
                    tipoDeDato = request.form['tipoDeDato'], 
                    detalle = request.form['detalle'], 
                    descripcion = request.form['descripcion']) 
            if form.validate():
                    atrib = TipoDeAtributo(nombre = request.form['nombre'], tipoDeDato = request.form['tipoDeDato'],
                    detalle = request.form['detalle'], descripcion = request.form['descripcion'])    
                    MgrTipoDeAtrib().guardar(atrib)
                    flash('Se ha creado correctamente el atributo')
                    return redirect(url_for('listAtrib'))
            else:
                    return render_template(app.config['DEFAULT_TPL']+'/addAtrib.html',
                                   conf = app.config,
                                   form = form)
    return render_template(app.config['DEFAULT_TPL']+'/addAtrib.html',
			       conf = app.config,
			       form = CreateFormAtrib())
                               
@app.route('/showAtrib/<path:nombre>.html', methods=['GET','POST'])
def showAtrib(nombre):
    """ Muestra los datos de un atributo """
    from ctrl.mgrTipoDeAtrib import MgrTipoDeAtrib
    from form import ShowFormAtrib
    if g.user is None:
        return redirect(url_for('login'))
    else:
        atrib = MgrTipoDeAtrib().filtrar(nombre)
        form = ShowFormAtrib(request.form, nombre = atrib.nombre,
               tipoDeDato = atrib.tipoDeDato, detalle = atrib.detalle, 
               descripcion = atrib.descripcion)
        if request.method == 'POST':
            if request.form.get('edit', None) == "Modificar Atributo":
                return redirect(url_for('editAtrib', nombre = atrib.nombre))
            elif request.form.get('delete', None) == "Eliminar Atributo":
                return redirect(url_for('deleteAtrib', nombre = atrib.nombre))
	return render_template(app.config['DEFAULT_TPL']+'/showAtrib.html',
			       conf = app.config,
			       form = form)
                               
@app.route('/editAtrib/<path:nombre>.html', methods=['GET','POST'])
def editAtrib(nombre):
    """ Modifica los datos de un atributo """
    from form import CreateFormAtrib
    from ctrl.mgrTipoDeAtrib import MgrTipoDeAtrib
    if g.user is None:
        return redirect(url_for('login'))
    else:
        atrib = MgrTipoDeAtrib().filtrar(nombre)
        form = CreateFormAtrib(request.form, nombre = atrib.nombre,
               tipoDeDato = atrib.tipoDeDato, detalle = atrib.detalle, 
               descripcion = atrib.descripcion)
	if request.method == 'POST' and form.validate():
            MgrTipoDeAtrib().modificar(nombre, request.form['nombre'], 
            request.form['tipoDeDato'], request.form['detalle'], 
            request.form['descripcion'])
            flash('Se ha modificado correctamente el atributo')
            return redirect(url_for('listAtrib'))
    return render_template(app.config['DEFAULT_TPL']+'/editAtrib.html',
			       conf = app.config,
			       form = form)

@app.route('/deleteAtrib/<path:nombre>.html')
def deleteAtrib(nombre):
    from ctrl.mgrTipoDeAtrib import MgrTipoDeAtrib
    if g.user is None:
        return redirect(url_for('login'))   
    else:
        MgrTipoDeAtrib().borrar(nombre)
        flash('Se ha borrado correctamente')
        return redirect(url_for('listAtrib'))
    
# ADMINISTRAR TIPO DE ITEM

@app.route('/listTipoDeItem')
def listTipoDeItem():
    """ Lista los datos de un tipo de item """
    from ctrl.mgrTipoDeItem import MgrTipoDeItem
    if g.user is None:
        return redirect(url_for('login'))   
    list = MgrTipoDeItem().listar()
    return render_template(app.config['DEFAULT_TPL']+'/listTipoDeItem.html',
                           conf = app.config,
                           list = list) 
                    
@app.route('/showTipoDeItem/<path:nombre>.html', methods=['GET','POST'])
def showTipoDeItem(nombre):
    """ Muestra los datos de un tipo de item """
    from ctrl.mgrTipoDeItem import MgrTipoDeItem
    from form import CreateFormTipoDeItem
    if g.user is None:
        return redirect(url_for('login'))
    else:
        tipoDeItem = MgrTipoDeItem().filtrar(nombre)
        form = CreateFormTipoDeItem(request.form, nombre = tipoDeItem.nombre, 
               descripcion = tipoDeItem.descripcion)
        if request.method == 'POST':
            if request.form.get('edit', None) == "Modificar Tipo de Item":
                return redirect(url_for('editTipoDeItem', nombre = tipoDeItem.nombre))
            elif request.form.get('delete', None) == "Eliminar Tipo de Item":
                return redirect(url_for('deleteTipoDeItem', nombre = tipoDeItem.nombre))
	return render_template(app.config['DEFAULT_TPL']+'/showTipoDeItem.html',
			       conf = app.config,
			       form = form)
                               
@app.route('/addTipoDeItem', methods=['GET','POST'])
def addTipoDeItem():
    """Controlador para crear un tipo de item"""
    from models import TipoDeItem
    from ctrl.mgrTipoDeItem import MgrTipoDeItem
    from form import CreateFormTipoDeItem
    if g.user is None:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            form = CreateFormTipoDeItem(request.form, nombre = request.form['nombre'], 
                    descripcion = request.form['descripcion'])
            if form.validate():
                tipoDeItem = TipoDeItem(nombre = request.form['nombre'],
                            descripcion = request.form['descripcion'])
                MgrTipoDeItem().guardar(tipoDeItem)
                flash('Se ha creado correctamente el tipo de item')
                return redirect(url_for('listTipoDeItem'))
            else:
                return render_template(app.config['DEFAULT_TPL']+'/addTipoDeItem.html',
                            conf = app.config,
                            form = form)
    return render_template(app.config['DEFAULT_TPL']+'/addTipoDeItem.html',
                conf = app.config,
                form = CreateFormTipoDeItem())
                
@app.route('/editTipoDeItem/<path:nombre>.html', methods=['GET','POST'])
def editTipoDeItem(nombre):
    """ Modifica los datos de un tipo de item """
    from ctrl.mgrTipoDeItem import MgrTipoDeItem
    from form import CreateFormTipoDeItem
    if g.user is None:
        return redirect(url_for('login'))
    else:
        tipoDeItem = MgrTipoDeItem().filtrar(nombre)
        form = CreateFormTipoDeItem(request.form, nombre = tipoDeItem.nombre,
                descripcion = tipoDeItem.descripcion)
	if request.method == 'POST' and form.validate():
            MgrTipoDeItem().modificar(nombre, request.form['nombre'], 
                            request.form['descripcion'])
            flash('Se ha modificado correctamente el tipo de item')
            return redirect(url_for('listTipoDeItem'))
    return render_template(app.config['DEFAULT_TPL']+'/editTipoDeItem.html',
			       conf = app.config,
			       form = form)
                
@app.route('/deleteTipoDeItem/<path:nombre>.html')
def deleteTipoDeItem(nombre):
    """ Elimina un usuario """
    from ctrl.mgrTipoDeItem import MgrTipoDeItem
    if g.user is None:
        return redirect(url_for('login'))   
    else:
        MgrTipoDeItem().borrar(nombre)
        flash('Se ha borrado correctamente')
        return redirect(url_for('listTipoDeItem'))

# ADMINISTRAR ITEM

@app.route('/listItem')
def listItem():
    """ Lista los datos de un tipo de item """
    from ctrl.mgrItem import MgrItem
    if g.user is None:
        return redirect(url_for('login'))   
    list = MgrItem().listar()
    return render_template(app.config['DEFAULT_TPL']+'/listItem.html',
                           conf = app.config,
                           list = list) 
                           
@app.route('/showItem/<path:nombre>.html', methods=['GET','POST'])
def showItem(nombre):
    """  Muestra un formulario no editable del item con las opciones de modificar, eliminar item """
    from ctrl.mgrItem import MgrItem
    from form import ShowFormItem
    if g.user is None:
        return redirect(url_for('login'))
    else:
        item = MgrItem().filtrar(nombre)
        form = ShowFormItem(request.form, nombre = item.nombre,
               version = item.version, complejidad = item.complejidad,
               costo = item.costo, estado = item.estado, fechaDeModif = item.fechaDeModif)
        if request.method == 'POST':
            if request.form.get('edit', None) == "Modificar Item":
                return redirect(url_for('editItem', nombre = item.nombre))
            elif request.form.get('delete', None) == "Eliminar Item":
                return redirect(url_for('deleteItem', nombre = item.nombre))
            elif request.form.get('state', None) == "Modificar Estado de Item":
                return redirect(url_for('editItemState', nombre = item.nombre))
	return render_template(app.config['DEFAULT_TPL']+'/showItem.html',
			       conf = app.config,
			       form = form)

@app.route('/addItem', methods=['GET','POST'])
def addItem():
    """Controlador para crear item"""
    from models import Item
    from ctrl.mgrItem import MgrItem
    from form import CreateFormItem
    if g.user is None:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            form = CreateFormItem(request.form, nombre = request.form['nombre'],
                        version = request.form['version'],
                        complejidad = request.form['complejidad'],
                        costo = request.form['costo'])
            if form.validate():
                item = Item(nombre = request.form['nombre'],
                            version = request.form['version'],
                            complejidad = request.form['complejidad'],
                            costo = request.form['costo'])
                MgrItem().guardar(item)
                flash('Se ha creado correctamente el item')
                return redirect(url_for('listItem'))
            else:
                return render_template(app.config['DEFAULT_TPL']+'/addItem.html',
                            conf = app.config,
                            form = form)
    return render_template(app.config['DEFAULT_TPL']+'/addItem.html',
                conf = app.config,
                form = CreateFormItem())
                
@app.route('/editItem/<path:nombre>.html', methods=['GET','POST'])
def editItem(nombre):
    """ Modifica los datos de un item """
    from ctrl.mgrItem import MgrItem
    from form import CreateFormItem
    if g.user is None:
        return redirect(url_for('login'))
    else:
        item = MgrItem().filtrar(nombre)
        form = CreateFormItem(request.form, nombre = item.nombre,
                        version = item.version,
                        complejidad = item.complejidad,
                        costo = item.costo)
	if request.method == 'POST' and form.validate():
            MgrItem().modificar(nombre, request.form['nombre'],
            request.form['version'], request.form['complejidad'],
            request.form['costo'])
            flash('Se ha modificado correctamente el item')
            return redirect(url_for('listItem'))
    return render_template(app.config['DEFAULT_TPL']+'/editItem.html',
			       conf = app.config,
			       form = form)
                               
@app.route('/deleteItem/<path:nombre>.html')
def deleteItem(nombre):
    """ Elimina un item """
    from ctrl.mgrItem import MgrItem
    if g.user is None:
        return redirect(url_for('login'))   
    else:
        MgrItem().borrar(nombre)
        flash('Se ha borrado correctamente')
        return redirect(url_for('listItem'))

@app.route('/editItemState/<path:nombre>.html', methods=['GET','POST'])
def editItemState(nombre):
    """ Modifica el estado de un usuario """
    from form import EditStateItemForm
    from ctrl.mgrItem import MgrItem
    if g.user is None:
        return redirect(url_for('login'))
    else:
        item = MgrItem().filtrar(nombre)
        form = EditStateItemForm(request.form, estado = item.estado)
	if request.method == 'POST' and form.validate(): 
                MgrItem().estado(nombre, request.form['estado'])
		return redirect(url_for('listItem'))
	return render_template(app.config['DEFAULT_TPL']+'/editItemState.html',
			       conf = app.config,
			       form = EditStateItemForm())
                               
#------------------------------------------------------------------------------#
# MAIN
#------------------------------------------------------------------------------#



if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    #app.run()
    from werkzeug.serving import run_simple
    run_simple('127.0.0.1', 8080, app, use_debugger=True, use_reloader=True)



