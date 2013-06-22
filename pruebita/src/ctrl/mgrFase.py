from modulo import *
from sqlalchemy import or_, and_

class MgrFase():

    def guardar(self, fase):
        db.session.add(fase)
        db.session.commit()
               
    def borrar(self,nombre):
        fase = Fase.query.filter(Fase.nombre == nombre).first_or_404()
        db.session.delete(fase)
        db.session.commit()
    
    def modificar(self, nombre, nombreNew, descripcionNew, ordenNew):
        fase = Fase.query.filter(Fase.nombre == nombre).first_or_404()
        fase.nombre = nombreNew
        fase.descripcion = descripcionNew
        fase.orden = ordenNew
        db.session.commit()

    def listar(self):
        return Fase.query.all()
    
    def listarXProyecto(self, nombreProyecto):
        proyecto = Proyecto.query.filter(Proyecto.nombre == nombre).first_or_404()    
        return Fase.query.filter(Fase.proyectoId == proyecto.idProyecto).all()
    
    def filtrar(self, nombre):
        return Fase.query.filter(Fase.nombre == nombre).first_or_404()
    
    def buscarPro(self, idFase):
        fase = Fase.query.filter(Fase.idFase == idFase).first_or_404()
        idPro = fase.proyectoId
        proyecto = Proyecto.query.filter(Proyecto.idProyecto == idPro).first_or_404()
        nombrePro = proyecto.nombre
        return nombrePro
        
    def estado(self, nombre, estadoNew):
        fase = Fase.query.filter(Fase.nombre == nombre).first_or_404()
        fase.estado = estadoNew        
        db.session.commit()
        
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
