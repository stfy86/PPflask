import os
from pruebita import db, app

# usuarios de comite
miembros = db.Table('miembros', \
    db.Column('idComite', db.Integer, db.ForeignKey('Comite.idComite')),
    db.Column('idUser', db.Integer, db.ForeignKey('User.idUser'))
    )

class Comite(db.Model):
    """ Modelo de Comite"""
    __tablename__ = 'Comite'
    
    idComite = db.Column(db.Integer, primary_key=True, nullable=False)
    nombre = db.Column(db.String(45), unique=True, nullable=False)
    descripcion = db.Column(db.String(150))
    cantMiembro = db.Column(db.Integer)
    
    # many to many : Relaciona Comite x User
    miembros = db.relationship('User', secondary = miembros, backref=db.backref('comite', lazy='dynamic'))

    # one to many : Relaciona Comite x Solicitud
    listaSolicitud = db.relationship('Solicitud', backref='comite',lazy='dynamic')
    
    # one to one : Relaciona Comite x Proyecto
    proyectoId = db.Column(db.Integer, db.ForeignKey('Proyecto.idProyecto'))
    proyecto = db.relationship("Proyecto", backref=db.backref("comite", uselist=False))
    
    def __init__(self, nombre=None, descripcion=None, cantMiembro=None, proyectoId=None):
        """ constructor de comite """
        self.nombre = nombre
        self.descripcion = descripcion
        self.cantMiembro = cantMiembro
        self.proyectoId = proyectoId

    def __repr__(self):
        return self.nombre


