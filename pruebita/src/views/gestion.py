from modulo import *
from flask import Flask, render_template, request, redirect, url_for, g, \
     session, flash, escape, request


@app.route('/listProjectP')
def listProjectP():   
    """ Lista los Proyectos Pendientes """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        return render_template(app.config['DEFAULT_TPL']+'/listProjectP.html',
                           conf = app.config,
                           list = MgrProyecto().listarPendiente()) 



@app.route('/listSolicitudesG', methods=['GET', 'POST'])
def listSolicitudesG():
    if g.user is None:
        return redirect(url_for('login'))
    else:
        return render_template(app.config['DEFAULT_TPL'] + '/listSolicitudesG.html',
                               conf=app.config,
                               list=MgrSolicitud().listar()
                               )
#------------------------------------------------------------------------------#
# MODULO GESTION
#------------------------------------------------------------------------------#
# GESTIONAR FASES DE UN PROYECTO by Stfy
#------------------------------------------------------------------------------#

@app.route('/gesProyecto', methods=['GET','POST'])
def gesProyecto():
    if g.user is None:
        return redirect(url_for('login'))
    else:
        project = MgrProyecto().filtrarXId(g.proyecto.idProyecto)
        form = ShowFormProject(request.form, nombre = project.nombre,
               descripcion = project.descripcion, 
               fechaDeCreacion = project.fechaDeCreacion,
               estado = project.estado,
               presupuesto = project.presupuesto)
        return render_template(app.config['DEFAULT_TPL']+'/gesProyecto.html',
			       conf = app.config,
			       form = form,
                               proyecto = g.proyecto
                               )
            
@app.route('/initProject/<path:idProyecto>.html')
def initProject(idProyecto):
    """ Inicia un proyecto """
    if g.user is None:
        return redirect(url_for('login'))   
    else:  
        project = MgrProyecto().filtrarXId(idProyecto)
        flash(MgrProyecto().iniciarProyecto(project))
        return redirect(url_for('gesProyecto'))
            
@app.route('/finProject/<path:idProyecto>.html')
def finProject(idProyecto):
    """ Finaliza un proyecto """
    if g.user is None:
        return redirect(url_for('login'))   
    else:  
        project = MgrProyecto().filtrarXId(idProyecto)
        flash(MgrProyecto().finalizarProyecto(project))
        return redirect(url_for('gesProyecto'))                        
    
@app.route('/reporteProject/<path:idProyecto>.html')
def reporteProject(idProyecto):   
    if g.user is None:
        return redirect(url_for('login'))
    else:
        import cStringIO
        buff = cStringIO.StringIO()
        doc = SimpleDocTemplate(buff, pagesize=A4, showBoundary=1)
        project = MgrProyecto().filtrarXId(idProyecto)
        story = MgrReporte().generarReporteProyecto(project)
        doc.build(story)        
        response = make_response(buff.getvalue())
        response.headers['Content-Disposition'] = "attachment; filename='reporteProyecto.pdf"
        response.mimetype = 'application/pdf'        
        buff.close()
        return response
    
@app.route('/reporteFaseProject/<path:idProyecto>.html')
def reporteFaseProject(idProyecto):   
    if g.user is None:
        return redirect(url_for('login'))
    else:
        import cStringIO
        buff = cStringIO.StringIO()
        doc = SimpleDocTemplate(buff, pagesize=A4, showBoundary=1)
        project = MgrProyecto().filtrarXId(idProyecto)
        story = MgrReporte().generarReporteFase(project)
        doc.build(story)        
        response = make_response(buff.getvalue())
        response.headers['Content-Disposition'] = "attachment; filename='reporteFaseDeProyecto.pdf"
        response.mimetype = 'application/pdf'        
        buff.close()
        return response

@app.route('/costoProyecto/<path:proyecto>.html', methods=['GET','POST'])
def costoProyecto(proyecto):
    if g.user is None:
        return redirect(url_for('login'))   
    else:
        list = MgrProyecto().listarItemProyecto(proyecto)   
        costo = MgrProyecto().costoProyecto(list)
        flash("El costo total del proyecto es: " + costo)
        return render_template(app.config['DEFAULT_TPL']+'/costoProyecto.html',
                           conf = app.config,
                           costo = costo,
                           list = list) 
             
