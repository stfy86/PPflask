import os
from datetime import datetime
from pruebita import db, app


#------------------------------------------------------------------------------#
# MODELS
#------------------------------------------------------------------------------#

# UserXRol
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
    roles = db.relationship('Rol', secondary = roles, 
        backref = db.backref('users' , lazy='dynamic'))
        
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

# RolXPermiso
permisos = db.Table('permisos', \
    db.Column('idRol',db.Integer, db.ForeignKey('Rol.idRol')),
    db.Column('idPermiso',db.Integer, db.ForeignKey('Permiso.idPermiso'))
    )
    
class Rol(db.Model):
    """ Modelo de Rol """
    __tablename__ = 'Rol'
    
    idRol = db.Column(db.Integer, primary_key=True, nullable=False)
    nombre = db.Column(db.String(45), unique=True, nullable=False)
    ambito = db.Column(db.String(45)) # corresponde al proyecto en el cual se creo
    descripcion = db.Column(db.String(150))
    
    # many to many: Relaciona Rol x Permiso
    permisos = db.relationship('Permiso', secondary = permisos,
        backref= db.backref('roles' , lazy='dynamic'))
        
    def __init__(self, nombre=None, descripcion=None):
        """ constructor de Rol """
        self.nombre = nombre
        self.descripcion = descripcion
    
    
    def __init__(self, nombre=None, descripcion=None, ambito=None):
        """ constructor de Rol """
        self.nombre = nombre
        self.ambito = ambito
        self.descripcion = descripcion
     
    def __repr__(self):
        return self.nombre

class Permiso(db.Model):
    """ Modelo de Permiso """
    __tablename__ = 'Permiso'
    
    idPermiso = db.Column(db.Integer, primary_key=True,nullable=False)
    nombre = db.Column(db.String(45), unique=True,nullable=False)
    descripcion = db.Column(db.String(150))
    
    def __init__(self, nombre=None, descripcion=None):
        """ constructor de Permiso """
        self.nombre = nombre
        self.descripcion = descripcion

    
#ProyectoXUser
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
    fechaDeCreacion = db.Column(db.DateTime, default = datetime.now(), nullable=False) 
    estado = db.Column(db.String(20), default ='Pendiente', nullable=False)
    
    # one to many: Relaciona Proyecto x Fase
    listafases = db.relationship('Fase', backref= 'proyecto', lazy = 'dynamic')
    
    # many to many: Relaciona Proyecto x User
    users = db.relationship('User', secondary = users,
        backref = db.backref('proyectos' , lazy='dynamic'))
    
    def __init__(self, nombre=None, descripcion=None):
        """ constructor de Proyecto """
        self.nombre = nombre
        self.descripcion = descripcion
        

class TipoDeAtributo(db.Model):
    """ Modelo de Tipo de Atributo """
    __tablename__ = 'TipoDeAtributo'
    
    idTipoDeAtributo = db.Column(db.Integer, primary_key=True, nullable=False)
    nombre = db.Column(db.String(45), unique=True, nullable=False)
    tipoDeDato = db.Column(db.String(20), nullable=False) # numerico, texto, fecha, boolean
    detalle = db.Column(db.Integer) # si tipoDeDato es numerico, corresponde a la presicion, si tipoDeDato es texto, corresponde a la cantidad de caracteres  
    descripcion = db.Column(db.String(150))
    
    # one to one: Relaciona Fase con Tipo de Atributo
    faseId = db.Column(db.Integer, db.ForeignKey('Fase.idFase'))
    
    
    def __init__(self, nombre=None, tipoDeDato=None, detalle=None, descripcion=None):
        """ constructor de Tipo de Atributo"""
        self.nombre = nombre
        self.tipoDeDato = tipoDeDato
        self.detalle = detalle
        self.descripcion = descripcion


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
    
    # one to many: Relaciona Fase x Tipo de Item
    listaTipoDeItem = db.relationship('TipoDeItem', backref='Fase', lazy = 'dynamic')
    
    # one to many: Relaciona Fase x Item
    listaItem = db.relationship('Item', backref='Fase', lazy = 'dynamic')
    
    # one to one: Relaciona Fase con Tipo de Atributo
    tipoDeAtributos = db.relationship('TipoDeAtributo', uselist=False, backref= 'Fase')
      
    
    def __init__(self, nombre=None, descripcion=None, orden=None):
        """ constructor de fase """
        self.nombre = nombre
        self.descripcion = descripcion
        self.orden = orden

class Item(db.Model):
    """ Modelo de Item """
    __tablename__ = 'Item'
    
    idItem = db.Column(db.Integer, primary_key=True, nullable=False)
    nombre = db.Column(db.String(45), unique=True, nullable=False)
    version = db.Column(db.Integer, nullable=False)
    complejidad = db.Column(db.Integer, nullable=False)
    costo = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(20), default ='Activo', nullable=False)
    fechaDeModif = db.Column(db.DateTime, default = datetime.now(), nullable=False) 
    
    # one to many: Relaciona Fase x Item 
    faseId = db.Column(db.Integer, db.ForeignKey('Fase.idFase'))
    
    # one to one: Relaciona Item x Tipo de Item
    tipoDeItem = db.relationship('TipoDeItem', uselist=False, backref='Item')
    
    
    def __init__(self, nombre=None, version=None, complejidad=None, costo=None):
        """ constructor de item """
        self.nombre = nombre
        self.version = version
        self.complejidad = complejidad
        self.costo = costo
        

class TipoDeItem(db.Model):
    """ Modelo de Tipo de Item """
    __tablename__ = 'TipoDeItem'
    
    idTipoDeItem = db.Column(db.Integer, primary_key=True, nullable=False)
    nombre = db.Column(db.String(45), unique=True, nullable=False)
    descripcion = db.Column(db.String(150))
    
    # one to many: Relaciona Fase x Tipo de Item
    faseId = db.Column(db.Integer, db.ForeignKey('Fase.idFase'))

    # one to one: Relaciona Item x Tipo de Item
    itemId = db.Column(db.Integer, db.ForeignKey('Item.idItem'))
    
    def __init__(self, nombre=None, descripcion=None):
        """ constructor de tipo de item """
        self.nombre = nombre
        self.descripcion = descripcion

