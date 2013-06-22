from modulo import *
from flask import Flask, render_template, request, redirect, url_for, g, \
     session, flash, escape, request
                         
#------------------------------------------------------------------------------#
# MODULO GESTION
#------------------------------------------------------------------------------#

# ADMINISTRAR PROYECTO - INICIAR UN PROYECTO 


@app.route('/initProyecto')
def initProyecto():
    if g.user is None:
        return redirect(url_for('login'))
    else:
        return render_template(app.config['DEFAULT_TPL']+'/initProyecto.html',
                           conf = app.config,
                           list = MgrProyecto().listarPendiente()) 


@app.route('/showInit/<path:nombre>.html', methods=['GET','POST'])
def showInit(nombre):
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
            if request.form.get('rol', None) == "Administrar Rol":
                return redirect(url_for('asignarRol', nombre = project.nombre))
            if request.form.get('usuario', None) == "Administrar Usuario":
                return redirect(url_for('asignarUsuario', nombre = project.nombre))            
            if request.form.get('usuarioAComite', None) == "Administrar Comite":
                return redirect(url_for('asignarUsuarioAComite', nombre = project.nombre))
            if request.form.get('fase', None) == "Administrar Fase":
                return redirect(url_for('asignarFase', nombre = project.nombre))
            if request.form.get('iniciar', None) == "Iniciar":
                return redirect(url_for('iniciarProyecto', nombre = project.nombre))
	return render_template(app.config['DEFAULT_TPL']+'/showInit.html',
			       conf = app.config,
			       form = form,
                               listU = MgrProyecto().usersDeProyecto(nombre),
                               ambito = nombre)

                               
@app.route('/iniciarProyecto/<path:nombre>.html', methods=['GET','POST'])
def iniciarProyecto(nombre):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        if request.method == 'GET':
            proyecto =  MgrProyecto().filtrar(nombre)
            flash(MgrProyecto().iniciarProyecto(proyecto))                        
            return redirect(url_for('asignarFase', nombre = proyecto.nombre)) 
        return render_template(app.config['DEFAULT_TPL']+'/listFasesProyecto.html',
			       conf = app.config,
                               list = MgrProyecto().fasesDeProyecto(nombre),
                               ambito = nombre )       
                       
# ADMINISTRAR PROYECTO - INICIAR UN PROYECTO - ADMINISTRAR FASE

@app.route('/asignarFase/<path:nombre>.html', methods=['GET','POST'])
def asignarFase(nombre):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            proyecto =  MgrProyecto().filtrar(nombre)
            if request.form.get('nuevo', None) == "Nueva Fase por Proyecto":
                return redirect(url_for('addFasePorProyecto', nombre = proyecto.nombre))           
            elif request.form.get('importar', None) =="Importar Fase":
                return redirect(url_for('importarFase', nombre = proyecto.nombre))            
        return render_template(app.config['DEFAULT_TPL']+'/listFasesProyecto.html',
			       conf = app.config,
                               list = MgrProyecto().fasesDeProyecto(nombre),
                               ambito = nombre )
                               
                              
@app.route('/importarFase/<path:nombre>.html', methods=['GET','POST'])
def importarFase(nombre):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        project = MgrProyecto().filtrar(nombre)
        listaFases = request.form.getlist("lista")
	if request.method == 'POST' and listaFases != None:
            for id in listaFases:
                fase = MgrFase().filtrarXId(id)
                flash(MgrProyecto().importarFase(project, fase))

            return redirect(url_for('asignarFase', nombre = project.nombre)) 
    return render_template(app.config['DEFAULT_TPL']+'/importarFase.html',
			       conf = app.config,
                               list = MgrProyecto().fasesDeProyectosPendiente(),
                               ambito = nombre,
                               proyectoId = project.idProyecto
                               )
                               
