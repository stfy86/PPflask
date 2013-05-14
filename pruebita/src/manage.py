from flask.ext.script import Manager
from pruebita import app, db

manager = Manager(app)

""" Administra la Base de Datos """

@manager.command
def initdb():
    """ Inicializar base de datos """
    db.create_all()


@manager.command
def createAdministrador():
    """ crea el usuario Admin """ 
    from pruebita import User
    u=User("admin","admin")
    db.session.add(u)
    db.session.commit()
   
@manager.command
def createRol():
    """ Crear Roles de Sistema Pre establecidos """
    from pruebita import Rol
    r=Rol("Administrador", "Permite el acceso al Modulo de Administracion")
    db.session.add(r)
    db.session.commit()
    r=Rol("LiderDeProyecto", "Permite el acceso al Modulo de Gestion de Cambio")
    db.session.add(r)
    db.session.commit()
    r=Rol("Desarrollador", "Permite el acceso al Modulo de Desarrollo")
    db.session.add(r)
    db.session.commit()
    
    
    
   
@manager.command
def createPermiso():
    """Crear Permisos Predefinidos """ 
    from pruebita import Permiso
    # Los permisos a Nivel de Sistema son
    p=Permiso("CrearProyecto","Permite crear un proyecto en el sistema")
    db.session.add(p)
    db.session.commit()
    p=Permiso("CrearUsuario","Permite crear un usuario dentro de un proyecto")
    db.session.add(p)
    db.session.commit()
    p=Permiso("CambiarEstadoUsuario","Permite cambiar el estado de un usuario dentro del proyecto")
    db.session.add(p)
    db.session.commit()
    p=Permiso("AdministrarTipoDeAtributo","Permite administrar un tipo de atributo")
    db.session.add(p)
    db.session.commit()
    # Los Permisos a Nivel de Proyecto son
    p=Permiso("CrearRol","Permite crear un rol en el sistema")
    db.session.add(p)
    db.session.commit()
    p=Permiso("AsignarRolAUsuario","Permite asignar Rol a Usuario")
    db.session.add(p)
    db.session.commit()
    p=Permiso("AdministrarFase","Permite administrar fase en un proyecto")
    db.session.add(p)
    db.session.commit()
    p=Permiso("ConsultaProyecto","Permite realizar consultas en un proyecto")
    db.session.add(p)
    db.session.commit()
    # Los Permisos a Nivel de Fase son
    p=Permiso("AdministrarLineaBase","Permite administrar linea base en un proyecto")
    db.session.add(p)
    db.session.commit()
    p=Permiso("AdministrarTiposDeItem","Permite administrar tipos de item en un proyecto")
    db.session.add(p)
    db.session.commit()
    # Los Permisos a Nivel de Item son
    p=Permiso("AdministrarItem","Permite administrar item en un proyecto")
    db.session.add(p)
    db.session.commit()
    p=Permiso("AdministrarCambio","Permite administrar cambio en un item de un proyecto")
    db.session.add(p)
    db.session.commit()
    p=Permiso("AprobacionItem","Permite administrar la aprobacion de item en un proyecto")
    db.session.add(p)
    db.session.commit()
    p=Permiso("DesaprobacionItem","Permite administrar la desaprobacion de item en un proyecto")
    db.session.add(p)
    db.session.commit()
    p=Permiso("ConsultaItem","Permite consulta de item en un proyecto")
    db.session.add(p)
    db.session.commit()
    
    
    
@manager.command
def dropdb():
    """Elimino la base de datos."""
    db.drop_all()


if __name__ == '__main__':
    manager.run()

