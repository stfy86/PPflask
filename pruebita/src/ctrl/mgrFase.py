from modulo import *

class MgrFase():

    def guardar(self, fase):
        proyecto = Proyecto.query.filter(Proyecto.idProyecto == fase.proyectoId).first_or_404()
        if proyecto.estado == "Pendiente":
            db.session.add(fase)
            db.session.commit()
            return ":guardo fase:"
        else:
            return ":NO guardo la fase:"
               
    def borrar(self, fase):
        proyecto = Proyecto.query.filter(Proyecto.idProyecto == fase.proyectoId).first_or_404()
        if proyecto.estado == "Pendiente":
            db.session.delete(fase)
            db.session.commit()
            return ":elimino la fase:"
        else:
            return ":NO se elimino la fase:"
    
    def modificar(self, fase,  descripcionNew, tipoDeItemIdNew):
        if fase.estado == "Pendiente":
            fase.descripcion = descripcionNew
            fase.tipoDeItemId = tipoDeItemIdNew
            db.session.commit()
            return ":modifico la fase:"
        else:
            return ":NO modifico la fase:"

    def listar(self):
        return Fase.query.all()
               
    def filtrar(self, nombre):
        return Fase.query.filter(Fase.nombre == nombre).first_or_404()

    def filtrarXId(self, idFase):
        return Fase.query.filter(Fase.idFase == idFase).first_or_404()

    def estado(self, fase, estadoNew):
        if fase.estado == "Activo" and estadoNew == "Finalizado" and self.itemsAprobados(fase):
            fase.estado = estadoNew        
            db.session.commit()
            return ":modifico estado: todos los items estan aprobados"
        if fase.estado == "Pendiente" and estadoNew == "Activo":
            fase.estado = estadoNew        
            db.session.commit()
            return ":modifico estado: desea crear items e ir aprobando los items"           
        if fase.estado == "Finalizado" and estadoNew == "Activo":
            fase.estado = estadoNew        
            db.session.commit()
            return ":modifico estado: desea modificar algun item de la fase"
        return ":NO modifico el estado:"
    
    def itemsAprobados(self, fase):
        for item in fase.listaItem:
            if item.estado != "Aprobado":
                return False
        return True