@app.route('/impactoProyecto/<path:proyecto>.html', methods=['GET','POST'])
def impactoProyecto(proyecto):
    if g.user is None:
        return redirect(url_for('login'))   
    else:
        list = MgrProyecto().listarItemProyecto(proyecto)   
        impacto = MgrProyecto().impactoProyecto(list)
        flash("El impacto total del proyecto es: " + impacto)
        return render_template(app.config['DEFAULT_TPL']+'/costoProyecto.html',
                           conf = app.config,
                           impacto = impacto,
                           list = list) 
#------------------------------------------------------------------------------#
# MODULO GESTION
#------------------------------------------------------------------------------#
# GESTIONAR FASES DE UN PROYECTO by Stfy
#------------------------------------------------------------------------------#

@app.route('/listFases', methods=['GET','POST'])
def listFases():
    """ Muestra las fases de un proyecto y permite la opcion de agregar fase e importar de otro proyecto"""
    if g.user is None:
        return redirect(url_for('login'))
    else:        
        return render_template(app.config['DEFAULT_TPL']+'/listFases.html',
			       conf = app.config,
                               list = MgrProyecto().fasesDeProyecto(g.proyecto.nombre))

@app.route('/addFase', methods=['GET','POST'])
def addFase():
    if g.user is None:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            nombre = g.proyecto.nombre
            proyecto =  MgrProyecto().filtrar(nombre)
            form = CreateFormFase(request.form, request.form['nombre'], descripcion = request.form['descripcion'])
            tipoDeItem = request.form.get("tipoDeItem")                 
            if form.validate() and  tipoDeItem != None:
                tipo = MgrTipoDeItem().filtrar(tipoDeItem)
                flash(MgrProyecto().asignarFase(nombre, proyecto.nombre + "-" + request.form['nombre'], 
                                                request.form['descripcion'], MgrProyecto().nroDeFaseDeProyecto(nombre) + 1,
                                                tipo.idTipoDeItem))
                return redirect(url_for('listFases'))
            else:
                return render_template(app.config['DEFAULT_TPL']+'/formFase.html',
                            conf = app.config,
                            form = form,
                            list = MgrTipoDeItem().listar()
                            )
    return render_template(app.config['DEFAULT_TPL']+'/formFase.html',
                conf = app.config,
                form = CreateFormFase(),
                list = MgrTipoDeItem().listar())


@app.route('/importarFase', methods=['GET','POST'])
def importarFase():
    if g.user is None:
        return redirect(url_for('login'))
    else:
        nombre = g.proyecto.nombre
        project = MgrProyecto().filtrar(nombre)
        listaFases = request.form.getlist("lista")
	if request.method == 'POST' and listaFases != None:
            for id in listaFases:
                fase = MgrFase().filtrarXId(id)
                flash(MgrProyecto().importarFase(project, fase))
            return redirect(url_for('listFases')) 
        else:
            return render_template(app.config['DEFAULT_TPL']+'/importarFase.html',
			       conf = app.config,
                               list = MgrProyecto().fasesDeProyectosPendiente(),
                               proyectoId = project.idProyecto
                               )
                               
@app.route('/showFase/<path:idFase>.html', methods=['GET','POST'])
def showFase(idFase):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        fase = MgrFase().filtrarXId(idFase)
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
                return redirect(url_for('editFase', idFase = fase.idFase))
            elif request.form.get('delete', None) == "Eliminar Fase":
                return redirect(url_for('deleteFase', idFase = fase.idFase))
            elif request.form.get('state', None) == "Modificar Estado de Fase":
                return redirect(url_for('editFaseState', idFase = fase.idFase))
            elif request.form.get('ordenar', None) == "Cambiar Orden de Fase":
                return redirect(url_for('ordenarFase', idFase = fase.idFase))
            elif request.form.get('gesLB', None) == "Ver Linea Base":
                return redirect(url_for('gesLB', idFase = fase.idFase))
            elif request.form.get('initFase', None) == "Iniciar Fase":
                return redirect(url_for('initFase', idFase = fase.idFase))
            elif request.form.get('finFase', None) == "Finalizar Fase":
                return redirect(url_for('finFase', idFase = fase.idFase))
            elif request.form.get('items', None) == "Ver Items":
                return redirect(url_for('listItemG', idFase = fase.idFase))
                        
	return render_template(app.config['DEFAULT_TPL']+'/showFase.html',
			       conf = app.config,
			       form = form,
                               fase = fase)
                               
