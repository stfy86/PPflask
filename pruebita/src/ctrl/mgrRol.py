from modulo import *

class MgrRol():
    
    def listar(self):
        return Rol.query.all()

    def guardar(self, rol):
        for r in self.listarPorAmbito(rol.ambito):
            if r.nombre == rol.nombre :
                return ":error: rol ya creado en el proyecto"
        
        db.session.add(rol)
        db.session.commit()
        return ":guardo el rol:"
    
    def borrar(self, rol):
        if rol in self.listar():
            db.session.delete(rol)
            db.session.commit()
            return ":borro:"
        else:   
            return ":NO borro:"
  
    def modificar(self, nombre, nombreNew, ambitoNew, descripcionNew):
        rol = Rol.query.filter(Rol.nombre == nombre).first_or_404()
        rol.nombre = nombreNew
        rol.ambito = ambitoNew
        rol.descripcion = descripcionNew
        db.session.commit()
        
    def filtrar(self, nombre):
        return Rol.query.filter(Rol.nombre == nombre).first_or_404()
                
    def getPermisos(self, nombre):
        rol = Rol.query.filter(Rol.nombre == nombre).first_or_404()
        return rol.permisos

    def delete(self, rol):
        db.session.delete(rol)
        db.session.commit()
        
    def search(self, nombre, ambito):
        return Rol.query.filter(Rol.nombre == nombre, Rol.ambito == ambito).first_or_404()
        
    def listarPorAmbito(self, ambito):
        return Rol.query.filter(Rol.ambito == ambito).all()
    
    
    def asignarPermiso(self, nombre, ambito, nombrePermiso ):
        rol = Rol.query.filter(Rol.nombre == nombre, Rol.ambito == ambito).first_or_404()
        permiso = Permiso.query.filter(Permiso.nombre == nombrePermiso).first_or_404()
        if not permiso in rol.permisos:
            rol.permisos.append(permiso)
            db.session.commit()  
            return ":asigno permiso a rol:"
        else:
            return ":error: no asigno permiso al rol"

        
    def desasignarPermiso(self, nombre, ambito, nombrePermiso ):
        rol = Rol.query.filter(Rol.nombre == nombre, Rol.ambito == ambito).first_or_404()
        permiso = Permiso.query.filter(Permiso.nombre == nombrePermiso).first_or_404() 
        if permiso in rol.permisos:
            rol.permisos.remove(permiso)
            db.session.commit()  
            return ":desasigno permiso del rol:"
        else:
            return ":error: no desasigno"
                

                
