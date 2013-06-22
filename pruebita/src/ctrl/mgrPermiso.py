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
        permiso =  Permiso.query.filter(Permiso.nombre == nombre).first_or_404()
        return permiso