@app.route('/listItemG/<path:idFase>.html')
def listItemG(idFase):
    """ Lista los datos de un item """
    if g.user is None:
        return redirect(url_for('login'))   
    list = MgrFase().filtrarItemsId(idFase)
    return render_template(app.config['DEFAULT_TPL']+'/listItemG.html',
                           conf = app.config,
                           id = idFase,
                           list = list) 
                                                              
@app.route('/ordenarFase/<path:idFase>.html', methods=['GET','POST'])
def ordenarFase(idFase):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        nombreProyecto = g.proyecto.nombre
        fase = MgrFase().filtrarXId(idFase)
        project = MgrProyecto().filtrarXId(fase.proyectoId)
        idFaseAux = request.form.get("fase")
	if request.method == 'POST' and  idFaseAux != None:
            faseNew = MgrFase().filtrarXId(idFaseAux)
            flash(MgrProyecto().modificarOrden(project, fase, faseNew))
            return redirect(url_for('listFases')) 
    return render_template(app.config['DEFAULT_TPL']+'/ordenarFase.html',
			       conf = app.config,
                               list = MgrProyecto().fasesDeProyecto(nombreProyecto),
                               nombre = fase.nombre,
                               idFase = fase.idFase)
                               
@app.route('/editFase/<path:idFase>.html', methods=['GET','POST'])
def editFase(idFase):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        fase = MgrFase().filtrarXId(idFase)
        project = MgrProyecto().filtrarXId(fase.proyectoId)
        tipoDeItem = MgrTipoDeItem().filtrarXId(fase.tipoDeItemId)        
        form = EditFormFase(request.form, nombre = fase.nombre, tipoDeItem = tipoDeItem.nombre,descripcion = fase.descripcion)
        idTipoDeItem = request.form.get("tipoDeItem")
	if request.method == 'POST' and form.validate() and  idTipoDeItem != None:
            tipo = MgrTipoDeItem().filtrarXId(idTipoDeItem)
            flash(MgrFase().modificar(fase, request.form['descripcion'], tipo.idTipoDeItem))
            return redirect(url_for('showFase', idFase = fase.idFase)) 
    return render_template(app.config['DEFAULT_TPL']+'/editFase.html',
			       conf = app.config,
			       form = form, 
                               tipoDeItemFase = fase.tipoDeItemId,
                               list = MgrTipoDeItem().listar(),
                               idFase = fase.idFase,
                               nombreFase = fase.nombre
                               )


@app.route('/editFaseState/<path:idFase>.html', methods=['GET','POST'])
def editFaseState(idFase):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        fase = MgrFase().filtrarXId(idFase)
        project = MgrProyecto().filtrarXId(fase.proyectoId)
        if request.method == 'POST': 
            flash(MgrFase().estado(fase, request.form['estado']))
            return redirect(url_for('showFase', idFase = fase.idFase)) 
	return render_template(app.config['DEFAULT_TPL']+'/editFaseState.html',
			       conf = app.config,
			       fase = fase,
                               idFase = idFase,
                               buttons=['Pendiente', 'Activo', 'Finalizado'])
                               

@app.route('/deleteFase/<path:idFase>.html')
def deleteFase(idFase):
    if g.user is None:
        return redirect(url_for('login'))   
    else:
        fase = MgrFase().filtrarXId(idFase)
        project = MgrProyecto().filtrarXId(fase.proyectoId)
        flash(MgrProyecto().ordenarFase(project, fase))
        flash(MgrFase().borrar(fase))
        return redirect(url_for('listFases')) 
    
@app.route('/initFase/<path:idFase>.html')
def initFase(idFase):
    """ Iniciar una fase implica cambiar de Pendiente a Activo"""
    if g.user is None:
        return redirect(url_for('login'))   
    else:
        fase = MgrFase().filtrarXId(idFase)       
        flash(MgrFase().estado(fase,"Activo"))
        flash(":Inicio la Fase - ya puede agregar items a la fase:")        
        return redirect(url_for('listFases')) 
    
@app.route('/finFase/<path:idFase>.html')
def finFase(idFase):
    if g.user is None:
        return redirect(url_for('login'))   
    else:
        fase = MgrFase().filtrarXId(idFase)
        if MgrFase().itemsAprobados(fase):
            flash(MgrFase().estado(fase,"Finalizado"))
            flash(":Finalizo Fase: todos los Items de la fase estan dentro de una Linea Base:")        
        else:
            flash(":NO Finalizo Fase:")        
        return redirect(url_for('listFases')) 
        
# FIN DE GESTIONAR FASE by Stfy

