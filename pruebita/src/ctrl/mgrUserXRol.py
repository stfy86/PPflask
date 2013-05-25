from pruebita import db, app

class MgrUserXRol():

    def guardar(self, usuarioName, rolNombre):
        """ asigna un rol a un usuario"""
        from models import User, Rol, roles
        user = User.query.filter(User.name == usuarioName).first_or_404()
        rol = Rol.query.filter(Rol.nombre == rolNombre).first_or_404() 
        user.roles.append(rol)
        db.session.commit()         
        
    def borrar(self, usuarioName, rolNombre):
        """ desasigna un rol a un usuario"""
        from models import User, Rol, roles
        user = User.query.filter(User.name == usuarioName).first_or_404()
        rol = Rol.query.filter(Rol.nombre == rolNombre).first_or_404() 
        user.roles.remove(rol)
        db.session.commit()    
        