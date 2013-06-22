import os
from datetime import datetime
from pruebita import db, app

class TipoDeAtributo(db.Model):
    """ Modelo de Tipo de Atributo """
    __tablename__ = 'TipoDeAtributo'
    
    idTipoDeAtributo = db.Column(db.Integer, primary_key=True, nullable=False)
    nombre = db.Column(db.String(45), unique=True, nullable=False)
    tipoDeDato = db.Column(db.String(20), nullable=False) # numerico, texto, fecha, boolean, archivo
    detalle = db.Column(db.Integer) # si tipoDeDato es numerico, corresponde a la presicion, si tipoDeDato es texto, corresponde a la cantidad de caracteres
    filename = db.Column(db.String(30)) # el nombre del archivo
    archivo = db.Column(db.LargeBinary) # si tipoDeDato es file, corresponde al archivo
    descripcion = db.Column(db.String(150))
       
    def __init__(self, nombre=None, tipoDeDato=None, detalle=None, descripcion=None,filename = None, archivo=None):
        """ constructor de Tipo de Atributo"""
        self.nombre = nombre
        self.tipoDeDato = tipoDeDato
        self.detalle = detalle
        self.descripcion = descripcion
        self.filename = filename
        self.archivo = archivo
    
    def __repr__(self):
        return self.nombre
