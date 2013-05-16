from flask.ext.script import Manager
from pruebita import app, db
from poblarBD import createUser, createPermiso, createRol, createProject
from models import *

manager = Manager(app)
"""
Clase que contiene los metodos relacionados con la inicializacion de la base de datos 
@param manager Inicializa el modulo 
"""

@manager.command
def initdb():
    """ Inicializar base de datos """
    db.create_all()
    createUser()
    createPermiso()
    createRol()
    createProject()
   
    
@manager.command
def dropdb():
    """Elimino la base de datos."""
    db.drop_all()


if __name__ == '__main__':
    manager.run()

