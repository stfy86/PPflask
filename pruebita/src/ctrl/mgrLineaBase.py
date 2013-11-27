from modulo import *
from sqlalchemy import or_, and_

class MgrLineaBase():

    def guardar(self, lineaBase):
        f = Fase.query.filter(Fase.idFase == lineaBase.faseId).first_or_404()
        if f.estado == "Activo":
            return ":No guardo la linea base: la fase no esta en estado Activo"
        if self.existe(lineaBase):
            return ":No guardo linea base:"
        else:
            lineaBase.estado = "Activo"
            db.session.add(lineaBase)
            db.session.commit()
            return ":guardo linea base:"
    
    def borrar(self, lineaBase):
        f = Fase.query.filter(Fase.idFase == lineaBase.faseId).first_or_404()
        if f.estado == "Finalizado":
            return ":No borro la linea base: la fase esta en estado Finalizado"        
        if self.existe(lineaBase) and f.estado == "Activo":
            lineaBase.estado="Inactivo"
            for i in self.itemsDeLB(lineaBase):
                item = Item.query.filter(Item.idItem == i.idItem).first_or_404()
                item.estado = "Revision"
            db.session.commit()
            return ":borro la linea base:"
        else:
            return ":no borro la linea base:"
        
    def listar(self):
        return LineaBase.query.all()
    
    def filtrar(self, nombre):
        return LineaBase.query.filter(LineaBase.nombre == nombre).first_or_404()

    def filtrarXId(self, idLineaBase):
        return LineaBase.query.filter(LineaBase.idLineaBase == idLineaBase).first_or_404()

    def estado(self, lineaBase, estadoNew):
        if not self.existe(lineaBase):
            return ":no modifico de estado: la lb no existe"
        if lineaBase.estado == "Activo" and estadoNew == "Comprometida" and self.hayItemRevision(lineaBase):
            lineaBase.estado = estadoNew 
            db.session.commit()
        if estadoNew == "Finalizado" and self.hayItemEliminado(lineaBase):    
            lineaBase.estado = estadoNew
            db.session.commit()
        
    def asignarItems(self, lineaBase, lista):
        for itm in lista:
            lineaBase.itemsLB.append(itm)
        db.session.commit()
        
    def desAsignarItems(self, nombre):
        lineaBase = LineaBase.query.filter(LineaBase.nombre == nombre).first_or_404()
        lineaBase.itemsLB = []
        
        db.session.commit()
        
    def modificar(self, lineaBase, nombreNew, descripcionNew):
        lineaBase.nombre = nombreNew
        lineaBase.descripcion = descripcionNew
        db.session.commit()
        
    def existe(self, lb):
        l = LineaBase.query.filter(and_(LineaBase.nombre == lb.nombre, LineaBase.faseId == lb.faseId)).first()
        if l != None:
            return True
        else:
            return False
    
    def itemsDeLB(self, lineaBase):
        return lineaBase.itemsLB
    
    def hayItemRevision(self, lineaBase):
        for i in self.itemsDeLB(lineaBase):
            item = Item.query.filter(Item.idItem == i.idItem).first_or_404()
            if item.estado == "Revision":
                return True
        return False
            
    def hayItemEliminado(self, lineaBase):
        for i in self.itemsDeLB(lineaBase):
            item = Item.query.filter(Item.idItem == i.idItem).first_or_404()
            if item.estado == "Eliminado":
                return True
        return False        
