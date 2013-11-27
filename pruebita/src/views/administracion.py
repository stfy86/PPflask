from modulo import *
from werkzeug import secure_filename
from flask import Flask, render_template, request, redirect, url_for, g, \
     session, flash, escape, request, Response
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import A4
  
   
#------------------------------------------------------------------------------#
# MODULO ADMINISTRACION
#------------------------------------------------------------------------------#


# Reportes
@app.route('/descargarUser')
def descargarUser():   
    if g.user is None:
        return redirect(url_for('login'))
    else:
        import cStringIO
        buff = cStringIO.StringIO()
        doc = SimpleDocTemplate(buff, pagesize=A4, showBoundary=1)
        story = MgrReporte().generarUser()
        doc.build(story)        
        response = make_response(buff.getvalue())
        response.headers['Content-Disposition'] = "attachment; filename='reporteUser.pdf"
        response.mimetype = 'application/pdf'        
        buff.close()
        return response

@app.route('/descargarProyecto')
def descargarProyecto():   
    if g.user is None:
        return redirect(url_for('login'))
    else:
        import cStringIO
        buff = cStringIO.StringIO()
        doc = SimpleDocTemplate(buff, pagesize=A4, showBoundary=1)
        story = MgrReporte().generarProyecto()
        doc.build(story)        
        response = make_response(buff.getvalue())
        response.headers['Content-Disposition'] = "attachment; filename='reporteProyecto.pdf"
        response.mimetype = 'application/pdf'        
        buff.close()
        return response
                               
@app.route('/listProject')
def listProject():   
    """ Lista los Proyectos Pendientes y Finalizados """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        return render_template(app.config['DEFAULT_TPL']+'/listProject.html',
                           conf = app.config,
                           list = MgrProyecto().listar()) 

@app.route('/showProjectPendiente/<path:idProyecto>.html', methods=['GET','POST'])
def showProjectPendiente(idProyecto):
    """ Muestra un proyecto con estado pendiente """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        project = MgrProyecto().filtrarXId(idProyecto)
        form = ShowFormProject(request.form, nombre = project.nombre,
               descripcion = project.descripcion, 
               fechaDeCreacion = project.fechaDeCreacion,
               estado = project.estado,
               presupuesto = project.presupuesto)
        if request.method == 'POST':
            if request.form.get('edit', None) == "Modificar Proyecto":
                return redirect(url_for('editProject', idProyecto = project.idProyecto))
            elif request.form.get('editState', None) == "Modificar Estado de Proyecto":
                return redirect(url_for('editProjectState', idProyecto = project.idProyecto)) 
            elif request.form.get('delete', None) == "Eliminar Proyecto":
                return redirect(url_for('deleteProject', idProyecto = project.idProyecto))
            elif request.form.get('listComiteProyecto', None) == "Ver Comite de Proyecto":
                return redirect(url_for('listComiteProyecto', idProyecto = project.idProyecto))
            
	return render_template(app.config['DEFAULT_TPL']+'/showProjectPendiente.html',
			       conf = app.config,
			       form = form, 
                               proyecto = project)
                               
@app.route('/editProject/<path:idProyecto>.html', methods=['GET','POST'])
def editProject(idProyecto):
    """ Modifica un proyecto """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        project = MgrProyecto().filtrarXId(idProyecto)
        form = EditFormProject(request.form,
               descripcion = project.descripcion,
               presupuesto = project.presupuesto)
	if request.method == 'POST' and form.validate():
            flash(MgrProyecto().modificar(project.nombre, request.form['descripcion'], request.form['presupuesto']))
            return redirect(url_for('showProjectPendiente', idProyecto = idProyecto))
    return render_template(app.config['DEFAULT_TPL']+'/editProject.html',
			       conf = app.config,
                               proyecto = project,
                               idProyecto = idProyecto,
			       form = form)

@app.route('/editProjectState/<path:idProyecto>.html', methods=['GET','POST'])
def editProjectState(idProyecto):
    """ Modifica el estado del Proyecto """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        proyecto = MgrProyecto().filtrarXId(idProyecto)
        if request.method == 'POST': 
            flash (MgrProyecto().estado(proyecto.nombre, request.form['estado']))
	    return redirect(url_for('showProjectPendiente',idProyecto = proyecto.idProyecto))
	return render_template(app.config['DEFAULT_TPL']+'/editProjectState.html',
			       conf = app.config,
                               proyecto = proyecto,
                               idProyecto = idProyecto,
                               buttons=['Pendiente', 'Inactivo','Activo', 'Finalizado']
			       )
                               
