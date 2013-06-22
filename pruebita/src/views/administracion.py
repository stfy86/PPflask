from modulo import *
from flask import Flask, render_template, request, redirect, url_for, g, \
     session, flash, escape, request
     
                           
#------------------------------------------------------------------------------#
# MODULO ADMINISTRACION
#------------------------------------------------------------------------------#


# ADMINISTRAR PROYECTO


@app.route('/listProject')
def listProject():
    if g.user is None:
        return redirect(url_for('login'))
    else:
        return render_template(app.config['DEFAULT_TPL']+'/listProject.html',
                           conf = app.config,
                           list = MgrProyecto().listar(),) 


@app.route('/showProject/<path:nombre>.html', methods=['GET','POST'])
def showProject(nombre):
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
          
	return render_template(app.config['DEFAULT_TPL']+'/showProject.html',
			       conf = app.config,
			       form = form)
                               
@app.route('/editProject/<path:nombre>.html', methods=['GET','POST'])
def editProject(nombre):
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

@app.route('/addProject', methods=['GET','POST'])
def addProject():
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

# ADMINISTRAR COMITE


@app.route('/listComite')
def listComite():
    if g.user is None:
        return redirect(url_for('login'))
    else:
        return render_template(app.config['DEFAULT_TPL']+'/listComite.html',
                           conf = app.config,
                           list = MgrComite().listar(),) 


@app.route('/showComite/<path:nombre>.html', methods=['GET','POST'])
def showComite(nombre):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        comite = MgrComite().filtrar(nombre)
        form = ShowFormComite(request.form, nombre = comite.nombre,
               descripcion = comite.descripcion, 
               cantMiembro = comite.cantMiembro,
               proyectoId = comite.proyectoId
               )
        if request.method == 'POST':
            if request.form.get('edit', None) == "Modificar Comite":
                return redirect(url_for('editComite', nombre = comite.nombre))
          
	return render_template(app.config['DEFAULT_TPL']+'/showComite.html',
			       conf = app.config,
			       form = form)
                               
@app.route('/editComite/<path:nombre>.html', methods=['GET','POST'])
def editComite(nombre):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        comite = MgrComite().filtrar(nombre)
        form = CreateFormComite(request.form,
               nombre = comite.nombre,
               descripcion = comite.descripcion,
               cantMiembro = comite.cantMiembro)
	if request.method == 'POST' and form.validate:
            MgrComite().modificar(nombre, request.form['nombre'],request.form['descripcion'], request.form['cantMiembro'])
            flash('Se ha modificado correctamente el comite')
            return redirect(url_for('listComite'))
    return render_template(app.config['DEFAULT_TPL']+'/editComite.html',
			       conf = app.config,
			       form = form)

@app.route('/addComite/<path:nameLider>/<path:nombre>.html', methods=['GET','POST'])
def addComite(nombre, nameLider):
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
                      