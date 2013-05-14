from pruebita import db, app

class MgrTipoDeItem():

    def listar(self):
        """ listar items """
        from models import TipoDeItem
        return TipoDeItem.query.all()
    
    def guardar(self, tipoDeItem):
        """ guarda un registro tipoDeItem """
        db.session.add(tipoDeItem)
        db.session.commit()
    
    def borrar(self,nombre):
        """ borra un registro tipoDeItem x name"""
        from models import TipoDeItem
        tipoDeItem = TipoDeItem.query.filter(TipoDeItem.nombre == nombre).first_or_404()
        db.session.delete(tipoDeItem)
        db.session.commit()
        
    def modificar(self, nombre, nombreNew, descripcionNew):
        """ modificar un registro de tipo de item"""
        from models import TipoDeItem
        tipoDeItem = TipoDeItem.query.filter(TipoDeItem.nombre == nombre).first_or_404()
        tipoDeItem.nombre = nombreNew
        tipoDeItem.descripcion = descripcionNew     
        db.session.commit()

    def filtrar(self, nombre):
        """ filtrar proyecto por nombre """
        from models import TipoDeItem
        return TipoDeItem.query.filter(TipoDeItem.nombre == nombre).first_or_404()
