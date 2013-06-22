import os
from datetime import datetime
from pruebita import db, app

# ItemXLineaBase
itemsLB = db.Table('itemsLB', \
    db.Column('idLineaBase',db.Integer, db.ForeignKey('LineaBase.idLineaBase')),
    db.Column('idItem',db.Integer, db.ForeignKey('Item.idItem'))
    )
    
class LineaBase(db.Model):
    """ Modelo de Linea Base"""
    __tablename__ = 'LineaBase'
    
    idLineaBase = db.Column(db.Integer, primary_key=True, nullable=False)
    nombre = db.Column(db.String(45), unique=True, nullable=False)
    descripcion = db.Column(db.String(150))
    estado = db.Column(db.String(20), default ='Activo', nullable=False)
    
    # many to many: Relaciona LineaBase x Item
    itemsLB = db.relationship('Item', secondary = itemsLB,
        backref= db.backref('lineaBases' , lazy='dynamic'))
        
    # one to many: Relaciona Linea Base x fase
    faseId = db.Column(db.Integer, db.ForeignKey('Fase.idFase'))
 
    def __init__(self, nombre=None, descripcion=None, faseId=None):
        """ constructor de linea base """
        self.nombre = nombre
        self.descripcion = descripcion
        self.faseId = faseId

    def __repr__(self):
        return self.nombre
    
    
