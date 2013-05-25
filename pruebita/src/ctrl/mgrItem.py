from pruebita import db, app

class MgrItem():

    def listar(self):
        """ listar items """
        from models import Item
        return Item.query.all()
    
    def guardar(self, item):
        """ guarda un registro tipoDeItem """
        db.session.add(item)
        db.session.commit()
        
    def estado(self, nombre, estadoNew):
        """ guarda el nuevo estado del usuario """
        from models import Item
        item = Item.query.filter(Item.nombre == nombre).first_or_404()
        item.estado = estadoNew        
        db.session.commit()
    
    def borrar(self,nombre):
        """ borra un registro tipoDeItem x name"""
        from models import Item
        item = Item.query.filter(Item.nombre == nombre).first_or_404()
        db.session.delete(item)
        db.session.commit()
        
    def modificar(self, nombre, nombreNew, versionNew, complejidadNew, costoNew):
        """ modificar un registro de tipo de item"""
        from models import Item
        item = Item.query.filter(Item.nombre == nombre).first_or_404()
        item.nombre = nombreNew
        item.version = versionNew
        item.complejidad = complejidadNew
        item.costo = costoNew
        db.session.commit()

    def filtrar(self, nombre):
        """ filtrar proyecto por nombre """
        from models import Item
        return Item.query.filter(Item.nombre == nombre).first_or_404()
    
    def asignarTipoDeItem2(self, nombre, id):
        """ asigna un tipo de item a un item """
        from models import Item, TipoDeItem
        item = Item.query.filter(Item.nombre == nombre).first_or_404()
        tipoItem = TipoDeItem.query.filter(TipoDeItem.idTipoDeItem == id).first_or_404()
        # asigna al item el tipo de item 
        item.tipoDeItem = tipoItem
        db.session.commit()
            
                
    def filtrarTipoDeItem(self, nombre):
        """ filtrar rol por nombre """
        from models import Item
        item = Item.query.filter(Item.nombre == nombre).first_or_404()
        return item.tipoDeItemId

    def filtrarAprobadoXFase(self, faseId):
        """ filtrar proyecto por fase """
        from models import Item
        from sqlalchemy import and_
        return Item.query.filter(and_(Item.faseId == faseId, Item.estado == 'Aprobado'))