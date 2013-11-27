from modulo import *
from pruebita import app
from pruebita import db

class MgrSolicitud():

    def guardar(self, solicitud):
        """ guarda un registro solicitud """
        db.session.add(solicitud)
        db.session.commit()
    
    def borrar(self, nombre):
        """ borra un registro fase x name"""
        from models import Solicitud
        solicitud = Solicitud.query.filter(Solicitud.nombre == nombre).first_or_404()
        db.session.delete(solicitud)
        db.session.commit()

    def listar(self):
        return Solicitud.query.all()
    
    def filtrar(self, nombre):
        return Solicitud.query.filter(Solicitud.nombre == nombre).first_or_404()

    def por_id(self, id):
        return Solicitud.query.filter(Solicitud.idSolicitud == id).first_or_404()

    def estado(self, nombre, estadoNew):
        """ guarda el nuevo estado de la fase """
        solicitud = Solicitud.query.filter(Solicitud.nombre == nombre).first_or_404()
        solicitud.estado = estadoNew        
        db.session.commit()
        
    def asignarItems(self, nombre, lista):
        from models.solicitud import Solicitud
        from models.item import Item
        from ctrl.mgrItem import MgrItem

        solicitud = Solicitud.query.filter(Solicitud.nombre == nombre).first_or_404()
        for itm in lista:
            item = MgrItem().filtrar(itm)
            solicitud.itemsSolicitud.append(item)
        
        solicitud.estado = 'Pendiente'
        db.session.commit()
        
    def desAsignarItems(self, nombre):
        
        lineaBase = LineaBase.query.filter(LineaBase.nombre == nombre).first_or_404()
        lineaBase.itemsLB = []
        
        db.session.commit()
        
    def modificar(self, nombre, nombreNew, descripcionNew):
        """ modificar un registro de linea base """
        solicitud = Solicitud.query.filter(Solicitud.nombre == nombre).first_or_404()
        solicitud.nombre = nombreNew
        solicitud.descripcion = descripcionNew
        db.session.commit()