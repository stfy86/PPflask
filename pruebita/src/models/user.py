import os
from datetime import datetime
from pruebita import db, app

# roles de usuarios
roles = db.Table('roles', \
    db.Column('idUser',db.Integer, db.ForeignKey('User.idUser')),
    db.Column('idRol',db.Integer, db.ForeignKey('Rol.idRol'))
)

class User(db.Model):
    """ Modelo de Usuario """
    __tablename__ = 'User'

    idUser = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(15), unique=True, nullable=False)
    passwd = db.Column(db.String(15), nullable=False)
    nombre = db.Column(db.String(45), nullable=False)
    apellido = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45))
    telefono = db.Column(db.Integer)
    obs = db.Column(db.String(150))
    estado = db.Column(db.String(20), default ='Inactivo', nullable=False)
            
    # many to many: Relaciona User x Rol
    roles = db.relationship('Rol', secondary = roles, backref = db.backref('users' , lazy='dynamic'))
  
    # one to many : Relaciona Solicitud x User
    solicitudes = db.relationship('Solicitud', backref='user',lazy='dynamic')
    
    def __init__(self,name=None, passwd=None, nombre=None, apellido=None, email=None, telefono=None, obs=None):
        """ constructor de user """
        self.name = name
        self.passwd = passwd
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.obs = obs
        
    def __repr__(self):
        return self.name