@app.route('/addProject', methods=['GET','POST'])
def addProject():
    """ Agrega un Proyecto """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        list = MgrUser().listar()
        if request.method == 'POST':
            lista = request.form.get("lista")
            form = CreateFormProject(request.form, 
                                     request.form['nombre'], 
                                     descripcion = request.form['descripcion'],
                                     presupuesto = request.form['presupuesto'])
            p = Proyecto(nombre = request.form['nombre'], 
                                   descripcion = request.form['descripcion'],
                                   presupuesto = request.form['presupuesto']) 
                
            if form.validate() and lista != None and not MgrProyecto().existe(p):
                # 0. Crear el rol de lider del proyecto
                per =  MgrPermiso().filtrarXModulo("ModuloGestion")
                r = Rol(nombre="LiderDeProyecto", descripcion="rol de lider", ambito= request.form['nombre'], permisos=per)
                u = MgrUser().filtrarXId(lista)
                # 1. guarda el proyecto
                flash(MgrProyecto().guardar(p))
                # 2. guarda el rol del lider
                #flash(MgrRol().guardar(r))
                # 3. asigna el rol de lider al usuario 
                flash(MgrProyecto().asignarLider(p, r, u.name))
                flash(":addProyecto:")
                proyecto = MgrProyecto().filtrar(p.nombre)
                return redirect(url_for('addComite', idProyecto = proyecto.idProyecto))
            elif lista==None:
                flash("no eligio un lider")
                return render_template(app.config['DEFAULT_TPL']+'/formProject.html',
                            conf = app.config,
                            form = form,
                            list = MgrUser().listar())
            elif MgrProyecto().existe(p):
                flash("ya existe el proyecto")
                return render_template(app.config['DEFAULT_TPL']+'/formProject.html',
                            conf = app.config,
                            form = form,
                            list = MgrUser().listar())
            else:
                return render_template(app.config['DEFAULT_TPL']+'/formProject.html',
                            conf = app.config,
                            form = form,
                            list = MgrUser().listar())
                
    return render_template(app.config['DEFAULT_TPL']+'/formProject.html',
                conf = app.config,
                form = CreateFormProject(),
                list = MgrUser().listar())

@app.route('/deleteProject/<path:idProyecto>.html')
def deleteProject(idProyecto):
    """ Elimina un proyecto """
    if g.user is None:
        return redirect(url_for('login'))   
    else:  
        project = MgrProyecto().filtrarXId(idProyecto)
        flash(MgrProyecto().borrar(project))
        return redirect(url_for('listProject'))
              
     
@app.route('/listComiteProyecto/<path:idProyecto>.html', methods=['GET','POST'])
def listComiteProyecto(idProyecto):
    """ Lista los comite del Sistema"""
    if g.user is None:
        return redirect(url_for('login'))
    else:
        project = MgrProyecto().filtrarXId(idProyecto)
        return render_template(app.config['DEFAULT_TPL']+'/listComiteProyecto.html',
                           conf = app.config,
                           list = MgrComite().listarPorProyecto(idProyecto),
                           proyecto = project,
                           idProyecto = idProyecto
                           ) 


@app.route('/showComite/<path:idProyecto>/<path:idComite>.html', methods=['GET','POST'])
def showComite(idProyecto, idComite):
    """Muestra un Comite"""
    if g.user is None:
        return redirect(url_for('login'))
    else:
        comite = MgrComite().filtrarXId(idComite)
        proyecto = MgrProyecto().filtrarXId(comite.proyectoId)
        form = ShowFormComite(request.form, nombre = comite.nombre,
               descripcion = comite.descripcion, 
               cantMiembro = comite.cantMiembro,
               proyectoId = comite.proyectoId
               )
        if request.method == 'POST':
            if request.form.get('edit', None) == "Modificar Comite":
                return redirect(url_for('editComite', idProyecto = idProyecto, idComite =idComite))
          
	return render_template(app.config['DEFAULT_TPL']+'/showComite.html',
			       conf = app.config,
			       form = form,
                               proyecto= proyecto,
                               idComite = idComite,
                               idProyecto = idProyecto)
                               
@app.route('/editComite/<path:idProyecto>/<path:idComite>.html', methods=['GET','POST'])
def editComite(idProyecto, idComite):
    """ Modifica un Comite """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        comite = MgrComite().filtrarXId(idComite)
        proyecto = MgrProyecto().filtrarXId(comite.proyectoId)
        form = EditFormComite(request.form,
               descripcion = comite.descripcion,
               cantMiembro = comite.cantMiembro)
	if request.method == 'POST' and form.validate():
            flash(MgrComite().modificar(comite, request.form['descripcion'], request.form['cantMiembro']))
            return redirect(url_for('listComiteProyecto', idProyecto= idProyecto))
    return render_template(app.config['DEFAULT_TPL']+'/editComite.html',
			       conf = app.config,
			       form = form,
                               idComite = idComite,
                               idProyecto = idProyecto)

