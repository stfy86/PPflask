from pruebita import db, app

class MgrLineaBase():

    def guardar(self, lineaBase):
        """ guarda un registro fase """
        db.session.add(lineaBase)
        db.session.commit()
    
    def borrar(self,nombre):
        """ borra un registro fase x name"""
        from models import LineaBase
        lineaBase = LineaBase.query.filter(LineaBase.nombre == nombre).first_or_404()
        db.session.delete(lineaBase)
        db.session.commit()

    def listar(self):
        from models import LineaBase
        return LineaBase.query.all()
    
    def filtrar(self, nombre):
        """ filtrar fase por nombre """
        from models import LineaBase
        return LineaBase.query.filter(LineaBase.nombre == nombre).first_or_404()

    def estado(self, nombre, estadoNew):
        """ guarda el nuevo estado de la fase """
        from models import LineaBase
        lineaBase = LineaBase.query.filter(LineaBase.nombre == nombre).first_or_404()
        lineaBase.estado = estadoNew        
        db.session.commit()
        
    def asignarItems(self, nombre, lista):
        from models import LineaBase
        from models import Item
        from ctrl.mgrItem import MgrItem

        lineaBase = LineaBase.query.filter(LineaBase.nombre == nombre).first_or_404()
        for itm in lista:
            item = MgrItem().filtrar(itm)
            lineaBase.itemsLB.append(item)
        
        lineaBase.estado = 'Activo'
        db.session.commit()
        
    def desAsignarItems(self, nombre):
        from models import LineaBase
        
        lineaBase = LineaBase.query.filter(LineaBase.nombre == nombre).first_or_404()
        lineaBase.itemsLB = []
        
        db.session.commit()
        
    def modificar(self, nombre, nombreNew, descripcionNew):
        """ modificar un registro de linea base """
        from models import LineaBase 
        lineaBase = LineaBase.query.filter(LineaBase.nombre == nombre).first_or_404()
        lineaBase.nombre = nombreNew
        lineaBase.descripcion = descripcionNew
        db.session.commit()