@app.route('/showFaseProyecto/<path:nombreProyecto>/<path:nombreFase>.html', methods=['GET','POST'])
def showFaseProyecto(nombreProyecto, nombreFase):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        fase = MgrFase().filtrar(nombreFase)
        project = MgrProyecto().filtrarXId(fase.proyectoId)
        tipoDeItem = MgrTipoDeItem().filtrarXId(fase.tipoDeItemId)        
        form = ShowFormFase(request.form, nombre = fase.nombre,
               descripcion = fase.descripcion, 
               fechaDeCreacion = fase.fechaDeCreacion,
               orden = fase.orden,
               estado = fase.estado,
               proyectoId = project,
               tipoDeItemId = tipoDeItem)
        if request.method == 'POST':
            if request.form.get('edit', None) == "Modificar Fase":
                return redirect(url_for('editFase', nombreFase = fase.nombre))
            elif request.form.get('delete', None) == "Eliminar Fase":
                return redirect(url_for('deleteFase', nombreFase = fase.nombre))
            elif request.form.get('state', None) == "Modificar Estado de Fase":
                return redirect(url_for('editFaseState', nombreFase = fase.nombre))
            elif request.form.get('ordenar', None) == "Cambiar Orden de Fase":
                return redirect(url_for('ordenarFase', nombreProyecto = project.nombre, nombreFase = fase.nombre))
	return render_template(app.config['DEFAULT_TPL']+'/showFaseProyecto.html',
			       conf = app.config,
			       form = form, 
                               ambito = nombreProyecto )

@app.route('/ordenarFase/<path:nombreProyecto>/<path:nombreFase>.html', methods=['GET','POST'])
def ordenarFase(nombreProyecto, nombreFase):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        fase = MgrFase().filtrar(nombreFase)
        project = MgrProyecto().filtrarXId(fase.proyectoId)
        faseAux = request.form.get("fase")
	if request.method == 'POST' and  faseAux != None:
            faseNew = MgrFase().filtrar(faseAux)
            flash(MgrProyecto().modificarOrden(nombreProyecto, fase, faseNew))
            return redirect(url_for('asignarFase', nombre = project.nombre)) 
    return render_template(app.config['DEFAULT_TPL']+'/ordenarFase.html',
			       conf = app.config,
                               list = MgrProyecto().fasesDeProyecto(nombreProyecto),
                               nombre = nombreFase)
                               
@app.route('/editFase/<path:nombreFase>.html', methods=['GET','POST'])
def editFase(nombreFase):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        fase = MgrFase().filtrar(nombreFase)
        project = MgrProyecto().filtrarXId(fase.proyectoId)
        form = EditFormFase(request.form, descripcion = fase.descripcion)
        tipoDeItem = request.form.get("tipoDeItem")
	if request.method == 'POST' and form.validate and  tipoDeItem != None:
            tipo = MgrTipoDeItem().filtrar(tipoDeItem)
            flash(MgrFase().modificar(fase, request.form['descripcion'], tipo.idTipoDeItem))
            return redirect(url_for('asignarFase', nombre = project.nombre)) 
    return render_template(app.config['DEFAULT_TPL']+'/editFase.html',
			       conf = app.config,
			       form = form, 
                               tipoDeItemFase = fase.tipoDeItemId,
                               list = MgrTipoDeItem().listar()
                               )


@app.route('/editFaseState/<path:nombreFase>.html', methods=['GET','POST'])
def editFaseState(nombreFase):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        fase = MgrFase().filtrar(nombreFase)
        project = MgrProyecto().filtrarXId(fase.proyectoId)
        form = EditStateFaseForm(request.form, estado = fase.estado)
	if request.method == 'POST' and form.validate(): 
            flash(MgrFase().estado(fase, request.form['estado']))
            return redirect(url_for('asignarFase', nombre = project.nombre)) 
	return render_template(app.config['DEFAULT_TPL']+'/editFaseState.html',
			       conf = app.config,
			       form = EditStateFaseForm())
                               

