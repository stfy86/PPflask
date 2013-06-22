from modulo import *

class MgrUser():

    def listar(self):
        return User.query.all()
    
    def guardar(self, user):
        db.session.add(user)
        db.session.commit()
        
    def borrar(self, user):
        if user.estado == "Inactivo":
            db.session.delete(user)
            db.session.commit()
            return ":borro el usuario:"
        else:
            return ":no borro:"
            
        
    def modificar(self, name, nameNew, passwordNew, nombreNew, apellidoNew,
                    emailNew, telefonoNew, obsNew):
        user =  self.filtrar(name)
        if user.estado == "Inactivo":
            user.password = passwordNew
            user.nombre = nombreNew
            user.apellido = apellidoNew
            user.email = emailNew
            user.telefono = telefonoNew
            user.obs = obsNew        
            db.session.commit()
            return ":modifico:"
        else:
            return ":no modifico:"
        
    def filtrar(self, name):
        return User.query.filter(User.name == name).first_or_404()
    
    
    def listarActivo(self):
        return User.query.filter(User.estado == "Activo").all()
    
    def estado(self, name, estadoNew):
        user = self.filtrar(name)
        if estadoNew == "Activo" and self.ceroRol(name) > 0:
            user.estado = estadoNew        
            db.session.commit()
            return ":cambio de estado:"
        if estadoNew == "Inactivo" and self.ceroRol(name) == 0:
            user.estado = estadoNew        
            db.session.commit()
            return ":cambio de estado:"    
        return ":no cambio de estado:"
    
   
    def existeRol(self, name, idRol):
        rol = Rol.query.filter(Rol.idRol == idRol).first()
        user = self.filtrar(name)
        if rol in user.roles:
            return True
        else:
            return False
    
    def ceroRol(self, name):
        user = self.filtrar(name)
        cont = 0
        for rol in user.roles:
            cont = cont + 1
        return cont
        
    def addRol(self, name, rol):  
        user = self.filtrar(name)
        if self.existeRol(name, rol.idRol):
            return ":ya tiene asignado ese rol:"
        else:
            user.roles.append(rol)
            user.estado = "Activo"
            db.session.commit()
            return ":asigno el rol:"
        
    def removeRol(self, name, rol):   
        user = self.filtrar(name)
        if self.existeRol(name, rol.idRol):
            user.roles.remove(rol)
            db.session.commit()
            if self.ceroRol(name) == 0:
                user.estado = "Inactivo"
                db.session.commit()              
            return ":removio el rol:"
        else:
            return ":no removio el rol:"
        
    def rolDeUser(self, name, nombreProyecto):
        user = self.filtrar(name)
        for rol in user.roles:
            if rol.ambito == nombreProyecto:
                return rol
        return None
