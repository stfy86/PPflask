from modulo import *
from pruebita import app
from pruebita import db

class MgrSolicitud():

    def guardar(self, solicitud):
        """ guarda un registro solicitud """
        db.session.add(solicitud)
        db.session.commit()
    
    def borrar(self, solicitud):
        db.session.delete(solicitud)
        db.session.commit()

    def listar(self):
        return Solicitud.query.all()
    
    def filtrar(self, nombre):
        return Solicitud.query.filter(Solicitud.nombre == nombre).first_or_404()

    def filtrarXId(self, id):
        return Solicitud.query.filter(Solicitud.idSolicitud == id).first_or_404()

    def estado(self, solicitud, estadoNew):
        """ guarda el nuevo estado de la fase """
        solicitud.estado = estadoNew        
        db.session.commit()
        
    def asignarItems(self, solicitud, lista):
        for id in lista:
            item = MgrItem().filtrarId(id)
            solicitud.items.append(item)
        db.session.commit()
        
    def modificar(self, solicitud, nombreNew, descripcionNew):
        """ modificar un registro de linea base """
        solicitud.nombre = nombreNew
        solicitud.descripcion = descripcionNew
        db.session.commit()

    def costoTotal(self, solicitud):
        t=0
        for i in solicitud.items:
           t=t+i.costo
        return t

    def complejidadTotal(self, solicitud):
        t=0
        for i in solicitud.items:
           t=t+i.complejidad
        return t
    
    def puedeEjecutar(self, comite, solicitud, user):
        nro = 0
        for u in comite.miembros:
            nro = nro +1            
        if solicitud.autorId == user.idUser and solicitud.votosPositivos == nro:
            return True
        else:
            return False