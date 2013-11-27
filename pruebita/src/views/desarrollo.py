from modulo import *
from flask import Flask, render_template, request, redirect, url_for, g, \
     session, flash, escape, request


                           
#------------------------------------------------------------------------------#
# MODULO DESARROLLO
#------------------------------------------------------------------------------#
   
# Desarrollo Item

@app.route('/listFasesActivasD', methods=['GET','POST'])
def listFasesActivasD():
    if g.user is None:
        return redirect(url_for('login'))
    else:
        return render_template(app.config['DEFAULT_TPL']+'/listFasesActivasD.html',
			       conf = app.config,
                               list = MgrProyecto().fasesActivasDeProyecto(g.proyecto.nombre),
                                )
                  

@app.route('/admItem/<path:idFase>.html')
def admItem(idFase):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        
        return render_template(app.config['DEFAULT_TPL']+'/admItem.html',
                           identFase = idFase,
                           nomProyecto = MgrFase().buscarPro(idFase),
                           conf = app.config)
                    
@app.route('/listItem<path:idFase>.html')
def listItem(idFase):
    """ Lista los datos de un item """
    if g.user is None:
        return redirect(url_for('login'))   
    list = MgrFase().filtrarItemsId(idFase)
    return render_template(app.config['DEFAULT_TPL']+'/listItem.html',
                           conf = app.config,
                           id = idFase,
                           list = list) 
                               
                               
@app.route('/addItem/<path:idFase>.html', methods=['GET','POST'])
def addItem(idFase):
    """Controlador para crear item"""
    if g.user is None:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            form = CreateFormItem(request.form, nombre = request.form['nombre'],
                        tipoDeItem = request.form['tipoDeItem'],
                        version = request.form['version'],
                        complejidad = request.form['complejidad'],
                        costo = request.form['costo'])
            if form.validate():
                idTipo =  MgrFase().filtrarTipoItemsId(idFase)
                item = Item(nombre = request.form['nombre'],
                            codigo = 0,
                            tipoDeItemId = idTipo,
                            version = request.form['version'],
                            complejidad = request.form['complejidad'],
                            faseId = idFase,
                            costo = request.form['costo'])
                nom = request.form['nombre']
                MgrItem().guardar(item)
                MgrItem().modificarCodigo(nom)
                flash('Se ha creado correctamente el item')
                return redirect(url_for('listItem', idFase = idFase))
            else:
                return render_template(app.config['DEFAULT_TPL']+'/addItem.html',
                            conf = app.config,
                            form = form,
                            tipoItem = MgrFase().filtrarTipoItems(idFase),
                            idFase = idFase
                            )
    return render_template(app.config['DEFAULT_TPL']+'/addItem.html',
                conf = app.config,
                tipoItem = MgrFase().filtrarTipoItems(idFase),
                form = CreateFormItem(),
                idFase = idFase)
                
@app.route('/showItem/<path:idItem>.html', methods=['GET','POST'])
def showItem(idItem):
    """  Muestra un formulario no editable del item con las opciones de modificar, eliminar item """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        item = MgrItem().filtrarId(idItem)
        form = ShowFormItem(request.form, nombre = item.nombre,
               version = item.version, complejidad = item.complejidad,
               costo = item.costo, estado = item.estado, fechaDeModif = item.fechaDeModif)
        if request.method == 'POST':
            if request.form.get('edit', None) == "Modificar Item":
                return redirect(url_for('editItem', idItem = item.idItem))
            elif request.form.get('delete', None) == "Eliminar Item":
                return redirect(url_for('deleteItem', idItem = item.idItem))
            elif request.form.get('state', None) == "Modificar Estado de Item":
                return redirect(url_for('editItemState', idItem = item.idItem))
            elif request.form.get('relacionar', None) == "Relacionar Item":
                return redirect(url_for('relacion', idItem = item.idItem))
	return render_template(app.config['DEFAULT_TPL']+'/showItem.html',
			       conf = app.config,
			       form = form,
                               idItem = idItem,
                               idFase = item.faseId
                               )
                               
@app.route('/editItem/<path:idItem>.html', methods=['GET','POST'])
def editItem(idItem):
    """ Modifica los datos de un item """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        item = MgrItem().filtrarId(idItem)
        cod = item.codigo
        fase = item.faseId
        if item.estado == "Activo":
            form = CreateFormItem(request.form, nombre = item.nombre,
                        tipoDeItem = item.tipoDeItemId,
                        complejidad = item.complejidad,
                        costo = item.costo)
            if request.method == 'POST' and form.validate():
                item = Item(codigo = cod,
                                nombre = request.form['nombre'],
                                version = request.form['version'],
                                complejidad = request.form['complejidad'],
                                costo = request.form['costo'],
                                faseId = fase,
                                tipoDeItemId = request.form['tipoDeItem'])
                MgrItem().cambiarEstadoAnterior(idItem)
                MgrItem().guardar(item)
                flash('Se ha modificado correctamente el item')
                return redirect(url_for('listItem', idFase = fase))
        else:
            flash('NO se puede modificar el item, verifique su estado')
            return redirect(url_for('listItem', idFase = fase))
    return render_template(app.config['DEFAULT_TPL']+'/editItem.html',
			       conf = app.config,
                               item = MgrItem().filtrarId(idItem),
                               version = item.version+1,
			       form = form, 
                               idItem = idItem)

