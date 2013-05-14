from pruebita import db, app

class MgrProject():

    def guardar(self, project):
        """ guarda un registro project """
        db.session.add(project)
        db.session.commit()
    
    def borrar(self,nombre):
        """ borra un registro project x name"""
        from models import Proyecto
        project = Proyecto.query.filter(Proyecto.nombre == nombre).first_or_404()
        db.session.delete(project)
        db.session.commit()
    
    def modificar(self, nombre, nombreNew, descripcionNew, presupuestoNew):
        """ modificar un registro project x name"""
        from models import Proyecto
        project = Proyecto.query.filter(Proyecto.nombre == nombre).first_or_404()
        project.nombre = nombreNew
        project.descripcion = descripcionNew
        project.presupuesto = presupuestoNew
        db.session.commit()
    
    def listar(self):
        """ listar proyectos """
        from models import Proyecto
        return Proyecto.query.all()

    def filtrar(self, nombre):
        """ filtrar proyecto por nombre """
        from models import Proyecto
        return Proyecto.query.filter(Proyecto.nombre == nombre).first_or_404()

    def estado(self, nombre, estadoNew):
        """ guarda el nuevo estado del usuario """
        from models import Proyecto
        proyecto = Proyecto.query.filter(Proyecto.nombre == nombre).first_or_404()
        proyecto.estado = estadoNew        
        db.session.commit()