#------------------------------------------------------------------------------#
# MODULO GESTION
#------------------------------------------------------------------------------#
# GESTIONAR ROL DE PROYECTO Y PERMISO by Stfy
#------------------------------------------------------------------------------#
@app.route('/listRolProyecto', methods=['GET','POST'])
def listRolProyecto():
    """ Lista los roles de un proyecto """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        return render_template(app.config['DEFAULT_TPL']+'/listRolProyecto.html',
			       conf = app.config,
                               list = MgrRol().listarPorAmbito(g.proyecto.nombre),
                               )


@app.route('/showRolProyecto/<path:idRol>.html', methods=['GET','POST'])
def showRolProyecto(idRol):
    """Muestra un Rol especifico de un proyecto"""
    if g.user is None:
        return redirect(url_for('login'))
    else:
        rol = MgrRol().filtrarXId(idRol)
        form = CreateFormRolProyecto(request.form, nombre = rol.nombre, ambito=rol.ambito, descripcion = rol.descripcion)
        if request.method == 'POST':
            if request.form.get('edit', None) == "Modificar Rol":
                return redirect(url_for('editRolProyecto', idRol = rol.idRol))
            elif request.form.get('delete', None) == "Eliminar Rol":
                return redirect(url_for('deleteRolProyecto',  idRol = rol.idRol))
	return render_template(app.config['DEFAULT_TPL']+'/showRolProyecto.html',
			       conf = app.config,
			       form = form,
                               list = MgrRol().listarPermisos(idRol))

@app.route('/editRolProyecto/<path:idRol>.html', methods=['GET','POST'])
def editRolProyecto(idRol):
    """ Edita los datos de un Rol de proyecto y permite configurar los permisos del rol """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        rol = MgrRol().filtrarXId(idRol)
        form = CreateFormRolProyecto(request.form, nombre = rol.nombre, ambito = rol.ambito, descripcion = rol.descripcion)
        list = request.form.getlist("lista")
	if request.method == 'POST' and form.validate() and list:
            perm = MgrPermiso().getlistaPermiso(list)
            #flash(list)
            flash(MgrRol().modificar(rol, request.form['nombre'],request.form['ambito'], request.form['descripcion'],perm))
            return redirect(url_for('showRolProyecto', idRol = rol.idRol))
        elif not list:
            flash("no eligio ningun permiso")
            return render_template(app.config['DEFAULT_TPL']+'/editRolProyecto.html',
			       conf = app.config,
			       form = form,
                               idRol =rol.idRol,
                               listT = MgrPermiso().listar())
    
            
    return render_template(app.config['DEFAULT_TPL']+'/editRolProyecto.html',
			       conf = app.config,
			       form = form,
                               idRol =rol.idRol,
                               listT = MgrPermiso().listar())
                               

@app.route('/addRolProyecto', methods=['GET','POST'])
def addRolProyecto():
    """Agrega un rol al proyecto"""
    if g.user is None:
        return redirect(url_for('login'))
    else:
	if request.method == 'POST':
            list = request.form.getlist("lista")
            form = CreateFormRolProyecto(request.form, nombre = request.form['nombre'], descripcion = request.form['descripcion'])
            if form.validate() and list: 
                perm = MgrPermiso().getlistaPermiso(list)
                rol = Rol(nombre = request.form['nombre'], ambito = g.proyecto.nombre, descripcion = request.form['descripcion'], permisos = perm) 
                flash(MgrRol().guardar(rol))
                return redirect(url_for('listRolProyecto')) 
                   
            elif not list:
                flash("no eligio ningun permiso")
                return render_template(app.config['DEFAULT_TPL']+'/formRolProyecto.html',
			       conf = app.config,
			       form = form,
                               list = MgrPermiso().listar()                      
                               )
            else:
                return render_template(app.config['DEFAULT_TPL']+'/formRolProyecto.html',
			       conf = app.config,
			       form = form,
                               list = MgrPermiso().listar()                      
                               )
    return render_template(app.config['DEFAULT_TPL']+'/formRolProyecto.html',
			       conf = app.config,
			       form = CreateFormRolProyecto(),
                               list = MgrPermiso().listar()
                               )

@app.route('/deleteRolProyecto/<path:idRol>.html')
def deleteRolProyecto(idRol):
    """ Elimina un Rol de proyecto """
    if g.user is None:
        return redirect(url_for('login'))   
    else:
        rol = MgrRol().filtrarXId(idRol)
        flash(MgrRol().borrar(rol))
        return redirect(url_for('listRolProyecto'))


