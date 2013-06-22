from modulo import *

class MgrFase():

    def guardar(self, fase):
        db.session.add(fase)
        db.session.commit()
               
    def borrar(self,nombre):
        fase = Fase.query.filter(Fase.nombre == nombre).first_or_404()
        db.session.delete(fase)
        db.session.commit()
    
    def modificar(self, nombre, nombreNew, descripcionNew, ordenNew):
        fase = Fase.query.filter(Fase.nombre == nombre).first_or_404()
        fase.nombre = nombreNew
        fase.descripcion = descripcionNew
        fase.orden = ordenNew
        db.session.commit()

    def listar(self):
        return Fase.query.all()
           
    def filtrar(self, nombre):
        return Fase.query.filter(Fase.nombre == nombre).first_or_404()

    def estado(self, nombre, estadoNew):
        fase = Fase.query.filter(Fase.nombre == nombre).first_or_404()
        fase.estado = estadoNew        
        db.session.commit()
