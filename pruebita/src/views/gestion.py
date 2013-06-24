from modulo import *
from flask import Flask, render_template, request, redirect, url_for, g, \
     session, flash, escape, request
                         
#------------------------------------------------------------------------------#
# MODULO GESTION
#------------------------------------------------------------------------------#

# ADMINISTRAR PROYECTO - INICIAR UN PROYECTO 


@app.route('/listProyectoPendiente')
def listProyectoPendiente():
    """ Muestra los proyectos pendiente del sistema"""
    if g.user is None:
        return redirect(url_for('login'))
    else:
        return render_template(app.config['DEFAULT_TPL']+'/listProyectoPendiente.html',
                           conf = app.config,
                           list = MgrProyecto().listarPendiente()) 


@app.route('/showInit/<path:nombre>.html', methods=['GET','POST'])
def showInit(nombre):
    """ Muestra un proyecto pendiente para el modulo administracion """
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
    """ Inicia un proyecto si es que es posible su inicializacion, es decir tiene al menos una fase con un tipo de item asignado"""
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
    """ Muestra las fases de un proyecto y permite la opcion de agregar fase """
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
            elif request.form.get('adminLB', None) == "Administrar Linea Base":
                return redirect(url_for('listLineaBase', nombre = fase.nombre))
            
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



#------------------------------------------------------------------------------#
# MODULO GESTION
#------------------------------------------------------------------------------#

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
 
    
# inicio Linea Base

@app.route('/listLineaBase/<path:nombre>.html', methods=['GET','POST'])
def listLineaBase(nombre):
    """ Lista editable de proyectos que se alojan en la base de datos"""
    if g.user is None:
        return redirect(url_for('login'))
    else:
        
        if request.method == 'POST':
            fase = MgrFase().filtrar(nombre)
            if request.form.get('add', None) == "Crear Linea Base":
                return redirect(url_for('addLineaBase', nombreFase = fase.nombre))
        
        return render_template(app.config['DEFAULT_TPL']+'/listLineaBase.html',
                           conf = app.config,
                           list = MgrFase().filtrar(nombre).listaLineaBase)


@app.route('/addLineaBase/<path:nombreFase>.html', methods=['GET','POST'])
def addLineaBase(nombreFase):
    """ Agrega una linea Base """  
    if g.user is None:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            form = CreateFormLineaBase(request.form,
                                     request.form['nombre'],
                                     descripcion = request.form['descripcion'],
                                     fase = request.form['fase'])
            if form.validate():
                faseref = MgrFase().filtrar(nombreFase)
                lineaBase = LineaBase(nombre = request.form['nombre'],
                                   descripcion = request.form['descripcion'])
                lineaBase.Fase = faseref
                
                MgrLineaBase().guardar(lineaBase)
                flash('Se ha creado correctamente el linea base')
                
                return redirect(url_for('seleccionarItems', nombre = lineaBase.nombre))
            else:
                return render_template(app.config['DEFAULT_TPL']+'/formLineaBase.html',
                            conf = app.config,
                            form = form)
                
    return render_template(app.config['DEFAULT_TPL']+'/formLineaBase.html',
                conf = app.config,
                form = CreateFormLineaBase())


@app.route('/showLineaBase/<path:nombre>.html', methods=['GET','POST'])
def showLineaBase(nombre):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        lineaBase = MgrLineaBase().filtrar(nombre)
        form = ShowFormLineaBase(request.form, nombre = lineaBase.nombre,
                    descripcion = lineaBase.descripcion,
                    estado = lineaBase.estado)
        if request.method == 'POST':
            if request.form.get('edit', None) == "Modificar Linea Base":
                return redirect(url_for('editLineaBase', nombre = lineaBase.nombre))
            elif request.form.get('listLineaBaseItems', None) == "Listar Items":
                return redirect(url_for('listLineaBaseItems', nombre = lineaBase.nombre))
            elif request.form.get('delete', None) == "Eliminar Linea Base":
                return redirect(url_for('deleteLineaBase', nombre = lineaBase.nombre))
# return redirect(url_for('deleteLineaBase', nombre = rol.nombre))
            elif request.form.get('editState', None) == "Modificar estado de Linea Base":
                return redirect(url_for('editStateLineaBase', nombre = lineaBase.nombre))
        return render_template(app.config['DEFAULT_TPL']+'/showLineaBase.html',
                conf = app.config,
                form = form)


@app.route('/editLineaBase/<path:nombre>.html', methods=['GET','POST'])
def editLineaBase(nombre):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        lineaBase = MgrLineaBase().filtrar(nombre)
        form = EditFormLineaBase(request.form, nombre = lineaBase.nombre,
                    descripcion = lineaBase.descripcion)
        if request.method == 'POST' and form.validate():
            MgrLineaBase().modificar(nombre, request.form['nombre'], request.form['descripcion'])
            flash('Se ha modificado correctamente el rol')
            return redirect(url_for('listLineaBase'))
    return render_template(app.config['DEFAULT_TPL']+'/editLineaBase.html',
                            conf = app.config,
                            form = form)


@app.route('/editStateLineaBase/<path:nombre>.html', methods=['GET','POST'])
def editStateLineaBase(nombre):
    """ Modifica el estado de un usuario """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        lineaBase = MgrLineaBase().filtrar(nombre)
        form = EditFormStateLineaBase(request.form, estado = lineaBase.estado)
        if request.method == 'POST' and form.validate():
            MgrLineaBase().estado(nombre, request.form['estado'])
            return redirect(url_for('listLineaBase'))
    return render_template(app.config['DEFAULT_TPL']+'/editStateLineaBase.html',
                            conf = app.config,
                            form = EditFormStateLineaBase())