# FIN DE GESTIONAR ROL DE PROYECTO Y PERMISO by Stfy


#------------------------------------------------------------------------------#
# MODULO GESTION
#------------------------------------------------------------------------------#
# GESTIONAR USUARIOS DEL PROYECTO
#------------------------------------------------------------------------------#
@app.route('/listUserProyecto', methods=['GET','POST'])
def listUserProyecto():
    """ Lista los Usuarios de un Proyecto"""
    if g.user is None:
        return redirect(url_for('login'))
    else:
        return render_template(app.config['DEFAULT_TPL']+'/listUserProyecto.html',
			       conf = app.config,
                               list = MgrProyecto().usersDeProyecto(g.proyecto.nombre), 
                               )
 
@app.route('/showUserProyecto/<path:idUser>.html', methods=['GET','POST'])
def showUserProyecto(idUser):
    """Muestra un usuario de un proyecto"""
    if g.user is None:
        return redirect(url_for('login'))
    else:
        user = MgrUser().filtrarXId(idUser)
        nombreProyecto = g.proyecto.nombre
        rol = MgrUser().rolDeUser(user, nombreProyecto)
        form = ShowFormUserProyecto(request.form, name = user.name, password = user.passwd,
               nombre = user.nombre, apellido = user.apellido, 
               email = user.email, telefono = user.telefono,
               obs = user.obs, estado = user.estado, rolNombre = rol.nombre)   
        if request.method == 'POST':
            if request.form.get('desasignar', None) == "Desasignar Usuario de Proyecto":
                return redirect(url_for('desasignarUsuarioDeProyecto', idUser = user.idUser))
        return render_template(app.config['DEFAULT_TPL']+'/showUserProyecto.html',
			       conf = app.config,
			       form = form,
                               user = user
                               )

@app.route('/desasignarUsuarioDeProyecto/<path:idUser>.html', methods=['GET','POST'])
def desasignarUsuarioDeProyecto(idUser):
    """ Elimina al usuario del proyecto"""
    if g.user is None:
        return redirect(url_for('login'))
    else:
        # verifica q exista  el proyecto, el usuario y el rol de proyecto
        user = MgrUser().filtrarXId(idUser)
        rol = MgrUser().rolDeUser(user, g.proyecto.nombre)
        flash(MgrProyecto().desasignarUsuario(g.proyecto, user, rol))
        return redirect(url_for('listUserProyecto')) 



@app.route('/addUserProyecto', methods=['GET','POST'])
def addUserProyecto():
    """ Agrega un usuario nuevo al proyecto"""
    if g.user is None:
        return redirect(url_for('login'))
    else:
        proy = MgrProyecto().filtrarXId(g.proyecto.idProyecto)
        idUser = request.form.get("usuario") 
        idRol = request.form.get("rol")
        if request.method == 'POST' and idUser != None and idRol != None:
            user = MgrUser().filtrarXId(idUser)
            rol = MgrRol().filtrarXId(idRol)
            flash(MgrProyecto().asignarUsuario(proy, user, rol))
            return redirect(url_for('listUserProyecto')) 
        else:
            return render_template(app.config['DEFAULT_TPL']+'/formUserProyecto.html',
                                   conf = app.config,
                               list = MgrProyecto().usersDeProyecto(proy.nombre),
                               listU = MgrUser().listar(),
                               listR = MgrRol().listarPorAmbito(proy.nombre))

# FIN DE GESTIONAR USUARIOS DE PROYECTO by Stfy


#------------------------------------------------------------------------------#
# MODULO GESTION
#------------------------------------------------------------------------------#
# GESTIONAR USUARIOS DEL COMITE DE UN PROYECTO
#------------------------------------------------------------------------------#
@app.route('/listUserComite', methods=['GET','POST'])
def listUserComite():
    """ Lista los Usuarios del comite de un Proyecto"""
    if g.user is None:
        return redirect(url_for('login'))
    else:
        return render_template(app.config['DEFAULT_TPL']+'/listUserComite.html',
			       conf = app.config,
                               list = MgrComite().miembrosComite(g.proyecto.nombre)
                               )

