from flask.ext.script import Manager
from pruebita import app, db
from poblarBD import createUser, createPermiso, createRol, createProject, createTipoDeAtrib, createAdmin, createLider, configurarPermiso, usuariosAProyecto
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
    print ":creo las tablas de la base de datos:"
    poblardb()


@manager.command
def poblardb():
    """ Carga registros en la base de datos """
    createUser()
    print ":cargo usuarios:"
    createPermiso()
    print ":cargo permisos predefinidos:"
    createRol()
    print ":cargo roles del sistema:"
    createProject()
    print ":cargo proyectos:"
    createTipoDeAtrib()
    print ":cargo tipo de atributos:"
    createAdmin()
    print":cargo un usuario admin con los roles de administrador, lider de proyecto y desarrollador:"
    createLider()
    print ":asigno lider a proyecto:"
    configurarPermiso()
    print ":asigna/desasigna permiso al rol:"
    usuariosAProyecto()
    print ":asigna/desasigna usuario al proyecto:"
    
@manager.command
def dropdb():
    """Elimino la base de datos."""
    db.drop_all()
    print ":borro la tablas de la base de datos:"


if __name__ == '__main__':
    manager.run()

