from pruebita import db, app

class MgrTipoDeAtrib():

    def listar(self):
        """ listar atributos """
        from models import TipoDeAtributo
        return TipoDeAtributo.query.all()
    
    def guardar(self, tipoDeAtributo):
        """ guarda un registro tipoDeAtributo """
        db.session.add(tipoDeAtributo)
        db.session.commit()
    
    def borrar(self,nombre):
        """ borra un registro tipoDeAtributo x name"""
        from models import TipoDeAtributo
        tipoDeAtributo = TipoDeAtributo.query.filter(TipoDeAtributo.nombre == nombre).first_or_404()
        db.session.delete(tipoDeAtributo)
        db.session.commit()
        
    def modificar(self, nombre, nombreNew, tipoDeDatoNew, detalleNew,
                    descripcionNew):
        """ modificar un registro de tipo de atributo"""
        from models import TipoDeAtributo
        atrib = TipoDeAtributo.query.filter(TipoDeAtributo.nombre == nombre).first_or_404()
        atrib.nombre = nombreNew
        atrib.tipoDeDato = tipoDeDatoNew
        atrib.detalle = detalleNew
        atrib.descripcion = descripcionNew     
        db.session.commit()

    def filtrar(self, nombre):
        """ filtrar proyecto por nombre """
        from models import TipoDeAtributo
        return TipoDeAtributo.query.filter(TipoDeAtributo.nombre == nombre).first_or_404()
