from pruebita import db, app

class MgrRol():
    
    def listar(self):
        """ listar roles """
        from models import Rol
        return Rol.query.all()

    def guardar(self, rol):
        """ guarda un registro rol """
        db.session.add(rol)
        db.session.commit()
    
    def borrar(self,nombre):
        """ borra un registro de rol"""
        from models import Rol
        rol = Rol.query.filter(Rol.nombre == nombre).first_or_404()
        db.session.delete(rol)
        db.session.commit()

    def modificar(self, nombre, nombreNew, ambitoNew, descripcionNew):
        """ modificar un registro de rol"""
        from models import Rol
        rol = Rol.query.filter(Rol.nombre == nombre).first_or_404()
        rol.nombre = nombreNew
        rol.ambito = ambitoNew
        rol.descripcion = descripcionNew
        db.session.commit()
        
    def filtrar(self, nombre):
        """ filtrar rol por nombre """
        from models import Rol
        return Rol.query.filter(Rol.nombre == nombre).first_or_404()
    
