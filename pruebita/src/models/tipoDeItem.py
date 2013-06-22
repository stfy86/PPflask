import os
from datetime import datetime
from pruebita import db, app

# tipoDeItem X TipoDeAtributo
atributosItem = db.Table('atributosItem', \
    db.Column('idTipoDeItem',db.Integer, db.ForeignKey('TipoDeItem.idTipoDeItem')),
    db.Column('idTipoDeAtributo',db.Integer, db.ForeignKey('TipoDeAtributo.idTipoDeAtributo'))
    )

class TipoDeItem(db.Model):
    """ Modelo de Tipo de Item """
    __tablename__ = 'TipoDeItem'
    
    idTipoDeItem = db.Column(db.Integer, primary_key=True, nullable=False)
    nombre = db.Column(db.String(45), unique=True, nullable=False)
    descripcion = db.Column(db.String(150))
    
    # one to many: Relaciona Tipo de Item x Fase
    fases = db.relationship('Fase', backref='tipoDeItem',lazy='dynamic')
    
    # one to many: Relaciona Tipo de Item x Item
    items = db.relationship('Item', backref='tipoDeItem',lazy='dynamic')

    # many to many: Relaciona Tipo de Item x Tipo de Atributo
    atributosItem = db.relationship('TipoDeAtributo', secondary = atributosItem, backref= db.backref('tipoDeItems' , lazy='dynamic'))
        
    def __init__(self, nombre=None, descripcion=None):
        """ constructor de tipo de item """
        self.nombre = nombre
        self.descripcion = descripcion

    def __repr__(self):
        return self.nombre
    
