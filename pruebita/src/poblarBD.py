""" Clase encargada de poblar la Base de Dato """

def createUser():
    """ Crea usuarios """ 
    from models import User
    from ctrl.mgrUser import MgrUser
    usuarios = [User("stfy","stfy","estefanis","zamora","stfy@gmail.com",1111,"usuario nuevo"),
                User("vavi","vavi","victor","vera","vavi@gmail.com",2222,"usuario nuevo"),
                User("lory","lory","lorelay","ortiz","lory@gmail.com",3333,"usuario nuevo"),
                User("guille","guille","guillermo","gonzalez","guille@gmail.com",4444,"usuario nuevo")]
    MgrUser().guardar(usuarios)
   
def createRol():
    """ 
    Crea Roles de Sistema Pre establecidos 
    1. Administrador:  Permite el acceso al Modulo de Administracion
    2. Desarrollador:  Permite el acceso al Modulo de Desarrollo
    3. Lider de Proyecto: Permite el acceso al Modulo de Gestion de Cambio
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
    from models import Fase
    from ctrl.mgrFase import MgrFase
    f = [Fase("proyecto1-fase1","fase inicial",1)]
    p = Proyecto("proyecto1","sistema para una veterinaria",1000,f)
    MgrProject().guardar(p)
    f = [Fase("proyecto2-fase1","fase inicial",1),
         Fase("proyecto2-fase2","nueva fase",2)]
    p = Proyecto("proyecto2","sistema para una guarderia",2000,f)
    MgrProject().guardar(p)
    f = [Fase("proyecto3-fase1","fase inicial",1),
         Fase("proyecto3-fase2","nueva fase",2),
         Fase("proyecto3-fase3","nueva fase",3),
         ]
    p = Proyecto("proyecto3","sistema para un consultorio",3000,f)
    MgrProject().guardar(p)
    f = [Fase("proyecto4-fase1","fase inicial",1),
         Fase("proyecto4-fase2","nueva fase",2),
         Fase("proyecto4-fase3","nueva fase",3),
         Fase("proyecto4-fase4","nueva fase",4)]
    p = Proyecto("proyecto4","sistema para un supermercado",4000,f)
    MgrProject().guardar(p)
    f = [Fase("proyecto5-fase1","fase inicial",1)]
    p = Proyecto("proyecto5","sistema para un banco",5000,f)
    MgrProject().guardar(p)
    #MgrProject().borrar("proyecto5")
    #MgrProject().modificar("proyecto5","proyecto5","sistema para un banco2","Pendiente")


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
    

def createAdmin():
    """ 
    Crea el usuario admin con los roles de:
        1. administrador
        2. desarrollador
        3. lider de proyecto
    Dicho usario, tiene acceso a todos los modulos del sistema (administracion, desarrollo y gestion)
    """
    from models import User, Rol
    from ctrl.mgrRol import MgrRol
    from ctrl.mgrUser import MgrUser
    rol1 = MgrRol().filtrar("Administrador")
    rol2 = MgrRol().filtrar("Desarrollador")
    rol3 = MgrRol().filtrar("LiderDeProyecto")
    roles = [rol1, rol2, rol3]
    usr1 = User("admin","admin","administrador","administrador","admin@gmail.com",1234,"usuario administrador", roles),
    MgrUser().guardar(usr1)

def createLider():
    """ asigna lider a un proyecto """
    from ctrl.mgrProject import MgrProject
    MgrProject().asignarLider("proyecto5","stfy")
    MgrProject().asignarLider("proyecto4","lory")
    MgrProject().asignarLider("proyecto2","vavi")
    
def configurarPermiso():
    """ asigna/desasigna permisos a un rol """
    from ctrl.mgrRol import MgrRol
    MgrRol().asignarPermiso("liderDeProyecto-proyecto5", "CrearRol")
    MgrRol().asignarPermiso("liderDeProyecto-proyecto5", "AsignarRolAUsuario")
    MgrRol().desasignarPermiso("liderDeProyecto-proyecto5", "AsignarRolAUsuario")
    

def usuariosAProyecto():
    """ asigna/desasigna usuarios a proyecto """
    from ctrl.mgrProject import MgrProject
    nombreRol = "desarrollador-proyecto4-vavi"
    descripcionRol = "nuevo rol asignado a un usuario del proyecto"
    MgrProject().asignarUsuario("proyecto4", "vavi", nombreRol, descripcionRol)
    nombreRol = "desarrollador-proyecto4-stfy"
    descripcionRol = "nuevo rol asignado a un usuario del proyecto"
    MgrProject().asignarUsuario("proyecto4", "stfy", nombreRol, descripcionRol)
    MgrProject().desasignarUsuario("proyecto4", "stfy", nombreRol)
    
def createItem():
    from ctrl.mgrItem import MgrItem
    from models import Item
    from ctrl.mgrFase import MgrFase
    from models import Fase
    
    faseref = MgrFase().filtrar('proyecto1-fase1')
    item = Item(nombre='proyecto1-fase1-item1', version=1, complejidad=3, costo=4, estado='Activo', fase=faseref)
    MgrItem().guardar(item)
    item = Item(nombre='proyecto1-fase1-item2', version=1, complejidad=3, costo=4, estado='Aprobado', fase=faseref)
    MgrItem().guardar(item)
    item = Item(nombre='proyecto1-fase1-item3', version=1, complejidad=3, costo=4, estado='Activo', fase=faseref)
    MgrItem().guardar(item)
    item = Item(nombre='proyecto1-fase1-item4', version=1, complejidad=3, costo=4, estado='Aprobado', fase=faseref)
    MgrItem().guardar(item)
    item = Item(nombre='proyecto1-fase1-item5', version=1, complejidad=3, costo=4, estado='Activo', fase=faseref)
    MgrItem().guardar(item)
    item = Item(nombre='proyecto1-fase1-item6', version=1, complejidad=3, costo=4, estado='Aprobado', fase=faseref)
    MgrItem().guardar(item)
    item = Item(nombre='proyecto1-fase1-item7', version=1, complejidad=3, costo=4, estado='Activo', fase=faseref)
    MgrItem().guardar(item)
    item = Item(nombre='proyecto1-fase1-item8', version=1, complejidad=3, costo=4, estado='Aprobado', fase=faseref)
    MgrItem().guardar(item)
    item = Item(nombre='proyecto1-fase1-item9', version=1, complejidad=3, costo=4, estado='Activo', fase=faseref)
    MgrItem().guardar(item)
    item = Item(nombre='proyecto1-fase1-item10', version=1, complejidad=3, costo=4, estado='Aprobado', fase=faseref)
    MgrItem().guardar(item)
    
    faseref = MgrFase().filtrar('proyecto2-fase1')
    item = Item(nombre='proyecto2-fase1-item1', version=1, complejidad=3, costo=4, estado='Activo', fase=faseref)
    MgrItem().guardar(item)
    item = Item(nombre='proyecto2-fase1-item2', version=1, complejidad=3, costo=4, estado='Aprobado', fase=faseref)
    MgrItem().guardar(item)
    item = Item(nombre='proyecto2-fase1-item3', version=1, complejidad=3, costo=4, estado='Activo', fase=faseref)
    MgrItem().guardar(item)
    item = Item(nombre='proyecto2-fase1-item4', version=1, complejidad=3, costo=4, estado='Aprobado', fase=faseref)
    MgrItem().guardar(item)
    item = Item(nombre='proyecto2-fase1-item5', version=1, complejidad=3, costo=4, estado='Activo', fase=faseref)
    MgrItem().guardar(item)
    item = Item(nombre='proyecto2-fase1-item6', version=1, complejidad=3, costo=4, estado='Aprobado', fase=faseref)
    MgrItem().guardar(item)
    item = Item(nombre='proyecto2-fase1-item7', version=1, complejidad=3, costo=4, estado='Activo', fase=faseref)
    MgrItem().guardar(item)
    item = Item(nombre='proyecto2-fase1-item8', version=1, complejidad=3, costo=4, estado='Aprobado', fase=faseref)
    MgrItem().guardar(item)
    item = Item(nombre='proyecto2-fase1-item9', version=1, complejidad=3, costo=4, estado='Activo', fase=faseref)
    MgrItem().guardar(item)
    item = Item(nombre='proyecto2-fase1-item10', version=1, complejidad=3, costo=4, estado='Aprobado', fase=faseref)
    MgrItem().guardar(item)
    
    faseref = MgrFase().filtrar('proyecto2-fase2')    
    item = Item(nombre='proyecto2-fase2-item1', version=1, complejidad=3, costo=4, estado='Activo', fase=faseref)
    MgrItem().guardar(item)
    item = Item(nombre='proyecto2-fase2-item2', version=1, complejidad=3, costo=4, estado='Aprobado', fase=faseref)
    MgrItem().guardar(item)
    item = Item(nombre='proyecto2-fase2-item3', version=1, complejidad=3, costo=4, estado='Activo', fase=faseref)
    MgrItem().guardar(item)
    item = Item(nombre='proyecto2-fase2-item4', version=1, complejidad=3, costo=4, estado='Aprobado', fase=faseref)
    MgrItem().guardar(item)
    item = Item(nombre='proyecto2-fase2-item5', version=1, complejidad=3, costo=4, estado='Activo', fase=faseref)
    MgrItem().guardar(item)
    item = Item(nombre='proyecto2-fase2-item6', version=1, complejidad=3, costo=4, estado='Aprobado', fase=faseref)
    MgrItem().guardar(item)
    item = Item(nombre='proyecto2-fase2-item7', version=1, complejidad=3, costo=4, estado='Activo', fase=faseref)
    MgrItem().guardar(item)
    item = Item(nombre='proyecto2-fase2-item8', version=1, complejidad=3, costo=4, estado='Aprobado', fase=faseref)
    MgrItem().guardar(item)
    item = Item(nombre='proyecto2-fase2-item9', version=1, complejidad=3, costo=4, estado='Activo', fase=faseref)
    MgrItem().guardar(item)
    item = Item(nombre='proyecto2-fase2-item10', version=1, complejidad=3, costo=4, estado='Aprobado', fase=faseref)
    MgrItem().guardar(item)
    
def createLineaBase():
    from models import LineaBase
    from ctrl.mgrLineaBase import MgrLineaBase
    from models import Item
    from ctrl.mgrItem import MgrItem
    from models import Fase
    from ctrl.mgrFase import MgrFase
    
    items = []
    item = MgrItem().filtrar('proyecto1-fase1-item2')
    items.append(item.nombre)
    item = MgrItem().filtrar('proyecto1-fase1-item4')
    items.append(item.nombre)
    
    faseref = MgrFase().filtrar('proyecto1-fase1')
    lineaBase = LineaBase(nombre = 'proyecto1-fase1-LB1', descripcion = 'LB1', fase = faseref)
    MgrLineaBase().guardar(lineaBase)
    MgrLineaBase().asignarItems(lineaBase.nombre, items)
    
    
    
    items = []
    item = MgrItem().filtrar('proyecto2-fase1-item2')
    items.append(item.nombre)
    item = MgrItem().filtrar('proyecto2-fase1-item4')
    items.append(item.nombre)
    
    faseref = MgrFase().filtrar('proyecto2-fase1')
    lineaBase = LineaBase(nombre= 'proyecto2-fase1-LB1', descripcion = 'LB1', fase = faseref)
    MgrLineaBase().guardar(lineaBase)
    MgrLineaBase().asignarItems(lineaBase.nombre, items)
    
    
    
    items = []
    item = MgrItem().filtrar('proyecto2-fase2-item2')
    items.append(item.nombre)
    item = MgrItem().filtrar('proyecto2-fase2-item4')
    items.append(item.nombre)
    
    faseref = MgrFase().filtrar('proyecto2-fase2')
    lineaBase = LineaBase(nombre= 'proyecto2-fase2-LB1', descripcion = 'LB1', fase = faseref)
    MgrLineaBase().guardar(lineaBase)
    MgrLineaBase().asignarItems(lineaBase.nombre, items)
    
    
    
    items = []
    item = MgrItem().filtrar('proyecto2-fase2-item4')
    items.append(item.nombre)
    item = MgrItem().filtrar('proyecto2-fase2-item6')
    items.append(item.nombre)
    
    faseref = MgrFase().filtrar('proyecto2-fase2')
    lineaBase = LineaBase(nombre= 'proyecto2-fase2-LB2', descripcion = 'LB1', fase = faseref)
    MgrLineaBase().guardar(lineaBase)
    MgrLineaBase().asignarItems(lineaBase.nombre, items)
