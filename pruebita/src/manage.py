from flask.ext.script import Manager
from pruebita import app, db


import models

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
    createTipoDeAtrib()
    createFase()

 
@manager.command
def createUser():
    """ Crea usuarios """ 
    from models import User
    from ctrl.mgrUser import MgrUser
    u = User("admin","admin","administrador","administrador","admin@gmail.com",1234,"usuario administrador")
    MgrUser().guardar(u)
    u=User("stfy","stfy","estefanis","zamora","stfy@gmail.com",1111,"usuario nuevo")
    MgrUser().guardar(u)
    u=User("vavi","vavi","victor","vera","vavi@gmail.com",2222,"usuario nuevo")
    MgrUser().guardar(u)
    u=User("lory","lory","lorelay","ortiz","lory@gmail.com",3333,"usuario nuevo")
    MgrUser().guardar(u)
    u=User("guille","guille","guillermo","gonzalez","guille@gmail.com",4444,"usuario nuevo")
    MgrUser().guardar(u)
    #MgrUser().borrar("guille")
       
@manager.command
def createRol():
    """ 
    Crea Roles de Sistema Pre establecidos 
    1. Administrador: -> Permite el acceso al Modulo de Administracion
        - administra usuarios
        - crea proyecto
        - elimina proyecto
        - asigna lider a proyecto
        - administra tipo de atributo
    2. Desarrollador: -> Permite el acceso al Modulo de Desarrollo
        - administra item
        - administra reportes
    3. Lider de Proyecto: -> Permite el acceso al Modulo de Gestion de Cambio
        - administra proyecto
        - administra fase
        - administra tipo de item
        - administra roles 
        - administra LB
        - calculo de costo
        - calculo de impacto
    """
    from models import Rol
    from ctrl.mgrRol import MgrRol
    r=Rol("Administrador","permite el acceso al modulo de administracion","all project")
    MgrRol().guardar(r)
    r=Rol("Desarrollador","permite el acceso al modulo de desarrollo","all project")
    MgrRol().guardar(r)
    r=Rol("LiderDeProyecto","permite el acceso al modulo de gestion","all project")
    MgrRol().guardar(r)
    #MgrRol().borrar("LiderDeProyecto")

@manager.command
def createPermiso():
    """
    Crea Permisos Predefinidos a nivel de:
    - sistema
    - proyecto
    - fase
    - item
    """
    from models import Permiso
    from ctrl.mgrPermiso import MgrPermiso
    # Los permisos a Nivel de Sistema son
    p=Permiso("CrearProyecto","Permite crear un proyecto en el sistema")
    MgrPermiso().guardar(p)
    p=Permiso("CrearUsuario","Permite crear un usuario dentro de un proyecto")
    MgrPermiso().guardar(p)
    p=Permiso("CambiarEstadoUsuario","Permite cambiar el estado de un usuario dentro del proyecto")
    MgrPermiso().guardar(p)
    p=Permiso("AdministrarTipoDeAtributo","Permite administrar un tipo de atributo")
    MgrPermiso().guardar(p)
    # Los Permisos a Nivel de Proyecto son
    p=Permiso("CrearRol","Permite crear un rol en el sistema")
    MgrPermiso().guardar(p)
    p=Permiso("AsignarRolAUsuario","Permite asignar Rol a Usuario")
    MgrPermiso().guardar(p)
    p=Permiso("AdministrarFase","Permite administrar fase en un proyecto")
    MgrPermiso().guardar(p)
    p=Permiso("ConsultaProyecto","Permite realizar consultas en un proyecto")
    MgrPermiso().guardar(p)
    # Los Permisos a Nivel de Fase son
    p=Permiso("AdministrarLineaBase","Permite administrar linea base en un proyecto")
    MgrPermiso().guardar(p)
    p=Permiso("AdministrarTiposDeItem","Permite administrar tipos de item en un proyecto")
    MgrPermiso().guardar(p)
    # Los Permisos a Nivel de Item son
    p=Permiso("AdministrarItem","Permite administrar item en un proyecto")
    MgrPermiso().guardar(p)
    p=Permiso("AdministrarCambio","Permite administrar cambio en un item de un proyecto")
    MgrPermiso().guardar(p)
    p=Permiso("AprobacionItem","Permite administrar la aprobacion de item en un proyecto")
    MgrPermiso().guardar(p)
    p=Permiso("DesaprobacionItem","Permite administrar la desaprobacion de item en un proyecto")
    MgrPermiso().guardar(p)
    p=Permiso("ConsultaItem","Permite consulta de item en un proyecto")
    MgrPermiso().guardar(p)
    #MgrPermiso().borrar("ConsultaItem")
 
@manager.command
def createProject():
    """ Crea proyectos por default """
    from models import Proyecto
    from ctrl.mgrProject import MgrProject
    p=Proyecto("proyecto1","sistema para una veterinaria")
    MgrProject().guardar(p)
    p=Proyecto("proyecto2","sistema para una guarderia")
    MgrProject().guardar(p)
    p=Proyecto("proyecto3","sistema para un consultorio")
    MgrProject().guardar(p)
    p=Proyecto("proyecto4","sistema para un supermercado")
    MgrProject().guardar(p)
    p=Proyecto("proyecto5","sistema para un banco")
    MgrProject().guardar(p)
    #MgrProject().borrar("proyecto5")
    #MgrProject().modificar("proyecto5","proyecto5","sistema para un banco2","Pendiente")

@manager.command
def createFase():
    """ crea proyectos por default """
    from models import Fase
    from ctrl.mgrFase import MgrFase
    f=Fase("fase1-proyecto1","fase inicial",1)
    MgrFase().guardar(f)
    f=Fase("fase2-proyecto1","fase",2)
    MgrFase().guardar(f)
    f=Fase("fase1-proyecto2","fase inicial",1)
    MgrFase().guardar(f)
    f=Fase("fase2-proyecto2","fase",2)
    MgrFase().guardar(f)
    f=Fase("fase1-proyecto3","fase inicial",1)
    MgrFase().guardar(f)
    f=Fase("fase2-proyecto3","fase",2)
    MgrFase().guardar(f)
    #MgrFase().borrar("fase2-proyecto3")
    #MgrFase().modificar("fase1-proyecto3", "fase1-proyecto3","inicio",1)

@manager.command
def createTipoDeAtrib():
    """ Crea tipo de Atibutos por default """
    from models import TipoDeAtributo
    from ctrl.mgrTipoDeAtrib import MgrTipoDeAtrib
    t=TipoDeAtributo("numerico20", "numerico", 20,"atributo numerico con presicion 20")
    MgrTipoDeAtrib().guardar(t)
    t=TipoDeAtributo("texto45", "texto", 45,"atributo texto con 45 caracteres")
    MgrTipoDeAtrib().guardar(t)
    t=TipoDeAtributo("date", "fecha", 0,"atributo fecha")
    MgrTipoDeAtrib().guardar(t)
    t=TipoDeAtributo("booleano", "boolean", 0,"atributo boleano")
    MgrTipoDeAtrib().guardar(t)
    t=TipoDeAtributo("numerico45", "numerico", 45,"atributo numerico con presicion 45")
    MgrTipoDeAtrib().guardar(t)
    #MgrTipoDeAtrib().borrar("date")
    
@manager.command
def dropdb():
    """Elimino la base de datos."""
    db.drop_all()


if __name__ == '__main__':
    manager.run()

