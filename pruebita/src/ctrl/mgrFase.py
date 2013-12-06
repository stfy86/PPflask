""" Clase que maneja la Fase"""
from modulo import *
from sqlalchemy import or_, and_

class MgrFase():

    def existe(self, fase):
        """ Retorna True si la fase ya existe dentro del proyecto al
        que corresponde, False en caso contrario """
        f = Fase.query.filter(and_(Fase.nombre == fase.nombre, Fase.proyectoId == fase.proyectoId)).first()
        if f != None:
            return True
        else:
            return False

    def guardar(self, fase):
        """ Guarda una fase solo si:
        1. El proyecto esta en estado Pendiente
        2. El nombre de la fase no se repite dentro del proyecto """
        proyecto = Proyecto.query.filter(Proyecto.idProyecto == fase.proyectoId).first_or_404()
        if self.existe(fase):
            return ":NO guardo la fase: existe una fase con el mismo nombre en el proyecto:"
        if proyecto.estado == "Pendiente":
            db.session.add(fase)
            db.session.commit()
            return ":guardo fase:"
        else:
            return ":NO guardo la fase: el proyecto no esta en estado Pendiente"
               
    def borrar(self, fase):
        """ Borra la fase solo si:
        1. El proyecto esta en estado Pendiente
        2. La fase existe 
        """
        proyecto = Proyecto.query.filter(Proyecto.idProyecto == fase.proyectoId).first_or_404()
        if not self.existe(fase):
            return ":NO borro la fas: la fase no existe:"
        if proyecto.estado == "Pendiente":
            db.session.delete(fase)
            db.session.commit()
            return ":borro la fase:"
        else:
            return ":NO borro la fase: el proyecto no esta en estado Pendiente"
    
    def modificar(self, fase,  descripcionNew, tipoDeItemIdNew):
        """ Edita la fase solo si:
        1. La fase existe y esta en estado Pendiente
        """
        if not self.existe(fase):
            return ":NO modifico la fase: la fase no existe:"
        if fase.estado == "Pendiente":
            fase.descripcion = descripcionNew
            fase.tipoDeItemId = tipoDeItemIdNew
            db.session.commit()
            return ":modifico la fase:"
        else:
            return ":NO modifico la fase: la fase debe estar en estado Pendiente"

    def listar(self):
        """ Lista las fases """
        return Fase.query.all()
               
    def filtrar(self, nombre):
        """ Busca por nombre de fase """
        return Fase.query.filter(Fase.nombre == nombre).first_or_404()
    
    def buscarPro(self, idFase):
        fase = Fase.query.filter(Fase.idFase == idFase).first_or_404()
        idPro = fase.proyectoId
        proyecto = Proyecto.query.filter(Proyecto.idProyecto == idPro).first_or_404()
        nombrePro = proyecto.nombre
        return nombrePro
       
    def filtrarItems(self, nombre):
        fase = Fase.query.filter(Fase.nombre == nombre).first_or_404()
        return fase.listaItem
    
    def filtrarItemsAprobId(self, idFase):
        fase = Fase.query.filter(Fase.idFase == idFase).first_or_404()
        todos = fase.listaItem
        list = []
        for item in todos:
            if item.estado == "Aprobado" or item.estado == "Revision":
                list.append(item)
        return list
    
    def filtrarItemsId(self, idFase):
        fase = Fase.query.filter(Fase.idFase == idFase).first_or_404()
        todos = fase.listaItem
        list = []
        for item in todos:
            if item.estado != "Eliminado":
                list.append(item)
        return list
    
    def filtrarItemsIdRelacion(self, idFase, codigo):
        fase = Fase.query.filter(Fase.idFase == idFase).first_or_404()
        todos = fase.listaItem
        list = []
        for item in todos:
            if item.estado != "Eliminado" and item.codigo != codigo:
                list.append(item)
        return list
    
    
    def filtrarItemsEliminadosId(self, idFase):
        fase = Fase.query.filter(Fase.idFase == idFase).first_or_404()
        todos = fase.listaItem
        list = []
        for item in todos:
            if item.estado == "Eliminado":
                list.append(item)
        return list
    
    
    def filtrarTipoItems(self, idFase):
        fase = Fase.query.filter(Fase.idFase == idFase).first_or_404()
        idTipo = fase.tipoDeItemId
        tipoDeItem = TipoDeItem.query.filter(TipoDeItem.idTipoDeItem == idTipo).first_or_404()
        return tipoDeItem.nombre

    
    def filtrarTipoItemsId(self, idFase):
        fase = Fase.query.filter(Fase.idFase == idFase).first_or_404()
        idTipo = fase.tipoDeItemId
        return idTipo
    
    def filtrarItemXid(self, idItem):
        return Item.query.filter(Item.idItem == idItem).first_or_404()
    
    def getListPadreHijo(self, idItem):
        """Funcion que retorna la el idlist de los items que estan en relacion padre-hijo"""
        relacionList = Relacion.query.filter(and_(Relacion.itemOrigenId==idItem,Relacion.tipoDeRelacion=='padre-hijo',Relacion.estado=='Pendiente')).all()
        idItemList = []
        for relacion in relacionList:
            idItemList.append(relacion.itemDestinoId)
        return idItemList
    
    
    def getItemsFaseAnterior(self, idFase):
        """Funcion que recibe un idfase y retorna los items de la  fase anterior"""
        faseActual = Fase.query.filter(Fase.idFase == idFase).first()
        posicion = faseActual.orden
        list = []
        if posicion != 1:
            faseAnterior = Fase.query.filter(and_(Fase.orden==posicion-1,
                                                    Fase.proyectoId==faseActual.proyectoId)).first_or_404()
            return self.filtrarItemsAprobId(faseAnterior.idFase)
        else:
            return list

    def getItemsFaseSiguiente(self, idFase):
        """Funcion que recibe un idfase y retorna los items de la  fase siguiente"""
        faseActual = Fase.query.filter(Fase.idFase == idFase).first()
        posicion = faseActual.orden
        list = []
        idProyecto = faseActual.proyectoId
        cant = self.cantFaseDeProyecto(idProyecto)
        if posicion != cant:
            faseSiguiente = Fase.query.filter(and_(Fase.orden==posicion+1,
                                                    Fase.proyectoId==faseActual.proyectoId)).first_or_404()
            return self.filtrarItemsId(faseSiguiente.idFase)
        else:
            return list
    
    
    def getListSucesorAntecesor(self, idItem):
        """Funcion que retorna la el idlist de los items que estan en relacion sucesor-antecesor"""    
        item = Item.query.filter(Item.idItem == idItem).first()
        relacionList = Relacion.query.filter(and_(Relacion.itemOrigenId==idItem,Relacion.tipoDeRelacion=='sucesor-antecesor',Relacion.estado=='Pendiente')).all()
        idItemList = []
        for relacion in relacionList:
            idItemList.append(relacion.itemDestinoId)
        return idItemList
    
    def getListAntecesorSucesor(self, idItem):
        """Funcion que retorna el idlist de los items que estan en relacion antecesor-sucesor"""    
        item = Item.query.filter(Item.idItem == idItem).first()
        relacionList = Relacion.query.filter(and_(Relacion.itemOrigenId==idItem,Relacion.tipoDeRelacion=='antecesor-sucesor',Relacion.estado=='Pendiente')).all()
        idItemList = []
        for relacion in relacionList:
            idItemList.append(relacion.itemDestinoId)
        return idItemList

    
    def ciclo(self, idItemA, idItemB):
        """Funcion para determinar si al itroducir el vertice A---->B no se formara ningun ciclo"""
        if(idItemA == idItemB):
            return True
        relacionList = self.getRelaciones(idItemB)
        for relacion in relacionList:
            if self.ciclo(idItemA,relacion.itemOrigenId):
                return True
        return False
    
    def getRelaciones(self, idItem):
        """Funcion que retorna las relaciones de un Item segun su id"""
        result = Relacion.query.filter(Relacion.itemDestinoId == idItem).all()
        return result
    
    def relacionar(self, idItem, idItemList, tipo):
        """Funcion que guarda la relacion en la Base de datos"""
        relacioneliminarList = Relacion.query.filter(Relacion.itemOrigenId==idItem).all()
        itemO = self.filtrarItemXid(idItem)
        for relacion in relacioneliminarList:
            db.session.delete(relacion)
        db.session.commit()
        relaciones = []    
        for id in idItemList:
            nuevo = Relacion(int(idItem),int(id),tipo)
            itemD = self.filtrarItemXid(id)
            nuevo.nombre = 'Relacion-'+tipo+'-'+itemO.nombre+'-'+itemD.nombre
            relaciones.append(nuevo)
            itemD.estado = "Aprobado"
        db.session.add_all(relaciones)
        itemO.estado = "Aprobado"
        db.session.commit()

    def filtrarXId(self, idFase):
        return Fase.query.filter(Fase.idFase == idFase).first_or_404()

    def estado(self, fase, estadoNew):
        if fase.estado == "Activo" and estadoNew == "Finalizado" and self.itemsAprobados(fase):
            fase.estado = estadoNew        
            db.session.commit()
            return ":modifico estado: de Activo a " + estadoNew
        if fase.estado == "Pendiente" and estadoNew == "Activo" and fase.tipoDeItemId != None:
            fase.estado = estadoNew        
            db.session.commit()
            return ":modifico estado:  de Pendiente a" + estadoNew
        if fase.estado == "Finalizado" and estadoNew == "Activo":
            fase.estado = estadoNew        
            db.session.commit()
            return ":modifico estado: de Finalizado a"+ estadoNew
        return ":NO modifico el estado: de " + fase.estado + " a " +estadoNew
    
    def itemsAprobados(self, fase):
        for item in fase.listaItem:
            if item.estado != "Aprobado":
                return False
        return True
    
    def lineaBaseDeFase(self, fase):
        return fase.listaLineaBase
    
    def listItemsAprobados(self, fase):
        list = []
        for item in fase.listaItem:
            if item.estado == "Aprobado":
                itemN = Item.query.filter(Item.idItem == item.idItem).first()
                list.append(itemN)
        return list
    
    def listItemsActivo(self, fase):
        list = []
        for item in fase.listaItem:
            if item.estado == "Activo":
                itemN = Item.query.filter(Item.idItem == item.idItem).first()
                list.append(itemN)
        return list
    
    def cantFaseDeProyecto(self, idProyecto):
        proyecto = Proyecto.query.filter(Proyecto.idProyecto == idProyecto).first_or_404()
        cont = 0
        for i in proyecto.listafases:
            if i != None:
                cont = cont +  1
        return cont