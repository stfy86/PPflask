import os
from pruebita import db, app

class Relacion(db.Model):
    """ Modelo de Relacion"""
    __tablename__ = 'Relacion'

    # items de la relacion
    itemOrigenId = db.Column(db.Integer, db.ForeignKey('Item.idItem'), primary_key=True)  
    itemDestinoId = db.Column(db.Integer, db.ForeignKey('Item.idItem'), primary_key=True) 
    
    tipoDeRelacion = db.Column(db.String(20), nullable=False) # padre-hijo  e antecesor-sucesor
    estado = db.Column(db.String(20), default ='Pendiente', nullable=False)
  
    
    def __init__(self, nombre=None, tipoDeRelacion=None):
        self.nombre = nombre
        self.tipoDeRelacion = tipoDeRelacion

    def __repr__(self):
        return self.nombre

