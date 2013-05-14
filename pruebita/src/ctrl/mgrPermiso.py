from pruebita import db, app

class MgrPermiso():

    def guardar(self, permiso):
        """ guarda un registro permiso """
        db.session.add(permiso)
        db.session.commit()
    
    def borrar(self,nombre):
        """ borra un registro permiso x name"""
        from models import Permiso
        permiso = Permiso.query.filter(Permiso.nombre == nombre).first_or_404()
        db.session.delete(permiso)
        db.session.commit()


