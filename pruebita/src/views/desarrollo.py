from modulo import *
from flask import Flask, render_template, request, redirect, url_for, g, \
     session, flash, escape, request


                           
#------------------------------------------------------------------------------#
# MODULO DESARROLLO
#------------------------------------------------------------------------------#



# Solicitud de cambio

@app.route('/addSolicitud/<path:nombre>.html', methods=['GET','POST'])
def addSolicitud(nombre):
    """ Agrega una Solicitud """
    from models.solicitud import *
    from models.fase import *
    from form import CreateFormSolicitud
    from ctrl.mgrSolicitud import MgrSolicitud
    from ctrl.mgrFase import MgrFase
    from ctrl.mgrProyecto import MgrProyecto
    
    if g.user is None:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            form = CreateFormSolicitud(request.form, 
                                     request.form['nombre'], 
                                     descripcion = request.form['descripcion'])
            if form.validate():
                proyecto = MgrProyecto().filtrar(nombre)
                solicitud = Solicitud(nombre = request.form['nombre'], 
                                   descripcion = request.form['descripcion'])
                solicitud.descripcion = request.form['descripcion']
                solicitud.Comite = proyecto.Comite
                solicitud.estado = 'Pendiente'
                solicitud.votosPositivos = 0
                solicitud.votosNegativos = 0
                
                MgrSolicitud().guardar(solicitud)
                flash('Se ha creado correctamente la solicitud')
                
                return redirect(url_for('seleccionarItemsProyecto', nombre = solicitud.nombre))
            else:
                return render_template(app.config['DEFAULT_TPL']+'/formSolicitud.html',
                            conf = app.config,
                            form = form)
                
    return render_template(app.config['DEFAULT_TPL']+'/formSolicitud.html',
                conf = app.config,
                form = CreateFormSolicitud())
                

@app.route('/seleccionarItemsProyecto/<path:nombre>.html', methods=['GET','POST'])
def seleccionarItemsProyecto(nombre):
    from ctrl.mgrLineaBase import MgrLineaBase
    from ctrl.mgrItem import MgrItem
    from ctrl.mgrFase import MgrFase
    from ctrl.mgrProyecto import MgrProyecto
    from ctrl.mgrSolicitud import MgrSolicitud
    
    if g.user is None:
        return redirect(url_for('login'))
    else:
        
        if request.method == 'POST':
            lista = request.form.getlist("lista")
            MgrSolicitud().asignarItems(nombre, lista) 
            flash('Se ha asignado correctamente los items')
            return redirect(url_for('desarrollo'))
        
        seleccion = []
        seleccion = MgrProyecto().filtrarItemSolicitud(nombre)
        
        
        return render_template(app.config['DEFAULT_TPL']+'/seleccionarItems.html',
			       conf = app.config,
                               list = seleccion)
                               

@app.route('/editSolicitud/<path:nombre>.html', methods=['GET','POST'])
def editSolicitud(nombre):
    from ctrl.mgrSolicitud import MgrSolicitud
    from form import EditFormSolicitud
    if g.user is None:
        return redirect(url_for('login'))
    else:
        solicitud = MgrSolicitud().filtrar(nombre)
        form = EditFormSolicitud(request.form, nombre = solicitud.nombre,
                    descripcion = solicitud.descripcion)
	if request.method == 'POST' and form.validate():
            MgrSolicitud().modificar(nombre, request.form['nombre'], request.form['descripcion'])
            flash('Se ha modificado correctamente la solicitud')
            return redirect(url_for('desarrollo'))
    return render_template(app.config['DEFAULT_TPL']+'/editSolicitud.html',
			       conf = app.config,
			       form = form)