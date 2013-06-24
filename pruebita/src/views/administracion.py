from modulo import *
from flask import Flask, render_template, request, redirect, url_for, g, \
     session, flash, escape, request
     
                           
#------------------------------------------------------------------------------#
# MODULO ADMINISTRACION
#------------------------------------------------------------------------------#


# ADMINISTRAR PROYECTO


@app.route('/listProject')
def listProject():   
    """ Lista los Proyectos Pendientes y Finalizados """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        return render_template(app.config['DEFAULT_TPL']+'/listProject.html',
                           conf = app.config,
                           list = MgrProyecto().listarPendienteYFinalizado()) 


@app.route('/showProjectPendiente/<path:nombre>.html', methods=['GET','POST'])
def showProjectPendiente(nombre):
    """ Muestra un proyecto con estado pendiente """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        project = MgrProyecto().filtrar(nombre)
        form = ShowFormProject(request.form, nombre = project.nombre,
               descripcion = project.descripcion, 
               fechaDeCreacion = project.fechaDeCreacion,
               estado = project.estado,
               presupuesto = project.presupuesto)
        if request.method == 'POST':
            if request.form.get('edit', None) == "Modificar Proyecto":
                return redirect(url_for('editProject', nombre = project.nombre))
            elif request.form.get('editState', None) == "Modificar Estado de Proyecto":
                return redirect(url_for('editProjectStateAdmin', nombre = project.nombre)) 
            elif request.form.get('delete', None) == "Eliminar Proyecto":
                return redirect(url_for('deleteProject', nombre = project.nombre))
            elif request.form.get('listRolProyecto', None) == "Ver Rol de Proyecto":
                return redirect(url_for('listRolProyecto', nombre = project.nombre))
            elif request.form.get('listComiteProyecto', None) == "Ver Comite de Proyecto":
                return redirect(url_for('listComiteProyecto', nombre = project.nombre))
            
	return render_template(app.config['DEFAULT_TPL']+'/showProjectPendiente.html',
			       conf = app.config,
			       form = form)
                               
@app.route('/editProject/<path:nombre>.html', methods=['GET','POST'])
def editProject(nombre):
    """ Modifica un proyecto """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        project = MgrProyecto().filtrar(nombre)
        form = EditFormProject(request.form,
               descripcion = project.descripcion,
               presupuesto = project.presupuesto)
	if request.method == 'POST' and form.validate:
            flash(MgrProyecto().modificar(nombre, request.form['descripcion'], request.form['presupuesto']))
            return redirect(url_for('listProject'))
    return render_template(app.config['DEFAULT_TPL']+'/editProject.html',
			       conf = app.config,
			       form = form)

@app.route('/editProjectStateAdmin/<path:nombre>.html', methods=['GET','POST'])
def editProjectStateAdmin(nombre):
    """ Modifica el estado del Proyecto """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        proyecto = MgrProyecto().filtrar(nombre)
        form = EditStateProjectAdminForm(request.form, estado = proyecto.estado)
	if request.method == 'POST' and form.validate(): 
                flash (MgrProyecto().estado(nombre, request.form['estado']))
		return redirect(url_for('listProject'))
	return render_template(app.config['DEFAULT_TPL']+'/editProjectState.html',
			       conf = app.config,
			       form = EditStateProjectAdminForm())
                               
