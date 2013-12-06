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
                    
@app.route('/listItem/<path:idFase>.html')
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
                list = MgrFase().filtrarItemsId(idFase)
                item = Item(nombre = request.form['nombre'],
                            codigo = 0,
                            tipoDeItemId = idTipo,
                            version = request.form['version'],
                            complejidad = request.form['complejidad'],
                            faseId = idFase,
                            costo = request.form['costo'])
                nom = request.form['nombre']
                if list != []:
                    for n in list:
                        if n.nombre == nom:
                            flash('Ya existe un item activo con ese nombre')
                            return redirect(url_for('listItem', idFase = idFase))
                        else:
                            MgrItem().guardar(item)
                            MgrItem().modificarCodigo(nom)
                            flash('Se ha creado correctamente el item')
                            return redirect(url_for('listItem', idFase = idFase))
                else:
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
        fase = item.faseId
        form = ShowFormItem(request.form, nombre = item.nombre,
               version = item.version, complejidad = item.complejidad,
               costo = item.costo, estado = item.estado, fechaDeModif = item.fechaDeModif)
        if request.method == 'POST':
            if request.form.get('graficarItem', None) == "Graficar Item":
                return redirect(url_for('graficarItem', idItem = item.idItem))
            elif request.form.get('edit', None) == "Modificar Item":
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
                               idFase = fase)
                               
