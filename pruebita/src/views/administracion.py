from modulo import *
from flask import Flask, render_template, request, redirect, url_for, g, \
     session, flash, escape, send_file


                           
#------------------------------------------------------------------------------#
# MODULO ADMINISTRACION
#------------------------------------------------------------------------------#

# ADMINISTRAR USUARIO

@app.route('/addUser', methods=['GET','POST'])
def addUser():
    """Controlador para crear usuario"""
    if g.user is None:
        return redirect(url_for('login'))
    else:
        opcion = request.form.get("opcion")
        if request.method == 'POST':
            ambito = 'sistema'
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
                nombre = user.name
                MgrUser().guardar(user)
                MgrUser().asignarRol(nombre, opcion)
                flash('Se ha creado correctamente el usuario')
                return redirect(url_for('listEdit'))
            else:
                return render_template(app.config['DEFAULT_TPL']+'/formUser.html',
                            conf = app.config,
                            form = form)
    return render_template(app.config['DEFAULT_TPL']+'/formUser.html',
                conf = app.config,
                list = MgrRol().listar(),
                form = CreateFormUser())


@app.route('/deleteUser/<path:nombre>.html')
def deleteUser(nombre):
    """ Elimina un usuario """
    if g.user is None:
        return redirect(url_for('login'))   
    else:
        user = MgrUser().filtrar(nombre)
        flash(MgrUser().borrar(user))
        return redirect(url_for('listEdit'))
                             

@app.route('/edit/<path:nombre>.html', methods=['GET','POST'])
def editState(nombre):
    """ Modifica el estado de un usuario """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        user = MgrUser().filtrar(nombre)
        form = EditStateForm(request.form, estado = user.estado)
	if request.method == 'POST' and form.validate(): 
                flash(MgrUser().estado(nombre, request.form['estado']))
		return redirect(url_for('listEdit'))
	return render_template(app.config['DEFAULT_TPL']+'/editState.html',
			       conf = app.config,
			       form = EditStateForm())


@app.route('/listEdit')
def listEdit():
    """ Lista los datos de un usuario """
    if g.user is None:
        return redirect(url_for('login'))   
    list = MgrUser().listar()
    return render_template(app.config['DEFAULT_TPL']+'/listEdit.html',
                           conf = app.config,
                           list = list) 