@app.route('/deleteItem/<path:idItem>.html')
def deleteItem(idItem):
    """ Elimina un item """
    if g.user is None:
        return redirect(url_for('login'))   
    else:
        item = MgrItem().filtrarId(idItem)
        fase = item.faseId
        if item.estado == "Activo":
            MgrItem().borrar(idItem)
            flash('Se ha borrado correctamente')
            return redirect(url_for('listItem', idFase = fase))
        else:
            flash('NO se puede eliminar el item, verifique su estado')
            return redirect(url_for('listItem', idFase = fase))
        
@app.route('/editItemState/<path:idItem>.html', methods=['GET','POST'])
def editItemState(idItem):
    """ Modifica el estado de un usuario """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        item = MgrItem().filtrarId(idItem)
        fase = item.faseId
        form = EditStateItemForm(request.form, estado = item.estado)
	if request.method == 'POST' and form.validate(): 
                MgrItem().estado(idItem, request.form['estado'])
		return redirect(url_for('listItem', idFase = fase))
	return render_template(app.config['DEFAULT_TPL']+'/editItemState.html',
			       conf = app.config,
			       form = EditStateItemForm(),
                               idItem = idItem)
                               
@app.route('/revivirItem<path:idFase>.html')
def revivirItem(idFase):
    """ Lista los datos de un de item ELIMINADO """
    if g.user is None:
        return redirect(url_for('login'))   
    list = MgrFase().filtrarItemsEliminadosId(idFase)
    return render_template(app.config['DEFAULT_TPL']+'/revivirItem.html',
                           conf = app.config,
                           id = idFase,
                           list = list) 
                           
@app.route('/showItemRevivir/<path:idItem>.html', methods=['GET','POST'])
def showItemRevivir(idItem):
    """  Muestra un formulario no editable del item con las opciones de modificar, eliminar item """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        item = MgrItem().filtrarId(idItem)
        form = ShowFormItem(request.form, nombre = item.nombre,
               version = item.version, complejidad = item.complejidad,
               costo = item.costo, estado = item.estado, fechaDeModif = item.fechaDeModif)
        if request.method == 'POST':
            if request.form.get('revivir', None) == "Revivir Item":
                return redirect(url_for('revivir', idItem = item.idItem))
	return render_template(app.config['DEFAULT_TPL']+'/showItemRevivir.html',
			       conf = app.config,
			       form = form)

@app.route('/revivir/<path:idItem>.html', methods=['GET','POST'])
def revivir(idItem):
    """ Revive un Item """
    if g.user is None:
        return redirect(url_for('login'))
    else:
            item = MgrItem().filtrarId(idItem)
            fase = item.faseId
            MgrItem().revivir(idItem)
            flash('Se ha revivido correctamente el item')
            return redirect(url_for('listItem', idFase = fase))
        
        
@app.route('/relacion/<path:idItem>.html', methods=['GET','POST'])
def relacion(idItem):
    """Funcion para relacionar los items"""  
    if g.user is None:
        return redirect(url_for('login'))
    else:
        if request.method == 'GET':
            return render_template(app.config['DEFAULT_TPL']+'/relacion.html',
                                            id = idItem,
                                            conf = app.config)
        if request.method == 'POST':
            if request.form['opcion'] == "Mostrar Item":
                if request.form['tipo']== "padre-hijo":
                    item = MgrItem().filtrarId(idItem)
                    idFase = item.faseId
                    listItem = MgrFase().filtrarItemsIdRelacion(idFase, idItem)
                    if listItem == []:
                        flash('No hay otros items dentro de la fase para relacionar')
                    relacionadoList = MgrFase().getListPadreHijo(idItem)
                    return render_template(app.config['DEFAULT_TPL']+'/relacion.html',
                                           conf = app.config,
                                           bool = True,
                                           id = idItem,
                                           listItem=listItem,
                                           idItem=idItem,
                                           relacionadoList = relacionadoList)
                if request.form['tipo']== "sucesor-antecesor":
                    item = MgrItem().filtrarId(idItem)
                    idFase = item.faseId
                    listItem = MgrFase().getItemsFaseAnterior(idFase)
                    if listItem == []:
                        flash('No hay fase anterior, estas en la primera fase')
                    relacionadoList = MgrFase().getListAntecesorSucesor(idItem)
                    return render_template(app.config['DEFAULT_TPL']+'/relacion.html',
                                           conf = app.config,
                                           bool = False,
                                           listItem=listItem,
                                           id = idItem,
                                           idItem=idItem,
                                           relacionadoList = relacionadoList)
            if request.form['opcion'] == "Guardar":
                if request.form['tipo']== "padre-hijo":
                    for idItemB in request.form.getlist('iditemList'):
                        if MgrFase().ciclo(int(idItemB),idItem):
                            item = MgrItem().filtrarId(idItem)
                            idFase = item.faseId
                            listItem = MgrFase().filtrarItemsIdRelacion(idFase, idItem)
                            itemB = MgrItem().filtrarId(idItemB)
                            relacionadoList = [int(r) for r in request.form.getlist('iditemList')]
                            return render_template(app.config['DEFAULT_TPL']+'/relacion.html',
                                                   conf = app.config,
                                                   bool = True,
                                                   listItem=listItem,
                                                   id = idItem,
                                                   idItem=idItem,
                                                   relacionadoList = relacionadoList,
                                                   error='Imposible crear relacion Padre-Hijo entre '+
                                                   itemB.nombre+
                                                   " - "+
                                                   item.nombre)
                MgrFase().relacionar(idItem,
                                    request.form.getlist('iditemList'),
                                    request.form['tipo'])
                flash("Se han guardado los cambios exitosamente")
    return render_template(app.config['DEFAULT_TPL']+'/relacion.html',
                       id = idItem,
                       idItem = idItem,
                       conf = app.config)




