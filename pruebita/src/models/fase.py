import os
from datetime import datetime
from pruebita import db, app

class Fase(db.Model):
    """ Modelo de Fase """
    __tablename__ = 'Fase'
    
    idFase = db.Column(db.Integer, primary_key=True, nullable=False)
    nombre = db.Column(db.String(45), unique=True, nullable=False)
    descripcion = db.Column(db.String(150))
    estado = db.Column(db.String(20), default ='Pendiente', nullable=False)
    orden = db.Column(db.Integer, nullable=False)
    fechaDeCreacion = db.Column(db.DateTime, default = datetime.now(), nullable=False) 
    
    # one to many: Relaciona Proyecto x Fase
    proyectoId = db.Column(db.Integer, db.ForeignKey('Proyecto.idProyecto'))

    # one to many: Relaciona Tipo de Item x Fase
    tipoDeItemId = db.Column(db.Integer, db.ForeignKey('TipoDeItem.idTipoDeItem'))
    
    # one to many: Relaciona Fase x Item
    listaItem = db.relationship('Item', backref='Fase', lazy = 'dynamic')
    
    # one to many: Relaciona Fase x Linea Base
    listaLineaBase = db.relationship('LineaBase', backref='Fase', lazy = 'dynamic')
        
    

    def __init__(self, nombre=None, descripcion=None, orden=None, proyectoId=None, tipoDeItemId=None):
        """ constructor de fase """
        self.nombre = nombre
        self.descripcion = descripcion
        self.orden = orden
        self.proyectoId = proyectoId
        self.tipoDeItemId = tipoDeItemId
    
    def __repr__(self):
        return self.nombre
  