@app.route('/editUser/<path:nombre>.html', methods=['GET','POST'])
def editUser(nombre):
    """ Modifica los datos de un usuario """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        user = MgrUser().filtrar(nombre)
        form = CreateFormUser(request.form,
                        name = user.name,
                        password = user.passwd,
                        confirmacion = user.passwd,
                        nombre = user.nombre,
                        apellido = user.apellido,
                        email = user.email,
                        telefono = user.telefono,
                        obs = user.obs)
	if request.method == 'POST' and form.validate():
            MgrUser().modificar(nombre, request.form['password'],
            request.form['confirmacion'], request.form['nombre'],
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

# ADMINISTRAR TIPO DE ATRIBUTO


@app.route('/listAtrib')
def listAtrib():
    """ Lista todos los tipos de atributo """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        return render_template(app.config['DEFAULT_TPL']+'/listAtrib.html',
                           conf = app.config,
                           list = MgrTipoDeAtrib().listar()) 
                           
@app.route('/addAtrib', methods=['GET','POST'])
def addAtrib():
    """ Agrega un nuevo tipo de atributo """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            tipoDeDato = request.form['tipoDeDato']
            if tipoDeDato == "archivo":
                arch = request.files['file']
                form = CreateFormAtrib(request.form, nombre = request.form['nombre'],
                        descripcion = request.form['descripcion']) 
                if form.validate():
                        atrib = TipoDeAtributo(nombre = request.form['nombre'], tipoDeDato = request.form['tipoDeDato'],
                        detalle = 0, descripcion = request.form['descripcion'], 
                        filename = arch.filename, archivo = arch.read())    
                        MgrTipoDeAtrib().guardar(atrib)
                        flash('Se ha creado correctamente el atributo')
                        return redirect(url_for('listAtrib'))
                else:
                        return render_template(app.config['DEFAULT_TPL']+'/addAtrib.html',
                                       conf = app.config,
                                       form = form)
            elif tipoDeDato == "numerico" or tipoDeDato == "texto":
                    form = CreateFormAtrib(request.form, nombre = request.form['nombre'],
                            descripcion = request.form['descripcion']) 
                    if form.validate():
                            atrib = TipoDeAtributo(nombre = request.form['nombre'], tipoDeDato = request.form['tipoDeDato'],
                            detalle = request.form['detalle'], descripcion = request.form['descripcion'], 
                            filename = "", archivo = None)    
                            MgrTipoDeAtrib().guardar(atrib)
                            flash('Se ha creado correctamente el atributo')
                            return redirect(url_for('listAtrib'))
                    else:
                            return render_template(app.config['DEFAULT_TPL']+'/addAtrib.html',
                                           conf = app.config,
                                           form = form)
            elif tipoDeDato == "booleano" or tipoDeDato == "fecha":
                    form = CreateFormAtrib(request.form, nombre = request.form['nombre'],
                            descripcion = request.form['descripcion']) 
                    if form.validate():
                            atrib = TipoDeAtributo(nombre = request.form['nombre'], tipoDeDato = request.form['tipoDeDato'],
                            detalle = 0, descripcion = request.form['descripcion'], 
                            filename = "", archivo = None)    
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
    if g.user is None:
        return redirect(url_for('login'))
    else:
        atrib = MgrTipoDeAtrib().filtrar(nombre)
        form = ShowFormAtrib(request.form, nombre = atrib.nombre,
               tipoDeDato = atrib.tipoDeDato, detalle = atrib.detalle, 
               descripcion = atrib.descripcion, filename = atrib.filename) 
        if request.method == 'POST':
            if request.form.get('descargar', None) == "Descargar":
                return redirect(url_for('descargar', nombre = atrib.nombre))
            elif request.form.get('edit', None) == "Modificar Atributo":
                return redirect(url_for('editAtrib', nombre = atrib.nombre))
            elif request.form.get('delete', None) == "Eliminar Atributo":
                return redirect(url_for('deleteAtrib', nombre = atrib.nombre))
	return render_template(app.config['DEFAULT_TPL']+'/showAtrib.html',
			       conf = app.config,
			       form = form)
                               
@app.route('/editAtrib/<path:nombre>.html', methods=['GET','POST'])
def editAtrib(nombre):
    """ Modifica los datos de un atributo """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        atrib = MgrTipoDeAtrib().filtrar(nombre)
        form = EditFormAtrib(request.form, nombre = atrib.nombre,
               detalle = atrib.detalle, descripcion = atrib.descripcion, 
               filename = atrib.filename)
        hola = MgrTipoDeAtrib().verificar_borrar(nombre)
        if hola == 1:
            flash('NO se puede modificar, esta relacionado a un tipo de Item')
            return redirect(url_for('showAtrib', nombre = atrib.nombre))
        elif hola == 2:
            if request.method == 'POST' and form.validate():
                tipoDeDato = request.form['tipoDeDato']
                if tipoDeDato == "archivo":
                    arch = request.files['file']
                    MgrTipoDeAtrib().modificar(nombre, request.form['nombre'], 
                    request.form['tipoDeDato'], request.form['descripcion'], 
                    0, arch.filename, arch.read())
                    flash('Se ha modificado correctamente el atributo')
                    return redirect(url_for('listAtrib'))
                elif tipoDeDato == "numerico" or tipoDeDato == "texto":
                    MgrTipoDeAtrib().modificar(nombre, request.form['nombre'], 
                    request.form['tipoDeDato'], request.form['descripcion'],
                    request.form['detalle'], "", None)
                    flash('Se ha modificado correctamente el atributo')
                    return redirect(url_for('listAtrib'))
                elif tipoDeDato == "booleano" or tipoDeDato == "fecha":
                    MgrTipoDeAtrib().modificar(nombre, request.form['nombre'], 
                    request.form['tipoDeDato'],request.form['descripcion'], 
                    0, "", None)
                    flash('Se ha modificado correctamente el atributo')
                    return redirect(url_for('listAtrib'))
    return render_template(app.config['DEFAULT_TPL']+'/editAtrib.html',
                               atrib = MgrTipoDeAtrib().filtrar(nombre),
                               buttons=['numerico', 'texto', 'booleano', 'fecha', 'archivo'], 
                               active_btns=atrib.tipoDeDato,
                               file = atrib.filename,
			       conf = app.config,
 			       form = form)

@app.route('/deleteAtrib/<path:nombre>.html')
def deleteAtrib(nombre):
    if g.user is None:
        return redirect(url_for('login'))   
    else:
        hola = MgrTipoDeAtrib().verificar_borrar(nombre)
        if hola == 1:
            flash('NO se puede eliminar, esta relacionado a un tipo de Item')
        elif hola == 2:
            MgrTipoDeAtrib().borrar(nombre)
            flash('Se ha borrado correctamente')
        return redirect(url_for('listAtrib'))
    
@app.route('/descargar/<path:nombre>.html')
def descargar(nombre):
    if g.user is None:
        return redirect(url_for('login'))   
    else:
        atrib = MgrTipoDeAtrib().filtrar(nombre)
        MgrTipoDeAtrib().descargar(nombre)  
        flash('El archivo se ha descargado satisfactoriamente')
    return redirect(url_for('showAtrib', nombre = atrib.nombre))
    

   