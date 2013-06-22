from modulo import *

class MgrLineaBase():

    def guardar(self, lineaBase):
        db.session.add(lineaBase)
        db.session.commit()
    
    def borrar(self,nombre):
        lineaBase = LineaBase.query.filter(LineaBase.nombre == nombre).first_or_404()
        db.session.delete(lineaBase)
        db.session.commit()

    def listar(self):
        return LineaBase.query.all()
    
    def filtrar(self, nombre):
        return LineaBase.query.filter(LineaBase.nombre == nombre).first_or_404()

    def estado(self, nombre, estadoNew):
        lineaBase = LineaBase.query.filter(LineaBase.nombre == nombre).first_or_404()
        lineaBase.estado = estadoNew        
        db.session.commit()
        
    def asignarItems(self, nombre, lista):
        lineaBase = LineaBase.query.filter(LineaBase.nombre == nombre).first_or_404()
        for itm in lista:
            item = MgrItem().filtrar(itm)
            lineaBase.itemsLB.append(item)
      
        lineaBase.estado = 'Activo'
        db.session.commit()
        
    def desAsignarItems(self, nombre):
        lineaBase = LineaBase.query.filter(LineaBase.nombre == nombre).first_or_404()
        lineaBase.itemsLB = []
        
        db.session.commit()
        
    def modificar(self, nombre, nombreNew, descripcionNew):
        lineaBase = LineaBase.query.filter(LineaBase.nombre == nombre).first_or_404()
        lineaBase.nombre = nombreNew
        lineaBase.descripcion = descripcionNew
        db.session.commit()
