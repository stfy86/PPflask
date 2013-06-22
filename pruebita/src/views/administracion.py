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
              
              
# ADMINISTRAR COMITE


@app.route('/listComite')
def listComite():
    """ Lista los comite del Sistema"""
    if g.user is None:
        return redirect(url_for('login'))
    else:
        return render_template(app.config['DEFAULT_TPL']+'/listComite.html',
                           conf = app.config,
                           list = MgrComite().listar()) 


@app.route('/showComite/<path:nombre>.html', methods=['GET','POST'])
def showComite(nombre):
    """Muestra un Comite"""
    if g.user is None:
        return redirect(url_for('login'))
    else:
        comite = MgrComite().filtrar(nombre)
        form = ShowFormComite(request.form,
               descripcion = comite.descripcion, 
               cantMiembro = comite.cantMiembro,
               proyectoId = comite.proyectoId
               )
        if request.method == 'POST':
            if request.form.get('edit', None) == "Modificar Comite":
                return redirect(url_for('editComite', nombre = comite.nombre))
          
	return render_template(app.config['DEFAULT_TPL']+'/showComite.html',
			       conf = app.config,
			       form = form,
                               nombreComite = nombre)
                               
@app.route('/editComite/<path:nombre>.html', methods=['GET','POST'])
def editComite(nombre):
    """ Modifica un Comite """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        comite = MgrComite().filtrar(nombre)
        form = EditFormComite(request.form,
               descripcion = comite.descripcion,
               cantMiembro = comite.cantMiembro)
	if request.method == 'POST' and form.validate:
            flash(MgrComite().modificar(nombre, request.form['descripcion'], request.form['cantMiembro']))
            return redirect(url_for('listComite'))
    return render_template(app.config['DEFAULT_TPL']+'/editComite.html',
			       conf = app.config,
			       form = form)

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
                            

                      