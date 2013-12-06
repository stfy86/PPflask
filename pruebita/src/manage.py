from flask.ext.script import Manager
from modulo import *
from poblarBD import *

"""
Clase que contiene los metodos relacionados con la inicializacion de la base de datos 
"""
manager = Manager(app)

@manager.command
def initdb():
    """ Inicializar base de datos """
    db.create_all()
    print ":creo las tablas de la base de datos:"
    #poblardb()
 
@manager.command
def poblardb():
    """ Carga registros en la base de datos """
    dropdb()
    initdb()
    createUser()
    createPermiso()
    createRol()
    createProyecto()
    createAtrib()
    createTipoDeItem()
    createFase()
    asignarRol()
    
@manager.command
def poblardbPrueba():
    """ Carga registros en la base de datos de Prueba """
    dropdb()
    initdb()
    
@manager.command
def dropdb():
    """Elimino la base de datos."""
    db.drop_all()
    print ":borro la tablas de la base de datos:"


if __name__ == '__main__':
    manager.run()
