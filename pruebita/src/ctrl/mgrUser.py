from modulo import *

class MgrUser():

    def listar(self):
        return User.query.all()
    
    def guardar(self, usuario):
        db.session.add(usuario)
        db.session.commit()
    
    def estado(self, nombre, estadoNew):
        user = User.query.filter(User.name == nombre).first_or_404()
        user.estado = estadoNew        
        db.session.commit()
    
    def borrar(self,nombre):
        user = User.query.filter(User.name == nombre).first_or_404()
        db.session.delete(user)
        db.session.commit()
        
    def modificar(self, nombre, nameNew, passwordNew, nombreNew, apellidoNew,
                    emailNew, telefonoNew, obsNew):
        user = User.query.filter(User.name == nombre).first_or_404()
        user.name = nameNew
        user.password = passwordNew
        user.nombre = nombreNew
        user.apellido = apellidoNew
        user.email = emailNew
        user.telefono = telefonoNew
        user.obs = obsNew        
        db.session.commit()
        
    def filtrar(self, nombre):
        return User.query.filter(User.name == nombre).first_or_404()
    
    def rolDeUser(self, nombre, nombreProyecto):
        usr = User.query.filter(User.name == nombre).first_or_404()
        for r in usr.roles:
            rol = Rol.query.filter(Rol.idRol == r.idRol, Rol.ambito == nombreProyecto).first()
            if not rol == None:
                return rol
    