@app.route('/addProject', methods=['GET','POST'])
def addProject():
    """ Guarda un Proyecto """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        list = MgrUser().listar()
        if request.method == 'POST':
            form = CreateFormProject(request.form, 
                                     request.form['nombre'], 
                                     descripcion = request.form['descripcion'],
                                     presupuesto = request.form['presupuesto'])
            if form.validate():
                lista = request.form.get("lista")
                p = Proyecto(nombre = request.form['nombre'], 
                                   descripcion = request.form['descripcion'],
                                   presupuesto = request.form['presupuesto']) 
                MgrProyecto().guardar(p)
                r = Rol(nombre="LiderDeProyecto", descripcion="rol de lider", ambito= p.nombre)
                MgrRol().guardar(r)
                flash(MgrProyecto().asignarLider(proyecto = p , rol = r, nameLider = lista))
                return redirect(url_for('addComite', nombre = p.nombre, nameLider = lista ))
            else:
                return render_template(app.config['DEFAULT_TPL']+'/formProject.html',
                            conf = app.config,
                            form = form,
                            list = MgrUser().listar())
                
    return render_template(app.config['DEFAULT_TPL']+'/formProject.html',
                conf = app.config,
                form = CreateFormProject(),
                list = MgrUser().listar())

@app.route('/deleteProject/<path:nombre>.html')
def deleteProject(nombre):
    """ Elimina un proyecto """
    if g.user is None:
        return redirect(url_for('login'))   
    else:  
        project = MgrProyecto().filtrar(nombre)
        flash(MgrProyecto().borrar(project))
        return redirect(url_for('listProject'))
              
     
#------------------------------------------------------------------------------#
# MODULO ADMINISTRACION
#------------------------------------------------------------------------------#


# ADMINISTRAR COMITE


@app.route('/listComiteProyecto/<path:nombre>.html', methods=['GET','POST'])
def listComiteProyecto(nombre):
    """ Lista los comite del Sistema"""
    if g.user is None:
        return redirect(url_for('login'))
    else:
        return render_template(app.config['DEFAULT_TPL']+'/listComiteProyecto.html',
                           conf = app.config,
                           list = MgrComite().listarPorProyecto(nombre),
                           nombreProyecto = nombre) 


@app.route('/showComite/<path:nombreProyecto>/<path:idComite>.html', methods=['GET','POST'])
def showComite(nombreProyecto, idComite):
    """Muestra un Comite"""
    if g.user is None:
        return redirect(url_for('login'))
    else:
        comite = MgrComite().filtrarXId(idComite)
        proyecto = MgrProyecto().filtrarXId(comite.proyectoId)
        form = ShowFormComite(request.form,
               descripcion = comite.descripcion, 
               cantMiembro = comite.cantMiembro,
               proyectoId = comite.proyectoId
               )
        if request.method == 'POST':
            if request.form.get('edit', None) == "Modificar Comite":
                return redirect(url_for('editComite', nombreProyecto = nombreProyecto, idComite = idComite))
          
	return render_template(app.config['DEFAULT_TPL']+'/showComite.html',
			       conf = app.config,
			       form = form,
                               idComite = idComite,
                               nombreProyecto = nombreProyecto)
                               
@app.route('/editComite/<path:nombreProyecto>/<path:idComite>.html', methods=['GET','POST'])
def editComite(nombreProyecto, idComite):
    """ Modifica un Comite """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        comite = MgrComite().filtrarXId(idComite)
        proyecto = MgrProyecto().filtrarXId(comite.proyectoId)
        form = EditFormComite(request.form,
               descripcion = comite.descripcion,
               cantMiembro = comite.cantMiembro)
	if request.method == 'POST' and form.validate:
            flash(MgrComite().modificar(comite, request.form['descripcion'], request.form['cantMiembro']))
            return redirect(url_for('listComiteProyecto', nombre = nombreProyecto))
    return render_template(app.config['DEFAULT_TPL']+'/editComite.html',
			       conf = app.config,
			       form = form,
                               idComite = idComite,
                               nombreProyecto = nombreProyecto)