@app.route('/editItem/<path:idItem>.html', methods=['GET','POST'])
def editItem(idItem):
    """ Modifica los datos de un item """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        item = MgrItem().filtrarId(idItem)
        maxVersion = MgrItem().versionMax(item.codigo)
        cod = item.codigo
        fase = item.faseId
        if item.estado == "Activo" or item.estado == "Revision":
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
                               version = (maxVersion)+1,
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
        if item.estado == "Activo" or item.estado == "Revision":
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
			       fase = item.faseId,
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
                                            bool = 1,
                                            conf = app.config)
        if request.method == 'POST':
            item = MgrItem().filtrarId(idItem)
            if request.form['opcion'] == "Mostrar Item":
                if request.form['tipo']== "padre-hijo":
                    item = MgrItem().filtrarId(idItem)
                    idFase = item.faseId
                    codigo = MgrItem().codigoItem(idItem)
                    listItem = MgrFase().filtrarItemsIdRelacion(idFase, codigo)
                    if listItem == []:
                        flash('No hay otros items dentro de la fase para relacionar')
                    relacionadoList = MgrFase().getListPadreHijo(idItem)
                    return render_template(app.config['DEFAULT_TPL']+'/relacion.html',
                                           conf = app.config,
                                           bool = 1,
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
                    relacionadoList = MgrFase().getListSucesorAntecesor(idItem)
                    return render_template(app.config['DEFAULT_TPL']+'/relacion.html',
                                           conf = app.config,
                                           bool = 2,
                                           listItem=listItem,
                                           id = idItem,
                                           idItem=idItem,
                                           relacionadoList = relacionadoList)
                if request.form['tipo']== "antecesor-sucesor":
                    item = MgrItem().filtrarId(idItem)
                    idFase = item.faseId
                    listItem = MgrFase().getItemsFaseSiguiente(idFase)
                    if listItem == []:
                        flash('No hay fase siguiente, estas en la ultima fase')
                    relacionadoList = MgrFase().getListAntecesorSucesor(idItem)
                    return render_template(app.config['DEFAULT_TPL']+'/relacion.html',
                                           conf = app.config,
                                           bool = 3,
                                           listItem=listItem,
                                           id = idItem,
                                           relacionadoList = relacionadoList)
            if request.form['opcion'] == "Guardar":
                #if request.form['tipo']== "padre-hijo":
                for idItemB in request.form.getlist('iditemList'):
                    if MgrFase().ciclo(int(idItemB),idItem) == True:
                        item = MgrItem().filtrarId(idItem)
                        idFase = item.faseId
                        tipoR = request.form['tipo']
                        codigo = MgrItem().codigoItem(idItem)
                        listItem = MgrFase().filtrarItemsIdRelacion(idFase, codigo)
                        itemB = MgrItem().filtrarId(idItemB)
                        flash('Imposible crear relacion '+tipoR+ " entre "+
                                               itemB.nombre+
                                               " - "+
                                               item.nombre)
                        relacionadoList = [int(r) for r in request.form.getlist('iditemList')]
                    else:                
                        item = MgrItem().filtrarId(idItem)
                        flash(item.version)
                        maxVersion = MgrItem().versionMax(item.codigo)
                        itemNuevo = Item(codigo = item.codigo,
                                        nombre = item.nombre,
                                        version = (maxVersion)+1,
                                        complejidad = item.complejidad,
                                        costo = item.costo,
                                        faseId = item.faseId,
                                        tipoDeItemId = item.tipoDeItemId)
                        flash(itemNuevo.version)
                        MgrItem().cambiarEstadoAnterior(idItem)
                        MgrItem().guardar(itemNuevo)
                        idItem = MgrItem().idParaRelacionar(item.codigo)
                        fase = item.faseId
                        MgrFase().relacionar(idItem,
                                            request.form.getlist('iditemList'),
                                            request.form['tipo'])
                        flash("Se han guardado los cambios exitosamente")
                        return redirect(url_for('listItem', idFase = fase))
        return render_template(app.config['DEFAULT_TPL']+'/relacion.html',
                           id = idItem,
                           bool = 1,
                           idItem = idItem,
                           conf = app.config)

@app.route('/graficarItem/<path:idItem>.html') 
def graficarItem(idItem):
    
    if g.user is None:
        return redirect(url_for('login'))
    else:
        itemSeleccionado = MgrItem().filtrarId(idItem)
        #~ " Arcos Verdes: Relacion Hijo-Item, Arcos Rojos: Relacion Item-Padre, Arcos Rosas: Relacion Sucesor-Item, Arcos Azules: Relacion Item-Antecesor"
        graph = pydot.Dot(graph_type='graph',  label= "GRAFICO DEL ITEM "+itemSeleccionado.nombre)
                
        listaAtras  , graph = MgrGraficarItem().calculo_atras_grafo(itemSeleccionado, [], graph, itemSeleccionado)
        
        listaAdelante  , graph = MgrGraficarItem().calculo_adelante_grafo(itemSeleccionado, [], graph, itemSeleccionado)
        
       
        #fecha=datetime.datetime.now()
        
        ############################################DESARROLLO########################################
        nombreImagen = idItem + '.png'
        graph.write_png(app.config['UPLOAD_FOLDER'] + nombreImagen)
        
        ############################################DESARROLLO########################################
        
        return send_from_directory(app.config['UPLOAD_FOLDER'],
                               nombreImagen)


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

@app.route('/showSolicitud/<path:idSolicitud>.html' , methods=['GET', 'POST'])
def showSolicitud(idSolicitud):
    """  Muestra un formulario no editable del item con las opciones de modificar, eliminar item """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        s = MgrSolicitud().filtrarXId(idSolicitud)
        form = ShowFormSolicitud(request.form, nombre = s.nombre,
                                        descripcion = s.descripcion,
                                        autor = s.autor.nombre,
                                        complejidad = MgrSolicitud().complejidadTotal(s),
                                        costo = MgrSolicitud().costoTotal(s),
                                        a_favor = s.votosPositivos,
                                        en_contra = s.votosNegativos)
                                 

        return render_template(app.config['DEFAULT_TPL'] + '/showSolicitud.html',
                               conf=app.config,
                               idSolicitud=idSolicitud, form = form
                               )

@app.route('/ejecutarSolicitud/<path:idSolicitud>.html', methods=['GET', 'POST'])
def ejecutarSolicitud(idSolicitud):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        s = MgrSolicitud().filtrarXId(idSolicitud)
        c = MgrComite().filtrarXId(s.comiteId)
        u = g.user
        if MgrSolicitud().puedeEjecutar(c,s,u):
            flash("se puede ejecutar la solicitud")
            for i in s.items:
                itemSeleccionado = MgrItem().filtrarId(i.idItem)
                listaAtras   = MgrCambio().calculo_atras_grafo(itemSeleccionado, [])        
                listaAdelante = MgrCambio().calculo_adelante_grafo(itemSeleccionado, [])
                flash(MgrCambio().getLBItem(itemSeleccionado))
                for lb in MgrCambio().getLBItem(itemSeleccionado):
                    lb.estado = "Comprometido"
                    db.session.commit()
            
        else:
            flash("NO se puede ejecutar la solicitud")
        return redirect(url_for('showSolicitud',idSolicitud=idSolicitud ))
        
    
@app.route('/votarSolicitud/<path:idSolicitud>.html', methods=['GET', 'POST'])
def votarSolicitud(idSolicitud):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        s = MgrSolicitud().filtrarXId(idSolicitud)
        form = ShowFormSolicitud(request.form, nombre = s.nombre,
                                        descripcion = s.descripcion,
                                        autor = s.autor.nombre,
                                        complejidad = MgrSolicitud().complejidadTotal(s),
                                        costo = MgrSolicitud().costoTotal(s),
                                        a_favor = s.votosPositivos,
                                        en_contra = s.votosNegativos)
        if request.method == 'POST':   
            comite = MgrComite().filtrarXId(s.comiteId)
            user = g.user
            if MgrComite().esUsuario(comite, user):                
                if str(g.user.idUser) in s.votantes.split(','):
                    flash('Ud ya a votado!!!')
                    return render_template(app.config['DEFAULT_TPL'] + '/votarSolicitud.html',idSolicitud = idSolicitud,conf=app.config,form=form)


                if request.form.get('aceptar')=='1':
                    flash('si')
                    flash(s.votosNegativos)
                    s.votosPositivos=s.votosPositivos+1
                else:
                    flash('no')
                    s.votosNegativos=s.votosNegativos+1
                s.votantes=s.votantes+str(g.user.idUser)+','
                MgrSolicitud().guardar(s)
                return render_template(app.config['DEFAULT_TPL'] + '/votarSolicitud.html',idSolicitud = idSolicitud, conf=app.config,form=form)
            else:
                flash("no puede votar")
                return render_template(app.config['DEFAULT_TPL'] + '/votarSolicitud.html',
                               conf=app.config,
                               idSolicitud=idSolicitud,form = form
                               )
                
            
        else:
            return render_template(app.config['DEFAULT_TPL'] + '/votarSolicitud.html',
                               conf=app.config,
                               idSolicitud=idSolicitud,form = form
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
            form = CreateFormSolicitud(request.form, nombre=request.form['nombre'],
                                       descripcion=request.form['descripcion'],
                                       proyecto_nombre=request.form['proyecto_nombre']
                                       )
            items = request.form.getlist('lista')
            if form.validate() and  items != None:
                proyecto = MgrProyecto().filtrar(request.form['proyecto_nombre'])
                comite = MgrComite().search(proyecto.nombre)
                user = g.user
                solicitud = Solicitud( nombre=request.form['nombre'], descripcion=request.form['descripcion'], autorId=user.idUser, comiteId=comite.idComite)
                MgrSolicitud().guardar(solicitud)
                MgrSolicitud().asignarItems(solicitud,items)
                flash('Se ha creado correctamente la solicitud')
                
                return redirect(url_for('listSolicitudes'))
            else:
                flash('Debe seleccionar un item y completar los datos de la solicitud')
                return render_template(app.config['DEFAULT_TPL'] + '/formSolicitud.html',
                                       conf=app.config,
                                       form= form,
                                       list= MgrItem().aprobados())

    return render_template(app.config['DEFAULT_TPL'] + '/formSolicitud.html',
                           conf=app.config,
                           form=CreateFormSolicitud(),
                           list=MgrItem().aprobados())


#------------------------------------------------------------------------------#
# MODULO DESARROLLO
#------------------------------------------------------------------------------#
   
# Desarrollo Reporte

@app.route('/desReporte', methods=['GET','POST'])
def desReporte():
    if g.user is None:
        return redirect(url_for('login'))
    else:
        return render_template(app.config['DEFAULT_TPL']+'/desReporte.html',
			       conf = app.config
                                )

@app.route('/reporteItem', methods=['GET','POST'])
def reporteItem():
    if g.user is None:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            idItem = request.form.get("item")
            idFase = request.form.get("fase") 
            if  idItem != None and idFase != None:
                fase = MgrFase().filtrarXId(idFase)
                item = MgrItem().filtrarId(idItem)
                flash(fase)
                flash(item)
                import cStringIO
                buff = cStringIO.StringIO()
                doc = SimpleDocTemplate(buff, pagesize=A4, showBoundary=1)
                story = MgrReporte().generarReporteItem(item)
                doc.build(story)        
                response = make_response(buff.getvalue())
                response.headers['Content-Disposition'] = "attachment; filename='reporteItem.pdf"
                response.mimetype = 'application/pdf'        
                buff.close()
                return response
            if request.form['opcion'] == "Mostrar Item" and idFase != None:
                fase = MgrFase().filtrarXId(idFase)
                flash(fase)
                listaFNueva = []
                listaFNueva.append(fase)
                return render_template(app.config['DEFAULT_TPL']+'/reporteItem.html',
                               conf = app.config,
                               idFase = fase.idFase,
                               idItem = None,
                               listF = listaFNueva,
                               listI = MgrFase().filtrarItems(fase.nombre)
                                 )
                
                
        return render_template(app.config['DEFAULT_TPL']+'/reporteItem.html',
			       conf = app.config,
                               idFase = None,
                               idItem = None,
                               listF = MgrProyecto().fasesActivasDeProyecto(g.proyecto.nombre),
                               listI = []
                                )