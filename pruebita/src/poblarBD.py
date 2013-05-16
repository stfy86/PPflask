""" Clase encargada de poblar la Base de Dato """

def createUser():
    """ Crea usuarios """ 
    from models import User
    from ctrl.mgrUser import MgrUser
    usuarios = [ User("admin","admin","administrador","administrador","admin@gmail.com",1234,"usuario administrador"),
                User("stfy","stfy","estefanis","zamora","stfy@gmail.com",1111,"usuario nuevo"),
                User("vavi","vavi","victor","vera","vavi@gmail.com",2222,"usuario nuevo"),
                User("lory","lory","lorelay","ortiz","lory@gmail.com",3333,"usuario nuevo"),
                User("guille","guille","guillermo","gonzalez","guille@gmail.com",4444,"usuario nuevo")]
    MgrUser().guardar(usuarios)
   
def createRol():
    """ 
    Crea Roles de Sistema Pre establecidos 
    1. Administrador: -> Permite el acceso al Modulo de Administracion
    2. Desarrollador: -> Permite el acceso al Modulo de Desarrollo
    3. Lider de Proyecto: -> Permite el acceso al Modulo de Gestion de Cambio
    """
    from models import Rol
    from ctrl.mgrRol import MgrRol
    from models import Permiso
    from ctrl.mgrPermiso import MgrPermiso
    pAdmin = [Permiso("ModuloAdministracion", "permite el acceso al modulo de administracion")]
    rAdmin = Rol("Administrador", "permite el acceso al modulo de administracion", "all project", pAdmin)
    MgrRol().guardar(rAdmin)
    pDesar = [Permiso("ModuloDesarrollo", "permite el acceso al modulo de desarrollo")]
    rDesar = Rol("Desarrollador", "permite el acceso al modulo de desarrollo", "all project", pDesar)
    MgrRol().guardar(rDesar)
    pLider = [Permiso("ModuloGestion", "permite el acceso al modulo de gestion")]
    rLider=Rol("LiderDeProyecto","permite el acceso al modulo de gestion","all project", pLider)
    MgrRol().guardar(rLider)
    
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
    permisos = [ # Los permisos a Nivel de Sistema son
                Permiso("CrearProyecto","Permite crear un proyecto en el sistema"),
                Permiso("CrearUsuario","Permite crear un usuario dentro de un proyecto"),
                Permiso("CambiarEstadoUsuario","Permite cambiar el estado de un usuario dentro del proyecto"),
                Permiso("AdministrarTipoDeAtributo","Permite administrar un tipo de atributo"),
                # Los Permisos a Nivel de Proyecto son
                Permiso("CrearRol","Permite crear un rol en el sistema"),
                Permiso("AsignarRolAUsuario","Permite asignar Rol a Usuario"),
                Permiso("AdministrarFase","Permite administrar fase en un proyecto"),
                Permiso("ConsultaProyecto","Permite realizar consultas en un proyecto"),
                # Los Permisos a Nivel de Fase son
                Permiso("AdministrarLineaBase","Permite administrar linea base en un proyecto"),
                Permiso("AdministrarTiposDeItem","Permite administrar tipos de item en un proyecto"),
                # Los Permisos a Nivel de Item son
                Permiso("AdministrarItem","Permite administrar item en un proyecto"),
                Permiso("AdministrarCambio","Permite administrar cambio en un item de un proyecto"),
                Permiso("AprobacionItem","Permite administrar la aprobacion de item en un proyecto"),
                Permiso("DesaprobacionItem","Permite administrar la desaprobacion de item en un proyecto"),
                Permiso("ConsultaItem","Permite consulta de item en un proyecto")]
    MgrPermiso().guardar(permisos)

def createProject():
    """ Crea proyectos por default """
    from models import Proyecto
    from ctrl.mgrProject import MgrProject
    p=Proyecto("proyecto1","sistema para una veterinaria",1000)
    MgrProject().guardar(p)
    p=Proyecto("proyecto2","sistema para una guarderia",2000)
    MgrProject().guardar(p)
    p=Proyecto("proyecto3","sistema para un consultorio",3000)
    MgrProject().guardar(p)
    p=Proyecto("proyecto4","sistema para un supermercado",4000)
    MgrProject().guardar(p)
    p=Proyecto("proyecto5","sistema para un banco",5000)
    MgrProject().guardar(p)
    #MgrProject().borrar("proyecto5")
    #MgrProject().modificar("proyecto5","proyecto5","sistema para un banco2","Pendiente")

