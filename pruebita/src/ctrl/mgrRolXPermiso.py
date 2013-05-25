from pruebita import db, app

class MgrRolXPermiso():
 
    def guardar(self, rolNombre, permisoNombre):
        """ asigna a un rol un permiso"""
        from models import Rol, Permiso, permisos
        rol = Rol.query.filter(Rol.nombre == rolNombre).first_or_404()
        permiso = Permiso.query.filter(Permiso.nombre == permisoNombre).first_or_404() 
        rol.permisos.append(permiso)
        db.session.commit()
    
    def borrar(self, rolNombre, permisoNombre):
        """ borra un permiso que a sido asignado a un rol"""
        from models import Rol, Permiso, permisos
        rol = Rol.query.filter(Rol.nombre == rolNombre).first_or_404()
        permiso = Permiso.query.filter(Permiso.nombre == permisoNombre).first_or_404() 
        rol.permisos.remove(permiso)
        db.session.commit()
    