@app.route('/addComite/<path:idProyecto>.html', methods=['GET','POST'])
def addComite(idProyecto):
    """Guarda un comite y asigna al lider del proyecto como usuario del comite"""
    if g.user is None:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            u = MgrProyecto().getUserLider(idProyecto)
            p = MgrProyecto().filtrarXId(idProyecto)
            form = CreateFormComite(request.form, 
                                     request.form['nombre'], 
                                     descripcion = request.form['descripcion'],
                                     cantMiembro = request.form['cantMiembro'])
            c = Comite(nombre = request.form['nombre']+"-"+p.nombre , 
                            descripcion = request.form['descripcion'],
                            cantMiembro = request.form['cantMiembro'],
                            proyectoId = idProyecto)
            if form.validate() and not MgrComite().existe(c) and u!=None:   
                flash(MgrComite().guardar(c))
                flash(MgrComite().asignarUsuario(p,u))  
                flash(':addComite:')
                return redirect(url_for('showProjectPendiente', idProyecto= idProyecto))
            elif MgrComite().existe(c):
                flash("ya existe el comite")
                return render_template(app.config['DEFAULT_TPL']+'/formComite.html',
                            conf = app.config,
                            idProyecto = idProyecto,
                            form = form)
            else:
                return render_template(app.config['DEFAULT_TPL']+'/formComite.html',
                            conf = app.config,
                            idProyecto = idProyecto,
                            form = form)                            
        return render_template(app.config['DEFAULT_TPL']+'/formComite.html',
                conf = app.config,
                idProyecto = idProyecto,
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
                           list = MgrUser().listar()) 


@app.route('/showUser/<path:idUser>.html', methods=['GET','POST'])
def showUser(idUser):
    """ Muestra un usuario"""
    if g.user is None:
        return redirect(url_for('login'))
    else:
        user = MgrUser().filtrarXId(idUser)
        form = ShowFormUser(request.form, name = user.name,
                            nombre = user.nombre, apellido = user.apellido,
                            email = user.email, telefono = user.telefono, obs = user.obs,
                            estado = user.estado)
        if request.method == 'POST':
            if request.form.get('edit', None) == "Modificar Usuario":
                return redirect(url_for('editUser', idUser = user.idUser))
            elif request.form.get('delete', None) == "Eliminar Usuario":
                return redirect(url_for('deleteUser', idUser = user.idUser))
            elif request.form.get('state', None) == "Modificar Estado de Usuario":
                return redirect(url_for('editState', idUser = user.idUser))
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
            user = User(name = request.form['name'],
                            passwd = request.form['password'],
                            nombre = request.form['nombre'],
                            apellido = request.form['apellido'],
                            email = request.form['email'],
                            telefono = request.form['telefono'],
                            obs = request.form['obs'])
            if form.validate() and not MgrUser().existe(user):
                flash(MgrUser().guardar(user))
                rol = MgrRol().search("Invitado", "none project")
                u = MgrUser().filtrar(user.name)
                flash(MgrUser().addRol(u, rol))
                return redirect(url_for('listUser'))
            elif MgrUser().existe(user):
                flash("el usuario ya existe")
                return render_template(app.config['DEFAULT_TPL']+'/formUser.html',
                            conf = app.config,
                            form = form)
            else:
                return render_template(app.config['DEFAULT_TPL']+'/formUser.html',
                            conf = app.config,
                            form = form)
    return render_template(app.config['DEFAULT_TPL']+'/formUser.html',
                conf = app.config,
                form = CreateFormUser())
                            

@app.route('/deleteUser/<path:idUser>.html')
def deleteUser(idUser):
    """ Elimina un usuario """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        user = MgrUser().filtrarXId(idUser)
        flash(MgrUser().borrar(user))
        return redirect(url_for('listUser'))
                             

@app.route('/edit/<path:idUser>.html', methods=['GET','POST'])
def editState(idUser):
    """ Modifica el estado de un usuario """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        user = MgrUser().filtrarXId(idUser)
        if request.method == 'POST':
            flash(MgrUser().estado(user, request.form['estado']))
            return redirect(url_for('listUser'))
    return render_template(app.config['DEFAULT_TPL']+'/editState.html',
                            conf = app.config,
                            idUser = idUser,
                            user = user,
                            buttons=['Inactivo', 'Activo']
                            )



@app.route('/editUser/<path:idUser>.html', methods=['GET','POST'])
def editUser(idUser):
    """ Modifica los datos de un usuario """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        user = MgrUser().filtrarXId(idUser)
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
            flash(MgrUser().modificar(user, request.form['password'],
            request.form['confirmacion'], request.form['nombre'],
            request.form['apellido'], request.form['email'],
            request.form['telefono'], request.form['obs']))
            flash(":editUser:")
            return redirect(url_for('listUser'))
    return render_template(app.config['DEFAULT_TPL']+'/editUser.html',
            conf = app.config,
            idUser = idUser,
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
                arch.save(os.path.join(app.config['UPLOAD_FOLDER']+secure_filename(arch.filename)))
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
                    if request.form['filename'] != atrib.filename or atrib.filename == "":
                        arch = request.files['file']
                        arch.save(os.path.join(app.config['UPLOAD_FOLDER']+secure_filename(arch.filename)))
                        MgrTipoDeAtrib().modificar(nombre, request.form['nombre'],
                        request.form['tipoDeDato'], request.form['descripcion'],
                        0, arch.filename, arch.read())
                        flash('Se ha modificado correctamente el atributo')
                        return redirect(url_for('listAtrib'))
                    else:
                        MgrTipoDeAtrib().modificarArchivo(nombre, request.form['nombre'],
                        request.form['descripcion'],0)
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
                               nombreu = nombre,
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
        filename = atrib.filename 
        return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
        #flash('El archivo se ha descargado satisfactoriamente')
                           

                                                 