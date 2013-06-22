import os
from datetime import datetime
from pruebita import db, app

class Item(db.Model):
    """ Modelo de Item """
    __tablename__ = 'Item'
    
    idItem = db.Column(db.Integer, primary_key=True, nullable=False)
    codigo = db.Column(db.Integer,  nullable=False )
    nombre = db.Column(db.String(45), nullable=False)
    version = db.Column(db.Integer, nullable=False)
    complejidad = db.Column(db.Integer, nullable=False)
    costo = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(20), default ='Activo', nullable=False)
    fechaDeModif = db.Column(db.DateTime, default = datetime.now(), nullable=False) 
    
    # one to many: Relaciona Fase x Item 
    faseId = db.Column(db.Integer, db.ForeignKey('Fase.idFase'))
    
    # one to many: Relaciona Tipo de Item x Item
    tipoDeItemId = db.Column(db.Integer, db.ForeignKey('TipoDeItem.idTipoDeItem'))
  
    def __init__(self, codigo=None, nombre=None, version=None, complejidad=None, costo=None, faseId = None, tipoDeItemId = None):
        """ constructor de item """
        self.codigo = codigo
        self.nombre = nombre
        self.version = version
        self.complejidad = complejidad
        self.costo = costo
        self.faseId = faseId
        self.tipoDeItemId = tipoDeItemId

    def __repr__(self):
        return self.nombre        


