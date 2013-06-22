import os
from datetime import datetime
from pruebita import db, app

class Permiso(db.Model):
    """ Modelo de Permiso """
    __tablename__ = 'Permiso'
    
    idPermiso = db.Column(db.Integer, primary_key=True,nullable=False)
    nombre = db.Column(db.String(45), unique=True,nullable=False)
    descripcion = db.Column(db.String(150))
    
    def __init__(self, nombre=None, descripcion=None):
        """ constructor de Permiso """
        self.nombre = nombre
        self.descripcion = descripcion
    
    def __repr__(self):
        return self.nombre
    