@app.route('/deleteFase/<path:nombreFase>.html')
def deleteFase(nombreFase):
    if g.user is None:
        return redirect(url_for('login'))   
    else:
        fase = MgrFase().filtrar(nombreFase)
        project = MgrProyecto().filtrarXId(fase.proyectoId)

        flash(MgrProyecto().ordenarFase(project, fase))
        flash(MgrFase().borrar(fase))
        return redirect(url_for('asignarFase', nombre = project.nombre)) 
    
    
@app.route('/addFasePorProyecto/<path:nombre>.html', methods=['GET','POST'])
def addFasePorProyecto(nombre):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            proyecto =  MgrProyecto().filtrar(nombre)
            form = CreateFormFase(request.form, request.form['nombre'], descripcion = request.form['descripcion'])
            tipoDeItem = request.form.get("tipoDeItem")
                      
            if form.validate() and  tipoDeItem != None:
                tipo = MgrTipoDeItem().filtrar(tipoDeItem)
                flash(MgrProyecto().asignarFase(nombre, proyecto.nombre + "-" + request.form['nombre'], 
                                                request.form['descripcion'], MgrProyecto().nroDeFaseDeProyecto(nombre) + 1,
                                                tipo.idTipoDeItem))
                return redirect(url_for('asignarFase', nombre = proyecto.nombre))
            else:
                if tipoDeItem == None:
                    flash('Elegir un tipo de item')
                return render_template(app.config['DEFAULT_TPL']+'/formFase.html',
                            conf = app.config,
                            form = form,
                            list = MgrTipoDeItem().listar()
                            )
    return render_template(app.config['DEFAULT_TPL']+'/formFase.html',
                conf = app.config,
                form = CreateFormFase(),
                list = MgrTipoDeItem().listar())



# ADMINISTRAR PROYECTO - INICIAR UN PROYECTO  - ADMINISTRAR COMITE

@app.route('/asignarUsuarioAComite/<path:nombre>.html', methods=['GET','POST'])
def asignarUsuarioAComite(nombre):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            proyecto =  MgrProyecto().filtrar(nombre)
            if request.form.get('nuevo', None) == "Nuevo Usuario por Comite":
                return redirect(url_for('addUsuarioPorComite', nombre = proyecto.nombre))
        return render_template(app.config['DEFAULT_TPL']+'/listUsuarioComite.html',
			       conf = app.config,
                               list = MgrComite().miembrosComite(nombre),
                               ambito = nombre
                               )

@app.route('/addUsuarioPorComite/<path:nombre>.html', methods=['GET','POST'])
def addUsuarioPorComite(nombre):
    if g.user is None:
        return redirect(url_for('login'))
    else:
     if request.method == 'POST':
        proyecto =  MgrProyecto().filtrar(nombre)
        comite = MgrComite().search(nombre)
        usuario = request.form.get("usuario") 
        if not usuario == None:
            flash(MgrComite().asignarUsuario(nombreProyecto = proyecto.nombre,  nameUser= usuario))
            return render_template(app.config['DEFAULT_TPL']+'/listUsuarioComite.html',
			       conf = app.config,
                               list = MgrComite().miembrosComite(nombre),
                               ambito = nombre
                               )
        else:
            flash(":error: no eligio ningun usuario")
                        
 
    return render_template(app.config['DEFAULT_TPL']+'/asignarUsuarioComite.html',
			       conf = app.config,
                               listU = MgrProyecto().usersDeProyecto(nombre),
                               list = MgrComite().miembrosComite(nombre),
                               ambito = nombre
                               )

@app.route('/showUserComite/<path:nombreProyecto>/<path:nameUser>.html', methods=['GET','POST'])
def showUserComite(nombreProyecto, nameUser):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        user = MgrUser().filtrar(nameUser)
        comite = MgrComite().search(nombreProyecto)
        form = ShowFormUserComite(request.form, name = user.name, password = user.passwd,
               nombre = user.nombre, apellido = user.apellido, 
               email = user.email, telefono = user.telefono,
               obs = user.obs, estado = user.estado, comiteNombre = comite.nombre)   
        if request.method == 'POST':
            if request.form.get('desasignar', None) == "Desasignar Usuario de Comite" :
                return redirect(url_for('desasignarUsuarioDeComite', nombre = nombreProyecto, nameUser = nameUser))
	return render_template(app.config['DEFAULT_TPL']+'/showUserComite.html',
			       conf = app.config,
			       form = form,
                               ambito = nombreProyecto
                               )