@app.route('/deleteLineaBase/<path:nombre>.html')
def deleteLineaBase(nombre):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        lineaBase=MgrLineaBase().filtrar(nombre)
        MgrLineaBase().desAsignarItems(nombre)
        
        MgrLineaBase().borrar(nombre)
        flash('Se ha borrado correctamente')
        return redirect(url_for('listLineaBase'))


@app.route('/seleccionarItems/<path:nombre>.html', methods=['GET','POST'])
def seleccionarItems(nombre):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        lista = request.form.getlist("lista")
        
        lineaBase = MgrLineaBase().filtrar(nombre)
        if request.method == 'POST':
            MgrLineaBase().asignarItems(nombre, lista)
            flash('Se ha configurado correctamente los permisos')
            return redirect(url_for('listLineaBase', nombre = lineaBase.Fase.nombre))
        
        lineaBase = MgrLineaBase().filtrar(nombre)
        fase = MgrFase().filtrar(lineaBase.Fase.nombre)
        itemsFase = MgrItem().filtrarAprobadoXFase(fase.idFase)

        lineasBases = fase.listaLineaBase
        itemsLineaBase = []
        for lb in lineasBases:
            itemsLineaBase.extend(lb.itemsLB)
            
        seleccion = []
        for item in itemsFase:
            if not (item in itemsLineaBase):
                seleccion.append(item)

    
        return render_template(app.config['DEFAULT_TPL']+'/seleccionarItems.html',
                                conf = app.config,
                                list = seleccion)


@app.route('/listLineaBaseItems/<path:nombre>.html', methods=['GET','POST'])
def listLineaBaseItems(nombre):
    """ Lista los datos de un tipo de item """
    if g.user is None:
        return redirect(url_for('login'))
    lineaBase = MgrLineaBase().filtrar(nombre)
    return render_template(app.config['DEFAULT_TPL']+'/listLineaBaseItems.html',
                           conf = app.config,
                           list = lineaBase.itemsLB)

# fin Linea Base

#Solicitud inicio

@app.route('/showSolicitud/<path:nombre>.html', methods=['GET','POST'])
def showSolicitud(nombre):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        solicitud = MgrSolicitud().filtrar(nombre)
        form = ShowFormSolicitud(request.form, nombre = solicitud.nombre,
                    descripcion = solicitud.descripcion,
                    estado = solicitud.estado)
        if request.method == 'POST':
            if request.form.get('edit', None) == "Modificar Solicitud":
                return redirect(url_for('editSolicitud', nombre = solicitud.nombre))
            elif request.form.get('listSolicitudItems', None) == "Listar Items":
                return redirect(url_for('listSolicitudItems', nombre = solicitud.nombre))
            elif request.form.get('votarAprobar', None) == "Aprobar":
                solicitud.votosPositivos = solicitud.votosPositivos+1
                db.session.commit()
                return redirect(url_for('showSolicitud', nombre = solicitud.nombre))
            elif request.form.get('votarDenegar', None) == "Denegar":
                solicitud.votosNegativos = solicitud.votosNegativos+1
                db.session.commit()
                return redirect(url_for('showSolicitud', nombre = solicitud.nombre))
        return render_template(app.config['DEFAULT_TPL']+'/showSolicitud.html',
                            conf = app.config,
                            form = form)


@app.route('/listSolicitudItems/<path:nombre>.html', methods=['GET','POST'])
def listSolicitudItems(nombre):
    """ Lista los datos de un tipo de item """
    if g.user is None:
        return redirect(url_for('login'))
    solicitud = MgrSolicitud().filtrar(nombre)
    return render_template(app.config['DEFAULT_TPL']+'/listLineaBaseItems.html',
                           conf = app.config,
                           list = solicitud.itemsSolicitud)

#Solicitud fin    



# ADMINISTRAR ROL Y PERMISO

@app.route('/editRol/<path:nombre>.html', methods=['GET','POST'])
def editRol(nombre):
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
            if request.form.get('config', None) == "Configurar Permisos":
                return redirect(url_for('configPermiso', nombre = rol.nombre))
            flash('Se ha modificado correctamente el rol')
            return redirect(url_for('listRolPermiso'))
    return render_template(app.config['DEFAULT_TPL']+'/editRol.html',
			       conf = app.config,
			       form = form)
                               
@app.route('/configPermiso/<path:nombre>.html', methods=['GET','POST'])
def configPermiso(nombre):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        lista = request.form.getlist("lista")
        permisos2 = MgrRol().filtrarPermiso(nombre)
        rol = MgrRol().filtrar(nombre)
        if request.method == 'POST':
            for perm in lista:
                if perm in permisos2:
                        lista.remove(perm)
            for perm in permisos2:
                if perm in lista:
                        permisos2.remove(perm)
            MgrRol().asignarPermiso2(nombre, lista, permisos2) 
            flash('Se ha configurado correctamente los permisos')
            return redirect(url_for('editRol', nombre = rol.nombre))
        return render_template(app.config['DEFAULT_TPL']+'/configPermiso.html',
			       conf = app.config,
                               permisos = MgrRol().filtrarPermiso(nombre),
                               list = MgrPermiso().listar())

