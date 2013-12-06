"""Clase que maneja los Items"""
from modulo import *
from sqlalchemy import and_, or_

class MgrItem():

    def listar(self):
        return Item.query.all()
    
    def guardar(self, item):
        db.session.add(item)
        db.session.commit()
        
    def estado(self, idItem, estadoNew):
        item = Item.query.filter(Item.idItem == idItem).first_or_404()
        item.estado = estadoNew        
        db.session.commit()
    
    def borrar(self,idItem):
        item = Item.query.filter(Item.idItem == idItem).first_or_404()
        relaciones = Relacion.query.filter(or_(Relacion.itemOrigenId == idItem,Relacion.itemDestinoId == idItem), Relacion.estado == "Pendiente").all()
        item.estado = "Eliminado"
        for relacion in relaciones:
            relacion.estado = "Inactivo"
        db.session.commit()
        
    def modificarCodigo(self, nombre):
        item = Item.query.filter(Item.nombre == nombre).first_or_404()
        item.codigo = item.idItem
        db.session.commit()
        
    def modificar(self, nombre, nombreNew, versionNew, complejidadNew, costoNew):
        item = Item.query.filter(Item.nombre == nombre).first_or_404()
        item.nombre = nombreNew
        item.version = versionNew
        item.complejidad = complejidadNew
        item.costo = costoNew
        db.session.commit()

    def filtrar(self, nombre):
        return Item.query.filter(Item.nombre == nombre).first_or_404()
    
    def filtrarId(self, idItem):
        return Item.query.filter(Item.idItem == idItem).first_or_404()
    
    def asignarTipoDeItem2(self, nombre, id):
        item = Item.query.filter(Item.nombre == nombre).first_or_404()
        tipoItem = TipoDeItem.query.filter(TipoDeItem.idTipoDeItem == id).first_or_404()
        # asigna al item el tipo de item 
        item.tipoDeItem = tipoItem
        db.session.commit()
            
                
    def filtrarTipoDeItem(self, nombre):
        item = Item.query.filter(Item.nombre == nombre).first_or_404()
        return item.tipoDeItemId

    def filtrarAprobadoXFase(self, faseId):
        return Item.query.filter(and_(Item.faseId == faseId, Item.estado == 'Aprobado'))
    
    def cambiarEstadoAnterior(self, idItem):
        item = Item.query.filter(Item.idItem == idItem).first_or_404()
        relaciones = Relacion.query.filter(or_(Relacion.itemOrigenId == idItem,Relacion.itemDestinoId == idItem), Relacion.estado == "Pendiente").all()
        item.estado = "Eliminado"
        for relacion in relaciones:
            relacion.estado = "Inactivo"
        db.session.commit()
        
    def eliminarRelacion(self, idItem):
        origen = Relacion.query.filter(Relacion.itemOrigenId == idItem).all()
        destino = Relacion.query.filter(Relacion.itemDestinoId == idItem).all()
        
        for o in origen:
            if o.estado == "Pendiente":
                o.estado = "Inactivo"
        
        for d in destino:
            if d.estado == "Pendiente":
                d.estado = "Inactivo"
                
    def revivirRelacion(self, idItem):
        origen = Relacion.query.filter(Relacion.itemOrigenId == idItem).all()
        destino = Relacion.query.filter(Relacion.itemDestinoId == idItem).all()
        
        for o in origen:
            if o.estado == "Inactivo":
                o.estado = "Pendiente"
        
        for d in destino:
            if d.estado == "Inactivo":
                d.estado = "Pendiente"
        
    def revivir(self, idItem):
        item = Item.query.filter(Item.idItem == idItem).first_or_404()
        cod = item.codigo
        list = []
        list = Item.query.filter(Item.codigo == cod).all()
        for i in list:
            if i.estado == "Activo":
                self.eliminarRelacion(i.idItem)
                i.estado = "Eliminado"
        item.estado = "Activo" 
        self.revivirRelacion(idItem)
        db.session.commit()

    def getListaItem(self, listaId):
        list = []
        for i in listaId:
            item = Item.query.filter(Item.idItem == i).first_or_404()
            list.append(item)
        return list
    
    def idParaRelacionar(self, cod):
        list = []
        list = Item.query.filter(Item.codigo == cod).all()
        for i in list:
            if i.estado == "Activo":
                return i.idItem
            
    def versionMax(self, cod):
        list2 = []
        list = Item.query.filter(Item.codigo == cod).all()
        for i in list:
            list2.append(i.version)
        list2.sort()
        return int(list2.pop())
    
    def codigoItem(self, idItem):
        item = Item.query.filter(Item.idItem == idItem).first_or_404()
        return item.codigo
  
    
    
    def aprobados(self):
        return Item.query.filter(Item.estado == 'Aprobado')
        
    def historialItem(self, item):
        list = Item.query.filter(Item.codigo == item.codigo).all()
        hist = []
        for i in list:
            hist.append(i)
        return hist
