from pruebita import db, app

class MgrFase():

    def guardar(self, fase):
        """ guarda un registro fase """
        db.session.add(fase)
        db.session.commit()
    
    def borrar(self,nombre):
        """ borra un registro fase x name"""
        from models import Fase
        fase = Fase.query.filter(Fase.nombre == nombre).first_or_404()
        db.session.delete(fase)
        db.session.commit()
    
    def modificar(self, nombre, nombreNew, descripcionNew, ordenNew):
        """ modificar un registro fase x name"""
        from models import Fase
        fase = Fase.query.filter(Fase.nombre == nombre).first_or_404()
        fase.nombre = nombreNew
        fase.descripcion = descripcionNew
        fase.orden = ordenNew
        db.session.commit()

    def listar(self):
        from models import Fase
        return Fase.query.all()
    
    def filtrar(self, nombre):
        """ filtrar fase por nombre """
        from models import Fase
        return Fase.query.filter(Fase.nombre == nombre).first_or_404()
