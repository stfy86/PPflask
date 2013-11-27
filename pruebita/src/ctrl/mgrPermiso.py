from modulo import *

class MgrPermiso():
    
    def listar(self):
        return Permiso.query.all()
    
    def guardar(self, permiso):
        db.session.add(permiso)
        db.session.commit()
    
    def borrar(self, nombre):
        permiso = Permiso.query.filter(Permiso.nombre == nombre).first_or_404()
        db.session.delete(permiso)
        db.session.commit()
    
    
    def filtrar(self, nombre):
        permiso =  Permiso.query.filter(Permiso.nombre == nombre).first()
        return permiso
    
    def filtrarXModulo(self, modulo):
        permiso = []
        if modulo == "ModuloAdministracion":
            permiso =  Permiso.query.filter(Permiso.tipoPermiso == 1).all()
        if modulo == "ModuloGestion":
            permiso =  Permiso.query.filter(Permiso.tipoPermiso == 2).all()
        if modulo == "ModuloDesarrollo":
            permiso =  Permiso.query.filter(Permiso.tipoPermiso == 3).all()
        return permiso
    
    def getlistaPermiso(self, lista):   
        perm = []
        for p in lista:
            perm.append(self.filtrarXId(p))
        return perm
    
    def filtrarXId(self, idPermiso):
        return Permiso.query.filter(Permiso.idPermiso == idPermiso).first()
        