@app.route('/addUserComite', methods=['GET','POST'])
def addUserComite():
    """ Agregar usuario a comite de proyecto """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        nombreProyecto = g.proyecto.nombre 
        proyecto =  MgrProyecto().filtrar(nombreProyecto)
        comite = MgrComite().search(nombreProyecto)
        idUser = request.form.get("usuario")       
        if request.method == 'POST' and idUser != None:
            user = MgrUser().filtrarXId(idUser)
            flash(MgrComite().asignarUsuario(proyecto,user))
            return redirect(url_for('listUserComite')) 
        else:
            return render_template(app.config['DEFAULT_TPL']+'/formUserComite.html',
			       conf = app.config,
                               listU = MgrProyecto().usersDeProyecto(nombreProyecto),
                               list = MgrComite().miembrosComite(nombreProyecto)
                               )
    

@app.route('/showUserComite/<idUser>.html', methods=['GET','POST'])
def showUserComite(idUser):
    """ Muestra un usuario de comite """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        nombreProyecto = g.proyecto.nombre 
        user = MgrUser().filtrarXId(idUser)
        comite = MgrComite().search(nombreProyecto)
        form = ShowFormUserComite(request.form, name = user.name, password = user.passwd,
               nombre = user.nombre, apellido = user.apellido, 
               email = user.email, telefono = user.telefono,
               obs = user.obs, estado = user.estado, comiteNombre = comite.nombre)   
        if request.method == 'POST':
            if request.form.get('desasignar', None) == "Desasignar Usuario de Comite" :
                return redirect(url_for('desasignarUsuarioDeComite', idUser=idUser))
	return render_template(app.config['DEFAULT_TPL']+'/showUserComite.html',
			       conf = app.config,
			       form = form
                               )
                               
@app.route('/desasignarUsuarioDeComite/<path:idUser>.html', methods=['GET','POST'])
def desasignarUsuarioDeComite(idUser):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        nombreProyecto = g.proyecto.nombre 
        proyecto = MgrProyecto().filtrar(nombreProyecto)
        user = MgrUser().filtrarXId(idUser)
        flash(MgrComite().desasignarUsuario(proyecto, user ))
        return redirect(url_for('listUserComite')) 
                               
# FIN DE GESTIONAR USUARIOS DE COMITE  by Stfy

#------------------------------------------------------------------------------#
# MODULO GESTION
#------------------------------------------------------------------------------#
# GESTIONAR LINEA BASE DE UNA FASE by Stfy
#------------------------------------------------------------------------------#
@app.route('/listFasesActivasG', methods=['GET','POST'])
def listFasesActivasG():
    if g.user is None:
        return redirect(url_for('login'))
    else:        
        return render_template(app.config['DEFAULT_TPL']+'/listFasesActivasG.html',
			       conf = app.config,
                               list = MgrProyecto().fasesDeProyecto(g.proyecto.nombre))


@app.route('/gesLB/<path:idFase>.html', methods=['GET','POST'])
def gesLB(idFase):
    """ Lista la lineas base de una fase """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        fase = MgrFase().filtrarXId(idFase)
        return render_template(app.config['DEFAULT_TPL']+'/gesLB.html',
                           conf = app.config,
                           fase = fase,
                           idFase = idFase,
                           list = MgrFase().lineaBaseDeFase(fase))


@app.route('/addLineaBase/<path:idFase>.html', methods=['GET','POST'])
def addLineaBase(idFase):
    """ Agrega una linea Base """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        fase = MgrFase().filtrarXId(idFase)
        if request.method == 'POST':
            idLista = request.form.getlist("lista") # lista de los items seleccionados
            form = CreateFormLineaBase(request.form,
                                     request.form['nombre'],
                                     descripcion = request.form['descripcion'],
                                     fase = request.form['fase'])
            lb = LineaBase(nombre=request.form['nombre'], descripcion=request.form['descripcion'], faseId=idFase)               
            if form.validate() and idLista != None and not MgrLineaBase().existe(lb):
                # 0. obtener los items aprobados seleccionados
                items = MgrItem().getListaItem(idLista)
                # 1. guardar la linea base
                flash(MgrLineaBase().guardar(lb))
                # 2. asignar los items seleccionados a la linea base
                flash(MgrLineaBase().asignarItems(lb, items))
        
                return redirect(url_for('gesLB', idFase = fase.idFase))
            else:
                return render_template(app.config['DEFAULT_TPL']+'/formLineaBase.html',
                            conf = app.config,
                            form = form,
                            fase = fase,
                            idFase = idFase,
                            list = MgrFase().listItemsAprobados(fase))
                            
        return render_template(app.config['DEFAULT_TPL']+'/formLineaBase.html',
                            conf = app.config,
                            form = CreateFormLineaBase(),
                            fase = fase,
                            idFase = idFase,
                            list = MgrFase().listItemsAprobados(fase))
                            
