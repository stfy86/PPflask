from modulo import *
from sqlalchemy import or_, and_

class MgrLineaBase():

    def guardar(self, lineaBase):
        """ Guarda una linea base solo si:
        1. La fase esta Activa
        2. No existe ya una linea base con el mismo nombre en la fase"""
        f = Fase.query.filter(Fase.idFase == lineaBase.faseId).first_or_404()
        if f.estado != "Activo" or self.existe(lineaBase):
            return ":No guardo linea base:"
        else:
            lineaBase.estado = "Activo"
            db.session.add(lineaBase)
            db.session.commit()
            return ":guardo linea base:"
    
    def borrar(self, lineaBase):
        """ Borra una linea base solo si:
        1. El estado de la fase este distinto de Finalizado
        2. Existe la linea base
        """
        f = Fase.query.filter(Fase.idFase == lineaBase.faseId).first_or_404()
        if not self.existe(lineaBase):
            return ":NO borro la linea base: la linea base no existe"
        if f.estado == "Finalizado":
            return ":NO borro la linea base: la fase tiene estado Finalizado"            
        else:
            lineaBase.estado="Inactivo"
            for i in self.itemsDeLB(lineaBase):
                item = Item.query.filter(Item.idItem == i.idItem).first()
                item.estado = "Revision"
            db.session.commit()
            return ":borro la linea base:"
        
    def listar(self):
        """ Lista todas las lineas base """
        return LineaBase.query.all()
    
    def filtrar(self, nombre):
        """Busca la linea base por nombre"""
        return LineaBase.query.filter(LineaBase.nombre == nombre).first_or_404()

    def filtrarXId(self, idLineaBase):
        """Busca la linea base por id """
        return LineaBase.query.filter(LineaBase.idLineaBase == idLineaBase).first_or_404()

    def estado(self, lineaBase, estadoNew):
        """Cambia el estado de una linea base"""
        if not self.existe(lineaBase):
            return ":NO modifico de estado: la lb no existe"
        if lineaBase.estado == "Activo" and estadoNew == "Comprometida" and self.hayItemRevision(lineaBase):
            lineaBase.estado = estadoNew 
            db.session.commit()
            return ":modifico el estado: Activo a Comprometida"
        if estadoNew == "Finalizado" and self.hayItemEliminado(lineaBase):    
            lineaBase.estado = estadoNew
            db.session.commit()
            return ":modifico el estado: Finalizado a " + estadoNew
        if estadoNew == "Inactivo":
            lineaBase.estado="Inactivo"
            for i in self.itemsDeLB(lineaBase):
                item = Item.query.filter(Item.idItem == i.idItem).first()
                item.estado = "Revision"
            db.session.commit()    
        return ":NO modifico el estado:"
        
    def asignarItems(self, lineaBase, lista):
        """ Asigna items a una linea base """
        for itm in lista:
            lineaBase.itemsLB.append(itm)
        db.session.commit()
        return ":asigno items a la linea base:"
        
    def desAsignarItems(self, nombre):
        """ Des asigna items de una linea base """
        lineaBase = LineaBase.query.filter(LineaBase.nombre == nombre).first_or_404()
        lineaBase.itemsLB = []        
        db.session.commit()
        return ":des asigno items a la linea base:"
        
    def modificar(self, lineaBase, nombreNew, descripcionNew):
        """Edita los datos de la linea base """
        if not self.existe(lineaBase):
            return ":NO modifico la linea base: la linea base no existe"
        else:
            lineaBase.nombre = nombreNew
            lineaBase.descripcion = descripcionNew
            db.session.commit()
            return ":mofidico los datos de la linea base:"
        
    def existe(self, lb):
        """ Retorna True si la linea base existe """
        l = LineaBase.query.filter(and_(LineaBase.nombre == lb.nombre, LineaBase.faseId == lb.faseId)).first()
        if l != None:
            return True
        else:
            return False
    
    def itemsDeLB(self, lineaBase):
        """ Retorna la lista de items de la linea base """
        lista = []
        for i in lineaBase.itemsLB:
            lista.append(i)            
        return lista
    
    def hayItemRevision(self, lineaBase):
        """ Retorna True si existe un items en estado de Revision """
        for i in self.itemsDeLB(lineaBase):
            item = Item.query.filter(Item.idItem == i.idItem).first_or_404()
            if item.estado == "Revision":
                return True
        return False
            
    def hayItemEliminado(self, lineaBase):
        """ Retorna True si existe un item en estado Eliminado """
        for i in self.itemsDeLB(lineaBase):
            item = Item.query.filter(Item.idItem == i.idItem).first_or_404()
            if item.estado == "Eliminado":
                return True
        return False        
