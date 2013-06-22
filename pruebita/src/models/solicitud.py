import os
from datetime import datetime
from pruebita import db, app

itemsSolicitud = db.Table('itemsSolicitud', \
    db.Column('idSolicitud',db.Integer, db.ForeignKey('Solicitud.idSolicitud')),
    db.Column('idItem',db.Integer, db.ForeignKey('Item.idItem'))
    )

class Solicitud(db.Model):
    """ Modelo de Solicitud"""
    __tablename__ = 'Solicitud'
    
    idSolicitud = db.Column(db.Integer, primary_key=True, nullable=False)
    nombre = db.Column(db.String(45), unique=True, nullable=False)
    descripcion = db.Column(db.String(150))
    estado = db.Column(db.String(20), default ='Pendiente', nullable=False)
    votosPositivos = db.Column(db.Integer)
    votosNegativos = db.Column(db.Integer)
    
    # one to many : Relaciona Solicitud x User
    autorId = db.Column(db.Integer, db.ForeignKey('User.idUser'))
    Autor = db.relationship("User", backref=db.backref("Solicitudes"))
    
    # many to many: Relaciona Solicitud x Item
    itemsSolicitud = db.relationship('Item', secondary = itemsSolicitud,
        backref= db.backref('solicitudes' , lazy='dynamic'))
        
    # one to many : Relaciona Comite x Solicitud
    comiteId = db.Column(db.Integer, db.ForeignKey('Comite.idComite'))
    Comite = db.relationship("Comite", backref=db.backref("Solicitudes"))
    

        
    def __init__(self, nombre=None, descripcion=None, votosPositivos=None, votosNegativos=None, autorId=None, itemsSolicitud =[None], comiteId=None):
        """ constructor de solicitud """
        self.nombre = nombre
        self.description = descripcion
        self.votosNegativos = votosNegativos
        self.votosPositivos = votosPositivos
        self.autorId = autorId
        self.itemsSolicitud = itemsSolicitud
        self.comiteId = comiteId
        
    def __repr__(self):
        return self.nombre  
    