#------------------------------------------------------------------------------#
# MODULO DESARROLLO
#------------------------------------------------------------------------------#
   
# Solicitud de Cambio

@app.route('/listSolicitudes', methods=['GET', 'POST'])
def listSolicitudes():
    if g.user is None:
        return redirect(url_for('login'))
    else:
        return render_template(app.config['DEFAULT_TPL'] + '/listSolicitudes.html',
                               conf=app.config,
                               list=MgrSolicitud().listar()
                               )

@app.route('/showSolicitud/<path:idSolicitud>', methods=['GET', 'POST'])
def showSolicitud(idSolicitud):
    """  Muestra un formulario no editable del item con las opciones de modificar, eliminar item """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            s = MgrSolicitud().por_id(idSolicitud)
            form = ShowFormSolicitud(request.form, nombre = s.nombre)
            if str(g.user.idUser) in s.votantes.split(','):
                flash('Ud ya a votado!!!')
                return render_template(app.config['DEFAULT_TPL'] + '/showSolicitud.html',conf=app.config,s=s,form=form)
            
            if request.form.get('aceptar')=='1':
                flash('si')
                flash(s.votosNegativos)
                s.votosPositivos=s.votosPositivos+1
            else:
                flash('no')
                s.votosNegativos=s.votosNegativos+1
            s.votantes=s.votantes+str(g.user.idUser)+','
            MgrSolicitud().guardar(s)
            return render_template(app.config['DEFAULT_TPL'] + '/showSolicitud.html',conf=app.config,s=s,form=form)
        else:
            s = MgrSolicitud().por_id(idSolicitud)            
            form = ShowFormSolicitud(request.form, nombre = s.nombre)
            return render_template(app.config['DEFAULT_TPL'] + '/showSolicitud.html',
                               conf=app.config,
                               idSolicitud=idSolicitud,form=form,s=s
                               )
                               
    s = MgrSolicitud().por_id(idSolicitud)
    form = ShowFormSolicitud()
    return render_template(app.config['DEFAULT_TPL'] + '/showSolicitud.html',
                               conf=app.config,
                               idSolicitud=idSolicitud,form=form,s=s
                               )


# Solicitud de cambio

@app.route('/addSolicitud', methods=['GET', 'POST'])
def addSolicitud():
    """ Agrega una Solicitud """
    items = []
    if g.user is None:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            form = CreateFormSolicitud(nombre=request.form['nombre'],
                                       descripcion=request.form['descripcion'],
                                       proyecto_nombre=request.form['proyecto_nombre']
                                       )
            if form.validate() and request.form.get('lista') != None:

                proyecto = MgrProyecto().filtrar(request.form['proyecto_nombre'])
                solicitud = Solicitud(nombre=request.form['nombre'],
                                      descripcion=request.form['descripcion'])


                solicitud.Comite = proyecto.comite
                solicitud.estado = 'Pendiente'
                solicitud.votosPositivos = 0
                solicitud.votosNegativos = 0
                solicitud.autor = g.user
                MgrSolicitud().guardar(solicitud)

                for id in request.form['lista']:
                    item = MgrItem().filtrarId(id)
                    solicitud.itemsSolicitud.append(item)


                flash('Se ha creado correctamente la solicitud')

                return redirect(url_for('listSolicitudes'))
            else:
                flash('Debe seleccionar un item y completar los datos de la solicitud')
                return render_template(app.config['DEFAULT_TPL'] + '/formSolicitud.html',
                                       conf=app.config,
                                       form=form,
                                       list=MgrItem().aprobados())

    return render_template(app.config['DEFAULT_TPL'] + '/formSolicitud.html',
                           conf=app.config,
                           form=CreateFormSolicitud(proyecto_nombre=g.proyecto),
                           list=MgrItem().aprobados())
