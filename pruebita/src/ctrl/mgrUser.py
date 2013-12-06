""" Clase que maneja los Usuarios"""
from modulo import *

class MgrUser():

    def listar(self):
        return User.query.all()
    
    def guardar(self, user):
        if not self.existe(user):
            db.session.add(user)
            db.session.commit()
            return ":guardo usuario:"
        else:
            return ":NO guardo usuario:"
        
    def borrar(self, user):
        if self.existe(user) and user.estado == "Inactivo" and user.name != "admin":
            db.session.delete(user)
            db.session.commit()
            return ":borro usuario:"
        else:
            return ":NO borro usuario:"
            
        
    def modificar(self, user, passwordNew, confirmacionNew, nombreNew, apellidoNew,
                    emailNew, telefonoNew, obsNew):       
        if user.estado == "Inactivo":
            user.password = passwordNew
            user.confirmacion = confirmacionNew
            user.nombre = nombreNew
            user.apellido = apellidoNew
            user.email = emailNew
            user.telefono = telefonoNew
            user.obs = obsNew        
            db.session.commit()
            return ":modifico usuario:"
        else:
            return ":NO modifico usuario: estado inactivo de usuario" 
        
    def filtrar(self, name):
        return User.query.filter(User.name == name).first_or_404()
    
    
    def listarActivo(self):
        return User.query.filter(User.estado == "Activo").all()
    
    def estado(self, user, estadoNew):
        if estadoNew == "Activo" and self.ceroRol(user) > 0:
            user.estado = estadoNew        
            db.session.commit()
            return ":cambio estado de usuario:"
        if estadoNew == "Inactivo" and self.ceroRol(user) == 0:
            user.estado = estadoNew        
            db.session.commit()
            return ":cambio estado de usuario:"
        return ": NO cambio estado de usuario:"
    
   
    def existeRol(self, user, idRol):
        rol = Rol.query.filter(Rol.idRol == idRol).first()
        if rol in user.roles:
            return True
        else:
            return False
    
    def ceroRol(self, user):
        cont = 0
        for rol in user.roles:
            cont = cont + 1
        return cont
        
    def addRol(self, user, rol):  
        if self.existeRol(user, rol.idRol):
            return ":ya tiene asignado ese rol:"
        else:
            user.roles.append(rol)
            user.estado = "Activo"
            db.session.commit()
            return ":asigno el rol:"
        
    def removeRol(self, user, rol):   
        if self.existeRol(user, rol.idRol):
            user.roles.remove(rol)
            db.session.commit()
            if self.ceroRol(name) == 0:
                user.estado = "Inactivo"
                db.session.commit()              
            return ":removio el rol:"
        else:
            return ":no removio el rol:"
        
    def rolDeUser(self, user, nombreProyecto):
        for rol in user.roles:
            if rol.ambito == nombreProyecto:
                return rol
        return None

    def existe(self, user):
        u = User.query.filter(User.name == user.name).first()
        if u != None:
            return True
        else:
            return False

    def filtrarXId(self,idUser):
        return User.query.filter(User.idUser == idUser).first_or_404()
    
    def proyectoDeUser(self, user):
        lista = []        
        for rol in user.roles:
            proyecto = Proyecto.query.filter(Proyecto.nombre == rol.ambito).first_or_404()
            lista.append(proyecto)
        return lista