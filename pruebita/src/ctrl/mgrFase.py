from modulo import *
from sqlalchemy import or_, and_

class MgrFase():

    def existe(self, fase):
        f = Fase.query.filter(and_(Fase.nombre == fase.nombre, Fase.proyectoId == fase.proyectoId)).first()
        if f != None:
            return True
        else:
            return False

    def guardar(self, fase):
        proyecto = Proyecto.query.filter(Proyecto.idProyecto == fase.proyectoId).first_or_404()
        if self.existe(fase):
            return ":NO guardo la fase - existe una fase con el mismo nombre en el proyecto:"
        if proyecto.estado == "Pendiente":
            db.session.add(fase)
            db.session.commit()
            return ":guardo fase:"
        else:
            return ":NO guardo la fase:"
               
    def borrar(self, fase):
        proyecto = Proyecto.query.filter(Proyecto.idProyecto == fase.proyectoId).first_or_404()
        if not self.existe(fase):
            return ":NO borro la fase - la fase no existe:"
        if proyecto.estado == "Pendiente":
            db.session.delete(fase)
            db.session.commit()
            return ":borro la fase:"
        else:
            return ":NO borro la fase:"
    
    def modificar(self, fase,  descripcionNew, tipoDeItemIdNew):
        if not self.existe(fase):
            return ":NO modifico la fase - la fase no existe:"
        if fase.estado == "Pendiente":
            fase.descripcion = descripcionNew
            fase.tipoDeItemId = tipoDeItemIdNew
            db.session.commit()
            return ":modifico la fase:"
        else:
            return ":NO modifico la fase:"

    def listar(self):
        return Fase.query.all()
               
    def filtrar(self, nombre):
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
    
    def filtrarItemsId(self, idFase):
        fase = Fase.query.filter(Fase.idFase == idFase).first_or_404()
        todos = fase.listaItem
        list = []
        for item in todos:
            if item.estado != "Eliminado":
                list.append(item)
        return list
    
    def filtrarItemsIdRelacion(self, idFase, idItem):
        fase = Fase.query.filter(Fase.idFase == idFase).first_or_404()
        todos = fase.listaItem
        list = []
        id=int(idItem)
        for item in todos:
            if item.estado != "Eliminado" and item.idItem != id:
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
    
    def getListPadreHijo(self, idItem):
        """Funcion que retorna la el idlist de los items que estan en relacion padre-hijo"""
        relacionList = Relacion.query.filter(and_(Relacion.itemDestinoId==idItem,Relacion.tipoDeRelacion=='padre-hijo')).all()
        idItemList = []
        for relacion in relacionList:
            idItemList.append(relacion.itemOrigenId)
        return idItemList
    
    def getItemsFaseAnterior(self, idFase):
        """Funcion que recibe un idfase y retorna los items de la  fase anterior"""
        faseActual = Fase.query.filter(Fase.idFase == idFase).first()
        posicion = faseActual.orden
        list = []
        if posicion != 1:
            faseAnterior = Fase.query.filter(and_(Fase.orden==posicion-1,
                                                    Fase.proyectoId==faseActual.proyectoId)).first_or_404()
            return self.filtrarItemsId(faseAnterior.idFase)
        else:
            return list
    
    def getListAntecesorSucesor(self, idItem):
        """Funcion que retorna la el idlist de los items que estan en relacion sucesor-antecesor"""    
        item = Item.query.filter(Item.idItem == idItem).first()
        relacionList = Relacion.query.filter(and_(Relacion.itemDestinoId==idItem,Relacion.tipoDeRelacion=='sucesor-antecesor')).all()
        idItemList = []
        for relacion in relacionList:
            idItemList.append(relacion.itemOrigenId)
        return idItemList

    def ciclo(self, idItemA, idItemB):
        """Funcion para determinar si al itroducir el vertice A---->B no se formara ningun ciclo"""
        if(idItemA == idItemB):
            return True
        relacionList = self.getRelaciones(idItemB)
        for relacion in relacionList:
            if self.ciclo(idItemA,relacion.itemDestinoId):
                return True
        return False
    
    def getRelaciones(self, idItem):
        """Funcion que retorna las relaciones de un Item segun su id"""
        result = Relacion.query.filter(Relacion.itemOrigenId == idItem).all()
        return result
    
    def relacionar(self, idItem, idItemList, tipo):
        """Funcion que guarda la relacion en la Base de datos"""
        relacioneliminarList = Relacion.query.filter(Relacion.itemDestinoId==idItem).all()
        for relacion in relacioneliminarList:
            db.session.delete(relacion)
        db.session.commit()
        relaciones = []    
        for id in idItemList:
            nuevo = Relacion(int(id),int(idItem),tipo)
            relaciones.append(nuevo)
        db.session.add_all(relaciones)
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
    