@app.route('/showLineaBase/<path:idLineaBase>.html', methods=['GET','POST'])
def showLineaBase(idLineaBase):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        lineaBase = MgrLineaBase().filtrarXId(idLineaBase)
        form = ShowFormLineaBase(request.form, nombre = lineaBase.nombre,
                    descripcion = lineaBase.descripcion,
                    estado = lineaBase.estado)
        if request.method == 'POST':
            if request.form.get('edit', None) == "Modificar LB":
                return redirect(url_for('editLineaBase', idLineaBase = lineaBase.idLineaBase))
            elif request.form.get('delete', None) == "Eliminar LB":
                return redirect(url_for('deleteLineaBase', idLineaBase = lineaBase.idLineaBase))
            elif request.form.get('editState', None) == "Modificar Estado de LB":
                return redirect(url_for('editStateLineaBase', idLineaBase = lineaBase.idLineaBase))
        return render_template(app.config['DEFAULT_TPL']+'/showLineaBase.html',
                conf = app.config,
                idLineaBase = idLineaBase,
                lineaBase = lineaBase,
                list = MgrLineaBase().itemsDeLB(lineaBase),
                form = form)


@app.route('/editLineaBase/<path:idLineaBase>.html', methods=['GET','POST'])
def editLineaBase(idLineaBase):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        lineaBase = MgrLineaBase().filtrarXId(idLineaBase)
        form = EditFormLineaBase(request.form, nombre = lineaBase.nombre,
                    descripcion = lineaBase.descripcion)
        if request.method == 'POST' and form.validate():
            flash(MgrLineaBase().modificar(lineaBase, request.form['nombre'], request.form['descripcion']))
            return redirect(url_for('showLineaBase', idLineaBase = lineaBase.idLineaBase))
    
    return render_template(app.config['DEFAULT_TPL']+'/editLineaBase.html',
                            conf = app.config,
                            idLineaBase = idLineaBase,
                            form = form)


@app.route('/editStateLineaBase/<path:idLineaBase>.html', methods=['GET','POST'])
def editStateLineaBase(idLineaBase):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        lineaBase = MgrLineaBase().filtrarXId(idLineaBase)
        if request.method == 'POST':
            flash(MgrLineaBase().estado(lineaBase, request.form['estado']))
            return redirect(url_for('showLineaBase', idLineaBase = lineaBase.idLineaBase))
        return render_template(app.config['DEFAULT_TPL']+'/editStateLineaBase.html',
                            conf = app.config,
                            idLineaBase = idLineaBase,
                            lineaBase = lineaBase,
                            buttons=['Activo', 'Comprometida', 'Inactivo']
                            )


@app.route('/deleteLineaBase/<path:idLineaBase>.html')
def deleteLineaBase(idLineaBase):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        lineaBase = MgrLineaBase().filtrarXId(idLineaBase)
        flash(MgrLineaBase().borrar(lineaBase, request.form['estado']))
        return redirect(url_for('gesLB', idFase = lineaBase.faseId))


# FIN DE GESTIONAR LINEA BASE DE UNA FASE  by Stfy

# ADMINISTRAR TIPO DE ITEM

@app.route('/listTipoDeItem')
def listTipoDeItem():
    """ Lista los datos de un tipo de item """
    if g.user is None:
        return redirect(url_for('login'))   
    else:
        list = MgrTipoDeItem().listar()
        return render_template(app.config['DEFAULT_TPL']+'/listTipoDeItem.html',
                           conf = app.config,
                           list = list) 
                    
@app.route('/showTipoDeItem/<path:idTipoDeItem>.html', methods=['GET','POST'])
def showTipoDeItem(idTipoDeItem):
    """ Muestra los datos de un tipo de item """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        tipoDeItem = MgrTipoDeItem().filtrarXId(idTipoDeItem)
        list = MgrTipoDeItem().atributosDeTipoDeItem(tipoDeItem)
        form = CreateFormTipoDeItem(request.form, nombre = tipoDeItem.nombre, 
               descripcion = tipoDeItem.descripcion)
        if request.method == 'POST':
            if request.form.get('edit', None) == "Modificar Tipo de Item":
                return redirect(url_for('editTipoDeItem', idTipoDeItem = tipoDeItem.idTipoDeItem))
            elif request.form.get('delete', None) == "Eliminar Tipo de Item":
                return redirect(url_for('deleteTipoDeItem', idTipoDeItem = tipoDeItem.idTipoDeItem))
	return render_template(app.config['DEFAULT_TPL']+'/showTipoDeItem.html',
			       conf = app.config,
                               list = list,
			       form = form)
                               
