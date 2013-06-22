import os
from datetime import datetime
from pruebita import db, app

# permisos de un rol
permisos = db.Table('permisos', \
    db.Column('idRol',db.Integer, db.ForeignKey('Rol.idRol')),
    db.Column('idPermiso',db.Integer, db.ForeignKey('Permiso.idPermiso'))
    )
  
class Rol(db.Model):
    """ Modelo de Rol """
    __tablename__ = 'Rol'
    
    idRol = db.Column(db.Integer, primary_key=True, nullable=False)
    nombre = db.Column(db.String(45), nullable=False)
    ambito = db.Column(db.String(45)) # corresponde al proyecto en el cual se creo
    descripcion = db.Column(db.String(150))
    
    # many to many: Relaciona Rol x Permiso
    permisos = db.relationship('Permiso', secondary = permisos, backref= db.backref('roles' , lazy='dynamic'))
     
    def __init__(self, nombre=None, descripcion=None, ambito=None):
        """ constructor de Rol con permisos"""
        self.nombre = nombre
        self.ambito = ambito
        self.descripcion = descripcion
        
    def __repr__(self):
        return self.nombre