@app.route('/addComite/<path:nameLider>/<path:nombre>.html', methods=['GET','POST'])
def addComite(nombre, nameLider):
    """Guarda un comite y asigna al lider del proyecto como usuario del comite"""
    if g.user is None:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            form = CreateFormComite(request.form, 
                                     request.form['nombre'], 
                                     descripcion = request.form['descripcion'],
                                     cantMiembro = request.form['cantMiembro'])
            if form.validate():
                u = MgrUser().filtrar(nameLider)
                p = MgrProyecto().filtrar(nombre)
                c = Comite(nombre = request.form['nombre']+"-"+nombre , 
                            descripcion = request.form['descripcion'],
                            cantMiembro = request.form['cantMiembro'],
                            proyectoId = p.idProyecto)    
                MgrComite().guardar(c)
                MgrComite().asignarUsuario(nombreProyecto = p.nombre,  nameUser= u.name)  
                flash('Se ha creado correctamente el comite')
                return redirect(url_for('listProject'))
            else:
                return render_template(app.config['DEFAULT_TPL']+'/formComite.html',
                            conf = app.config,
                            form = form)
                
    return render_template(app.config['DEFAULT_TPL']+'/formComite.html',
                conf = app.config,
                form = CreateFormComite())
    
                      
                      
     
#------------------------------------------------------------------------------#
# MODULO ADMINISTRACION
#------------------------------------------------------------------------------#

# ADMINISTRAR USUARIO


@app.route('/listUser')
def listUser():   
    """ Lista Usuarios Activos del Sistema """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        return render_template(app.config['DEFAULT_TPL']+'/listUser.html',
                           conf = app.config,
                           list = MgrUser().listarActivo()) 


@app.route('/showUser/<path:nombre>.html', methods=['GET','POST'])
def showUser(nombre):
    """ Muestra un usuario"""
    if g.user is None:
        return redirect(url_for('login'))
    else:
        user = MgrUser().filtrar(nombre)
        form = ShowFormUser(request.form, name = user.name,
                            nombre = user.nombre, apellido = user.apellido,
                            email = user.email, telefono = user.telefono, obs = user.obs,
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
                             
@app.route('/addUser', methods=['GET','POST'])
def addUser():
    """ Guarda un Usuario """
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
                rol = MgrRol().search("Invitado", "none project")
                MgrUser().addRol(user.name, rol)
                flash('Se ha creado correctamente el usuario')
                return redirect(url_for('listUser'))
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

                           
#------------------------------------------------------------------------------#
# MODULO ADMINISTRACION
#------------------------------------------------------------------------------#


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
    
    
                           
#------------------------------------------------------------------------------#
# MODULO ADMINISTRACION
#------------------------------------------------------------------------------#

# ADMINISTRACION DE ROLES Y PERMISOS

@app.route('/listRolProyecto/<path:nombre>.html', methods=['GET','POST'])
def listRolProyecto(nombre):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            proyecto =  MgrProyecto().filtrar(nombre)
            if request.form.get('nuevo', None) == "Nuevo Rol por Proyecto":
                return redirect(url_for('addRolPorProyecto', nombreProyecto = nombre))
        return render_template(app.config['DEFAULT_TPL']+'/listRolesProyecto.html',
			       conf = app.config,
                               list = MgrRol().listarPorAmbito(nombre),
                               nombreProyecto = nombre)


@app.route('/showRolProyecto/<path:nombreProyecto>/<path:nombre>.html', methods=['GET','POST'])
def showRolProyecto(nombreProyecto, nombre):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        rol = MgrRol().search(nombre, nombreProyecto)
        form = CreateFormRolProyecto(request.form, nombre = rol.nombre, 
                                    descripcion = rol.descripcion)
        if request.method == 'POST':
            if request.form.get('edit', None) == "Modificar Rol":
                return redirect(url_for('editRol', idRol = rol.idRol))
            elif request.form.get('config', None) == "Configurar Permisos":
                return redirect(url_for('configPermiso',  idRol = rol.idRol))
            elif request.form.get('delete', None) == "Eliminar Rol":
                return redirect(url_for('deleteRol',  idRol = rol.idRol))
	return render_template(app.config['DEFAULT_TPL']+'/showRolProyecto.html',
			       conf = app.config,
			       form = form,
                               ambito = nombreProyecto)

    