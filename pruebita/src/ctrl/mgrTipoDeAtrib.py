from modulo import *

class MgrTipoDeAtrib():

    def listar(self):
        return TipoDeAtributo.query.all()
    
    def guardar(self, tipoDeAtributo):
        db.session.add(tipoDeAtributo)
        db.session.commit()
    
    def borrar(self,nombre):
        tipoDeAtributo = TipoDeAtributo.query.filter(TipoDeAtributo.nombre == nombre).first_or_404()
        db.session.delete(tipoDeAtributo)
        db.session.commit()
        
    def modificar(self, nombre, nombreNew, tipoDeDatoNew, detalleNew,
                    descripcionNew):
        atrib = TipoDeAtributo.query.filter(TipoDeAtributo.nombre == nombre).first_or_404()
        atrib.nombre = nombreNew
        atrib.tipoDeDato = tipoDeDatoNew
        atrib.detalle = detalleNew
        atrib.descripcion = descripcionNew     
        db.session.commit()

    def filtrar(self, nombre):
        return TipoDeAtributo.query.filter(TipoDeAtributo.nombre == nombre).first_or_404()
