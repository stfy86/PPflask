from modulo import *
from sqlalchemy import or_, and_

class MgrRol():
    
    def listar(self):
        return Rol.query.all()

    def guardar(self, rol):
        if not self.existe(rol):
            db.session.add(rol)
            db.session.commit()
            return ":guardo el rol:"
        else:
            return ":No guardo el rol:"

    def borrar(self, rol):
        if self.existe(rol) and rol.nombre != "LiderDeProyecto" and rol.nombre != "Administracion":
            db.session.delete(rol)
            db.session.commit()
            return ":borro el rol:"
        else:   
            return ":NO borro:"

    def modificar(self, idRol, nombreNew, ambitoNew, descripcionNew, permisosNew):
        rol = self.filtrarXId(idRol)
        rol.nombre = nombreNew
        rol.ambito = ambitoNew
        rol.descripcion = descripcionNew
        rol.permisos = permisosNew;
        db.session.commit()
        return ":modifico el rol:"
        
    def filtrar(self, nombre):
        return Rol.query.filter(Rol.nombre == nombre).first_or_404()
    
    def filtrarXId(self, idRol):
        return Rol.query.filter(Rol.idRol == idRol).first_or_404()
    
    def getPermisos(self, rol):
        return rol.permisos

    
    def search(self, nombre, ambito):
        return Rol.query.filter(and_(Rol.nombre == nombre, Rol.ambito == ambito)).first_or_404()
        
    def listarPorAmbito(self, ambito):
        return Rol.query.filter(Rol.ambito == ambito).all()
    
    def config(self, rol, listaMarcada=[None]):
        if listaMarcada == None:
            return "NO se configuro"
        else:
            for perm in self.getPermisos(rol):
                if perm in listaMarcada:
                    self.asignarPermiso(rol, perm)
                else:
                    self.desasignarPermiso(rol, perm)
            return "se configuro el rol"
        
    def asignarPermiso(self, rol, permiso ):
        if not permiso in rol.permisos:
            rol.permisos.append(permiso)
            db.session.commit()  
            return ":asigno permiso a rol:"
        else:
            return ":error: no asigno permiso al rol"

        
    def desasignarPermiso(self, rol, permiso ):
        if permiso in rol.permisos:
            rol.permisos.remove(permiso)
            db.session.commit()  
            return ":desasigno permiso del rol:"
        else:
            return ":error: no desasigno"
                
    def existe(self, rol):
        r = Rol.query.filter(and_(Rol.nombre == rol.nombre, Rol.ambito == rol.ambito)).first()
        if r != None:
            return True
        else:
            return False

          
    def listarPermisos(self, idRol):
        lista = []
        rol = self.filtrarXId(idRol)
        for perm in rol.permisos:
            lista.append(perm)
        return lista     

    def listarNombrePermisos(self, idRol):
        lista = []
        rol = self.filtrarXId(idRol)
        for perm in rol.permisos:
            lista.append(perm.nombre)
        return lista    
    
   
    def modificarPermiso(self, idRol, lista):
        rol = self.filtrarXId(idRol)
        for p in rol.permisos:
            self.desasignarPermiso(rol, p)
        for p in lista:
            self.asignarPermiso(rol, p)
        return "Modifico los permisos del rol"
