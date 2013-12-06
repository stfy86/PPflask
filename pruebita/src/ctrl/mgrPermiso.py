from modulo import *

class MgrPermiso():
    
    def listar(self):
        """ Lista los permisos """
        return Permiso.query.all()
    
    def guardar(self, permiso):
        """ Guarda permiso """
        db.session.add(permiso)
        db.session.commit()
    
    def borrar(self, permiso):
        """ Borra permiso """
        db.session.delete(permiso)
        db.session.commit()
    
    
    def filtrar(self, nombre):
        """ Busca permiso por nombre """
        permiso =  Permiso.query.filter(Permiso.nombre == nombre).first()
        return permiso
    
    def filtrarXModulo(self, modulo):
        """ Busca permiso por modulo,retorna una lista """
        permiso = []
        if modulo == "ModuloAdministracion":
            permiso =  Permiso.query.filter(Permiso.tipoPermiso == 1).all()
        if modulo == "ModuloGestion":
            permiso =  Permiso.query.filter(Permiso.tipoPermiso == 2).all()
        if modulo == "ModuloDesarrollo":
            permiso =  Permiso.query.filter(Permiso.tipoPermiso == 3).all()
        return permiso
    
    def getlistaPermiso(self, lista):
        """ Retorna una lista de permiso del mismo id"""
        perm = []
        for p in lista:
            perm.append(self.filtrarXId(p))
        return perm
    
    def filtrarXId(self, idPermiso):
        """ Busca permiso por id """
        return Permiso.query.filter(Permiso.idPermiso == idPermiso).first()
        