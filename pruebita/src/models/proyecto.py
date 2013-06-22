import os
from datetime import datetime
from pruebita import db, app

# usuarios de proyecto
users = db.Table('users', \
    db.Column('idProyecto',db.Integer, db.ForeignKey('Proyecto.idProyecto')),
    db.Column('idUser',db.Integer, db.ForeignKey('User.idUser'))
    )

class Proyecto(db.Model):
    """ Modelo de Proyecto """
    __tablename__ = 'Proyecto'
    
    idProyecto = db.Column(db.Integer, primary_key=True, nullable=False)
    nombre = db.Column(db.String(45), unique=True, nullable=False)
    descripcion = db.Column(db.String(150))
    presupuesto = db.Column(db.Integer)
    fechaDeCreacion = db.Column(db.DateTime, default = datetime.now(), nullable=False) 
    estado = db.Column(db.String(20), default ='Pendiente', nullable=False)
    
 
    # one to many: Relaciona Proyecto x Fase
    listafases = db.relationship('Fase', backref= 'Proyecto', lazy = 'dynamic')

    # many to many: Relaciona Proyecto x User
    users = db.relationship('User', secondary = users, backref = db.backref('proyectos' , lazy='dynamic'))
          
    def __init__(self, nombre=None, descripcion=None, presupuesto=None ):
        """ constructor de Proyecto """
        self.nombre = nombre
        self.descripcion = descripcion
        self.presupuesto = presupuesto
        
    def __repr__(self):
        return self.nombre
