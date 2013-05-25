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
    

    def asignarPermiso(self, nombre, nombrePermiso):
        """ asigna un permiso a un rol """
        from ctrl.mgrRolXPermiso import MgrRolXPermiso
        # asigna al rol el permiso 
        MgrRolXPermiso().guardar(nombre, nombrePermiso) 
        
    def asignarPermiso2(self, nombre, listaPermiso=[None], listaSinPermiso=[None]):
        """ asigna un permiso a un rol """
        from models import Rol
        from ctrl.mgrRolXPermiso import MgrRolXPermiso
        # asigna al rol el permiso 
        for n in listaSinPermiso:
            MgrRolXPermiso().borrar(nombre, n.nombre) 
        for u in listaPermiso:
            MgrRolXPermiso().guardar(nombre, u)

    def desasignarPermiso(self, nombre, nombrePermiso):
        """ asigna un permiso a un rol """
        from ctrl.mgrRolXPermiso import MgrRolXPermiso
        # asigna al rol el permiso 
        MgrRolXPermiso().borrar(nombre, nombrePermiso) 
        
    
            
    def filtrarPermiso(self, nombre):
        """ filtrar rol por nombre """
        from models import Rol
        rol = Rol.query.filter(Rol.nombre == nombre).first_or_404()
        return rol.permisos