@app.route('/addTipoDeItem', methods=['GET','POST'])
def addTipoDeItem():
    """Controlador para crear un tipo de item"""
    if g.user is None:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST' :
            idLista = request.form.getlist("lista")
            form = CreateFormTipoDeItem(request.form, nombre = request.form['nombre'], 
                        descripcion = request.form['descripcion'])
            tipoDeItem = TipoDeItem(nombre = request.form['nombre'],
                            descripcion = request.form['descripcion'])
            if  form.validate() and idLista != None and not MgrTipoDeItem().existe(tipoDeItem):
                lisA = MgrTipoDeAtrib().listaAtrib(idLista)
                MgrTipoDeItem().asignarAtributosItem(tipoDeItem,lisA)
                MgrTipoDeItem().guardar(tipoDeItem)
                flash('Se ha creado correctamente el tipo de item')
                return redirect(url_for('listTipoDeItem'))
            else:
                return render_template(app.config['DEFAULT_TPL']+'/addTipoDeItem.html',
                                conf = app.config,
                                form = form,
                                list = MgrTipoDeAtrib().listar())
    return render_template(app.config['DEFAULT_TPL']+'/addTipoDeItem.html',
                conf = app.config,
                form = CreateFormTipoDeItem(),
                list = MgrTipoDeAtrib().listar())
                

@app.route('/editTipoDeItem/<path:idTipoDeItem>.html', methods=['GET','POST'])
def editTipoDeItem(idTipoDeItem):
    """ Modifica los datos de un tipo de item """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        tipoDeItem = MgrTipoDeItem().filtrarXId(idTipoDeItem)
        form = CreateFormTipoDeItem(request.form, nombre = tipoDeItem.nombre,
                descripcion = tipoDeItem.descripcion)
        idLista = request.form.getlist("lista")
        listAtrib2 = MgrTipoDeItem().filtrarTipoDeAtrib(tipoDeItem.nombre)
	if request.method == 'POST' and form.validate() and idLista != None:
            for atrib in idLista:
                if atrib in listAtrib2:
                    idLista.remove(atrib)
            for atrib in listAtrib2:
                if atrib in idLista:
                    listAtrib2.remove(atrib)
            MgrTipoDeItem().asignarTipoDeAtrib2(tipoDeItem, idLista,listAtrib2)
            MgrTipoDeItem().modificar(tipoDeItem.nombre, request.form['nombre'], request.form['descripcion'])
            flash('Se ha modificado correctamente el tipo de item')
            return redirect(url_for('showTipoDeItem', idTipoDeItem = tipoDeItem.idTipoDeItem))
        else:
            return render_template(app.config['DEFAULT_TPL']+'/editTipoDeItem.html',
			       conf = app.config,
			       form = form,
                               idTipoDeItem = idTipoDeItem,
                               listAtrib = MgrTipoDeItem().filtrarTipoDeAtrib(tipoDeItem.nombre),
                               list = MgrTipoDeAtrib().listar()
                               )
    return render_template(app.config['DEFAULT_TPL']+'/editTipoDeItem.html',
			       conf = app.config,
			       form = form,
                               idTipoDeItem = idTipoDeItem,
                               listAtrib = MgrTipoDeItem().filtrarTipoDeAtrib(tipoDeItem.nombre),
                               list = MgrTipoDeAtrib().listar()
                               )
            
@app.route('/deleteTipoDeItem/<path:idTipoDeItem>.html')
def deleteTipoDeItem(idTipoDeItem):
    """ Elimina un usuario """
    if g.user is None:
        return redirect(url_for('login'))   
    else:
        tipoDeItem = MgrTipoDeItem().filtrarXId(idTipoDeItem)
        MgrTipoDeItem().borrar(tipoDeItem.nombre)
        flash('Se ha borrado correctamente')
        return redirect(url_for('listTipoDeItem'))
    
    
#------------------------------------------------------------------------------#
# MODULO GESTION
#------------------------------------------------------------------------------#
# GESTIONAR REPORTES DE UN PROYECTO by Stfy
#------------------------------------------------------------------------------#
