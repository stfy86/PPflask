from modulo import *
from sqlalchemy import or_, and_

class MgrRol():
    
    def listar(self):
        return Rol.query.all()

    def guardar(self, rol):
        if not rol in self.listar():
            db.session.add(rol)
            db.session.commit()
            return ":guardo el rol:"
        else:
            return ":NO guardo el rol:"

    def borrar(self, rol):
        if rol in self.listar():
            db.session.delete(rol)
            db.session.commit()
            return ":borro:"
        else:   
            return ":NO borro:"

    def modificar(self, idRol, nombreNew, ambitoNew, descripcionNew):
        rol = self.filtrarXId(idRol)
        rol.nombre = nombreNew
        rol.ambito = ambitoNew
        rol.descripcion = descripcionNew
        db.session.commit()
        return ":modifico el rol:"
        
    def filtrar(self, nombre):
        return Rol.query.filter(Rol.nombre == nombre).first_or_404()
    
    def filtrarXId(self, idRol):
        return Rol.query.filter(Rol.idRol == idRol).first_or_404()
    
    def getPermisos(self, rol):
        return rol.permisos

    def delete(self, rol):
        db.session.delete(rol)
        db.session.commit()
        
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
                

                
