from pruebita import db, app

class MgrFase():

    def guardar(self, fase):
        """ guarda un registro fase """
        db.session.add(fase)
        db.session.commit()
    
    def guardarLista(self, fase = [None]):
        """ guarda varios registros fase """
        for f in fase:
            db.session.add(f)
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
    
    def listarXProyecto(self, nombreProyecto):
        from models import Fase, Proyecto
        proyecto = Proyecto.query.filter(Proyecto.nombre == nombre).first_or_404()    
        return Fase.query.filter(Fase.proyectoId == proyecto.idProyecto).all()
    
    def filtrar(self, nombre):
        """ filtrar fase por nombre """
        from models import Fase
        return Fase.query.filter(Fase.nombre == nombre).first_or_404()


    def estado(self, nombre, estadoNew):
        """ guarda el nuevo estado de la fase """
        from models import Fase
        fase = Fase.query.filter(Fase.nombre == nombre).first_or_404()
        fase.estado = estadoNew        
        db.session.commit()
        
    def filtrarItems(self, nombre):
        """ filtrar items por nombre """
        from models import Fase
        fase = Fase.query.filter(Fase.nombre == nombre)
        return fase.listaItem