@app.route('/desasignarUsuarioDeComite/<path:nombre>/<path:nameUser>.html', methods=['GET','POST'])
def desasignarUsuarioDeComite(nombre, nameUser):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        flash(MgrComite().desasignarUsuario(nombreProyecto = nombre,  nameUser= nameUser))
        return render_template(app.config['DEFAULT_TPL']+'/listUsuarioComite.html',
			       conf = app.config,
                               list = MgrComite().miembrosComite(nombre),
                               ambito = nombre)
                               
# ADMINISTRAR PROYECTO - INICIAR UN PROYECTO  - ADMINISTRAR ROL

@app.route('/asignarRol/<path:nombre>.html', methods=['GET','POST'])
def asignarRol(nombre):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            proyecto =  MgrProyecto().filtrar(nombre)
            if request.form.get('nuevo', None) == "Nuevo Rol por Proyecto":
                return redirect(url_for('addRolPorProyecto', nombre = proyecto.nombre))
        return render_template(app.config['DEFAULT_TPL']+'/listRolesProyecto.html',
			       conf = app.config,
                               list = MgrRol().listarPorAmbito(nombre),
                               nombreProyecto = nombre)

@app.route('/showRolProyecto/<path:nombreProyecto>/<path:nombre>.html', methods=['GET','POST'])
def showRolProyecto(nombre, nombreProyecto):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        rol = MgrRol().search(nombre, nombreProyecto)
        form = CreateFormRolProyecto(request.form, nombre = rol.nombre, 
                                    descripcion = rol.descripcion)
        if request.method == 'POST':
            if request.form.get('edit', None) == "Modificar Rol":
                return redirect(url_for('editRol', nombre = rol.nombre))
            elif request.form.get('config', None) == "Configurar Permisos":
                return redirect(url_for('configPermiso', nombre = rol.nombre))
            elif request.form.get('delete', None) == "Eliminar Rol":
                return redirect(url_for('deleteRol', nombre = rol.nombre))
	return render_template(app.config['DEFAULT_TPL']+'/showRolProyecto.html',
			       conf = app.config,
			       form = form,
                               ambito = nombreProyecto)

@app.route('/addRolPorProyecto/<path:nombre>.html', methods=['GET','POST'])
def addRolPorProyecto(nombre):
    if g.user is None:
        return redirect(url_for('login'))
    else:
	if request.method == 'POST':
            form = CreateFormRolProyecto(request.form, nombre = request.form['nombre'], 
                                          descripcion = request.form['descripcion'])
            if form.validate():
                rol = Rol(nombre = request.form['nombre'],
                        ambito = nombre,
                        descripcion = request.form['descripcion'])    
                
                flash(MgrRol().guardar(rol))
                return redirect(url_for('asignarRol', nombre = nombre)) 
            else:
                return render_template(app.config['DEFAULT_TPL']+'/formRolPorProyecto.html',
			       conf = app.config,
			       form = form)
    return render_template(app.config['DEFAULT_TPL']+'/formRolPorProyecto.html',
			       conf = app.config,
			       form = CreateFormRolProyecto())

# ADMINISTRAR PROYECTO - INICIAR UN PROYECTO  - ADMINISTRAR USUARIO 

