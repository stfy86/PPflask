from pruebita import db, app

class MgrTipoDeItemXTipoDeAtrib():
 
    def guardar(self, tipoDeItemNombre, tipoDeAtribNombre):
        """ asigna a un item un tipo de atributo"""
        from models import TipoDeItem, TipoDeAtributo, atributosItem
        tipoDeItem = TipoDeItem.query.filter(TipoDeItem.nombre == tipoDeItemNombre).first_or_404()
        tipoDeAtrib= TipoDeAtributo.query.filter(TipoDeAtributo.nombre == tipoDeAtribNombre).first_or_404() 
        tipoDeItem.atributosItem.append(tipoDeAtrib)
        db.session.commit()
    
    def borrar(self,  tipoDeItemNombre, tipoDeAtribNombre):
        """ borra un tipo de atributo que a sido asignado a un tipo de item"""
        from models import TipoDeItem, TipoDeAtributo, atributosItem
        tipoDeItem = TipoDeItem.query.filter(TipoDeItem.nombre == tipoDeItemNombre).first_or_404()
        tipoDeAtrib= TipoDeAtributo.query.filter(TipoDeAtributo.nombre == tipoDeAtribNombre).first_or_404() 
        tipoDeItem.atributosItem.remove(tipoDeAtrib)
        db.session.commit()
    