@app.route('/asignarUsuario/<path:nombre>.html', methods=['GET','POST'])
def asignarUsuario(nombre):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            proyecto =  MgrProyecto().filtrar(nombre)
            if request.form.get('nuevo', None) == "Asignar Usuario a Proyecto" :
                return redirect(url_for('addUsuarioAProyecto', nombre = proyecto.nombre))
        return render_template(app.config['DEFAULT_TPL']+'/listUsuarioProyecto.html',
			       conf = app.config,
                               list = MgrProyecto().usersDeProyecto(nombre), 
                               ambito = nombre)
 

@app.route('/showUserProyecto/<path:nombreProyecto>/<path:nameUser>.html', methods=['GET','POST'])
def showUserProyecto(nombreProyecto, nameUser):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        user = MgrUser().filtrar(nameUser)
        rol = MgrUser().rolDeUser(nameUser, nombreProyecto)
        form = ShowFormUserProyecto(request.form, name = user.name, password = user.passwd,
               nombre = user.nombre, apellido = user.apellido, 
               email = user.email, telefono = user.telefono,
               obs = user.obs, estado = user.estado, rolNombre = rol.nombre)   
        if request.method == 'POST':
            if request.form.get('desasignar', None) == "Desasignar Usuario de Proyecto":
                return redirect(url_for('desasignarUsuarioDeProyecto', nombre = nombreProyecto, nameUser = nameUser, nombreRol = rol.nombre))
        return render_template(app.config['DEFAULT_TPL']+'/showUserProyecto.html',
			       conf = app.config,
			       form = form,
                               ambito = nombreProyecto
                               )

@app.route('/desasignarUsuarioDeProyecto/<path:nombre>/<path:nameUser>/<path:nombreRol>.html', methods=['GET','POST'])
def desasignarUsuarioDeProyecto(nombre, nameUser, nombreRol):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        proyecto = MgrProyecto().filtrar(nombre)
        user = MgrUser().filtrar(nameUser)
        rol = MgrRol().search(nombreRol, nombre)
        flash(MgrProyecto().desasignarUsuario(nombre = proyecto.nombre,  nameUser = user.name, nombreRol= rol.nombre))
        return redirect(url_for('asignarUsuario', nombre = proyecto.nombre)) 



@app.route('/addUsuarioAProyecto/<path:nombre>.html', methods=['GET','POST'])
def addUsuarioAProyecto(nombre):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            proyecto =  MgrProyecto().filtrar(nombre)
            usuario = request.form.get("usuario") 
            rol = request.form.get("rol")
            if usuario != None and rol != None:
                flash(MgrProyecto().asignarUsuario( nombre = proyecto.nombre,  nameUser = usuario , nombreRol= rol))
                return redirect(url_for('asignarUsuario', nombre = proyecto.nombre)) 
            else:
                if usuario == None:
                    flash(":error: no eligio el usuario")
                if rol == None:
                    flash(":error: no eligio el rol")
                
                return render_template(app.config['DEFAULT_TPL']+'/asignarUsuario.html',
			       conf = app.config,
                               list = MgrProyecto().usersDeProyecto(nombre),
                               listU = MgrUser().listar(),
                               listR = MgrRol().listarPorAmbito(nombre),
                               nombreProyecto = nombre)

    return render_template(app.config['DEFAULT_TPL']+'/asignarUsuario.html',
			       conf = app.config,
                               list = MgrProyecto().usersDeProyecto(nombre),
                               listU = MgrUser().listar(),
                               listR = MgrRol().listarPorAmbito(nombre),
                               nombreProyecto = nombre
                               )




# ADMINISTRAR PROYECTO - FINALIZAR UN PROYECTO 


@app.route('/finProyecto')
def finProyecto():
    if g.user is None:
        return redirect(url_for('login'))
    else:
        return render_template(app.config['DEFAULT_TPL']+'/finProyecto.html',
                           conf = app.config,
                           list = MgrProyecto().listarActivo()) 


@app.route('/showFin/<path:nombre>.html', methods=['GET','POST'])
def showFin(nombre):
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
            flash('falta')
          
	return render_template(app.config['DEFAULT_TPL']+'/showFin.html',
			       conf = app.config,
			       form = form)
 
    