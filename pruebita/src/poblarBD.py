#------------------------------------------------------------------------------#
# poblarBD
#------------------------------------------------------------------------------#
from modulo import *

""" Clase encargada para poblar la base de datos """

def createUser():
    """ Carga usuarios """ 
    u = User(name="stfy", passwd="stfy", nombre="estefanis", apellido="zamora", email="stfy@gmail.com", telefono=1111, obs="usuario nuevo")
    MgrUser().guardar(u)
    u = User(name="vavi", passwd="vavi", nombre="victor", apellido="vera", email="vavi@gmail.com", telefono=2222, obs="usuario nuevo")
    MgrUser().guardar(u)
    u = User(name="lory", passwd="lory", nombre="lorelay", apellido="ortiz", email="lory@gmail.com", telefono=3333, obs="usuario nuevo")
    MgrUser().guardar(u)
    u = User(name="guille", passwd="guille", nombre="guillermo", apellido="gonzalez", email="guille@gmail.com", telefono=4444, obs="usuario nuevo")
    MgrUser().guardar(u)
    u = User(name="admin", passwd="admin", nombre="administrador", apellido="administrador", email="admin@gmail.com", telefono=1234, obs="administrador del sistema")
    MgrUser().guardar(u)
    print ":cargo usuarios:"
 
def createProyecto():
    """ Carga proyectos """
    # crea un proyecto
    p = Proyecto(nombre="proyecto1", descripcion="sistema 1", presupuesto=10000)
    MgrProyecto().guardar(p)
    r = Rol(nombre="LiderDeProyecto", descripcion="rol de lider", ambito= p.nombre)
    MgrRol().guardar(r)
    MgrProyecto().asignarLider(proyecto = p , rol = r, nameLider = "lory")
    p = MgrProyecto().filtrar("proyecto1")
    c = Comite(nombre="comite-proyecto1", descripcion="comite de cambio", cantMiembro=3, proyectoId=p.idProyecto)
    MgrComite().guardar(c)
    MgrComite().asignarUsuario(nombreProyecto = "proyecto1",  nameUser= "lory")

    p = Proyecto(nombre="proyecto2", descripcion="sistema 2", presupuesto=20000)
    MgrProyecto().guardar(p)
    r = Rol(nombre="LiderDeProyecto", descripcion="rol de lider", ambito= p.nombre)
    MgrRol().guardar(r)
    MgrProyecto().asignarLider(proyecto = p , rol = r, nameLider = "vavi")
    p = MgrProyecto().filtrar("proyecto2")
    c = Comite(nombre="comite-proyecto2", descripcion="comite de cambio", cantMiembro=4, proyectoId=p.idProyecto)
    MgrComite().guardar(c)
    MgrComite().asignarUsuario(nombreProyecto = "proyecto2",  nameUser= "vavi")
    
    p = Proyecto(nombre="proyecto3", descripcion="sistema 3", presupuesto=30000)
    MgrProyecto().guardar(p)
    r = Rol(nombre="LiderDeProyecto", descripcion="rol de lider", ambito= p.nombre)
    MgrRol().guardar(r)
    MgrProyecto().asignarLider(proyecto = p , rol = r, nameLider = "guille")
    p = MgrProyecto().filtrar("proyecto3")
    c = Comite(nombre="comite-proyecto3", descripcion="comite de cambio", cantMiembro=5, proyectoId=p.idProyecto)
    MgrComite().guardar(c)
    MgrComite().asignarUsuario(nombreProyecto = "proyecto3",  nameUser= "guille")    
    
    p = Proyecto(nombre="proyecto4", descripcion="sistema 4", presupuesto=40000)
    MgrProyecto().guardar(p)
    r = Rol(nombre="LiderDeProyecto", descripcion="rol de lider", ambito= p.nombre)
    MgrRol().guardar(r)
    MgrProyecto().asignarLider(proyecto = p , rol = r, nameLider = "stfy")
    p = MgrProyecto().filtrar("proyecto4")
    c = Comite(nombre="comite-proyecto4", descripcion="comite de cambio", cantMiembro=6, proyectoId=p.idProyecto)
    MgrComite().guardar(c)
    MgrComite().asignarUsuario(nombreProyecto = "proyecto4",  nameUser= "stfy")
    
    
    p = Proyecto(nombre="proyecto5", descripcion="sistema 5", presupuesto=50000)
    MgrProyecto().guardar(p)
    r = Rol(nombre="LiderDeProyecto", descripcion="rol de lider", ambito= p.nombre)
    MgrRol().guardar(r)
    MgrProyecto().asignarLider(proyecto = p , rol = r, nameLider = "lory")
    p = MgrProyecto().filtrar("proyecto5")
    c = Comite(nombre="comite-proyecto5", descripcion="comite de cambio", cantMiembro=3, proyectoId=p.idProyecto)
    MgrComite().guardar(c)
    MgrComite().asignarUsuario(nombreProyecto = "proyecto5",  nameUser= "lory")
    
    p = Proyecto(nombre="proyecto6", descripcion="sistema 6", presupuesto=60000)
    MgrProyecto().guardar(p)
    r = Rol(nombre="LiderDeProyecto", descripcion="rol de lider", ambito= p.nombre)
    MgrRol().guardar(r)
    MgrProyecto().asignarLider(proyecto = p , rol = r, nameLider = "vavi")
    p = MgrProyecto().filtrar("proyecto6")
    c = Comite(nombre="comite-proyecto6", descripcion="comite de cambio", cantMiembro=3, proyectoId=p.idProyecto)
    MgrComite().guardar(c)
    MgrComite().asignarUsuario(nombreProyecto = "proyecto6",  nameUser= "vavi")
    
    
    p = Proyecto(nombre="proyecto7", descripcion="sistema 7", presupuesto=70000)
    MgrProyecto().guardar(p)
    r = Rol(nombre="LiderDeProyecto", descripcion="rol de lider", ambito= p.nombre)
    MgrRol().guardar(r)
    MgrProyecto().asignarLider(proyecto = p , rol = r, nameLider = "stfy")
    p = MgrProyecto().filtrar("proyecto7")
    c = Comite(nombre="comite-proyecto7", descripcion="comite de cambio", cantMiembro=5, proyectoId=p.idProyecto)
    MgrComite().guardar(c)
    MgrComite().asignarUsuario(nombreProyecto = "proyecto7",  nameUser= "stfy")    
    
    print ":cargo proyectos:"
        
def createAtrib():
    """ Carga tipos de atributos """
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
    t=TipoDeAtributo("texto100", "texto", 100,"atributo texto con 100 caracteres")
    MgrTipoDeAtrib().guardar(t)
    print ":cargo tipo de atributo:"
  
def createRol():
    """ Carga los roles del sistema """
    r = Rol(nombre="Administrador", descripcion="rol de administrador", ambito= "all project")
    MgrRol().guardar(r)
    MgrRol().asignarPermiso("Administrador", "all project", "ModuloAdministracion")
    r = Rol(nombre="Desarrollador", descripcion="rol de desarrollador", ambito= "all project")
    MgrRol().guardar(r)
    MgrRol().asignarPermiso("Desarrollador", "all project", "ModuloDesarrollo")
    r = Rol(nombre="LiderDeProyecto", descripcion="rol de lider", ambito= "all project")
    MgrRol().guardar(r)
    MgrRol().asignarPermiso("LiderDeProyecto", "all project", "ModuloGestion")
    print ":cargo los roles del sistema con los permisos:"

    
def createPermiso():
    """ Carga permisos predefinidos """
    p = Permiso("ModuloAdministracion","Acceso al modulo de administracion del sistema")
    MgrPermiso().guardar(p)
    p = Permiso("ModuloGestion","Acceso al modulo de gestion del sistema")
    MgrPermiso().guardar(p)
    p = Permiso("ModuloDesarrollo","Acceso al modulo desarrollo del sistema")
    MgrPermiso().guardar(p)

    p = Permiso("AdmUsuario","Permite crear/modificar/eliminar/cambiar de estado un usuario dentro de un proyecto")
    MgrPermiso().guardar(p)
    p = Permiso("AdmUsuariosDeProyecto","Permite asignar/desasignar usuarios a un proyecto del sistema")
    MgrPermiso().guardar(p)
    p = Permiso("AdmRolDeProyecto","Permite crear/modificar/eliminar/configurar un rol")
    MgrPermiso().guardar(p)
    p = Permiso("AdmAtributo","Permite crear/modificar/eliminar un tipo de atributo")
    MgrPermiso().guardar(p)
    p = Permiso("AdmComite","Permite crear/modificar un comite de cambio en un proyecto")
    MgrPermiso().guardar(p)
    p = Permiso("AdmUsuarioComite","Permite asignar/desasignar usuarios al comite de cambio de un proyecto")
    MgrPermiso().guardar(p)
    p = Permiso("CrearProyecto","Permite crear un proyecto en el sistema")
    MgrPermiso().guardar(p)
    p = Permiso("ModificarProyecto","Permite modificar datos de un proyecto")
    MgrPermiso().guardar(p)
    p = Permiso("AsignarLiderAProyecto","Permite asignar lider a un proyecto del sistema")
    MgrPermiso().guardar(p)

    p = Permiso("AdmRolesDeUsuarios","Permite asignar/desasignar Roles a Usuario de un proyecto")
    MgrPermiso().guardar(p)
    p = Permiso("CalculoCosto","Permite generar el costo")
    MgrPermiso().guardar(p)
    p = Permiso("CalculoImpacto","Permite generar el impacto")
    MgrPermiso().guardar(p)
    
    p = Permiso("AdmCambio","Permite administrar cambio")
    MgrPermiso().guardar(p)
    p = Permiso("AdmSolicitud","Permite gestionar una solicitud")
    MgrPermiso().guardar(p)
    p = Permiso("AdmReporte","Permite generar reporte")
    MgrPermiso().guardar(p)
    p = Permiso("AdmItemDeFase","Permite asignar item a fase")
    MgrPermiso().guardar(p)

    p = Permiso("AdmProyecto","Permite gestionar un proyecto")
    MgrPermiso().guardar(p)
    p = Permiso("AdmFase","Permite gestionar las fases de un proyecto")
    MgrPermiso().guardar(p)
    p = Permiso("AdmLB","Permite gestinar la LB dentro de una fase de un proyecto")
    MgrPermiso().guardar(p)
    p = Permiso("AdmTiposDeItem","Permite gestionar los tipos de item de una fase")
    MgrPermiso().guardar(p)
    p = Permiso("AdmItem","Permite gestionar item de una fase")
    MgrPermiso().guardar(p)
    print ":cargo permisos:"
 
    
def createTipoDeItem():
    """ Carga Tipo de Item con tipos de Atributos asignados """
    t = TipoDeItem(nombre="TipoDeItem1", descripcion="tipo de item con atributo numerico de precicion 20")
    MgrTipoDeItem().guardar(t)
    MgrTipoDeItem().asignarTipoDeAtrib(t.nombre, "numerico20")
    
    t = TipoDeItem(nombre="TipoDeItem2", descripcion="tipo de item con atributo numerico de precicion 20 y texto de 45 caracteres")
    MgrTipoDeItem().guardar(t)
    MgrTipoDeItem().asignarTipoDeAtrib(t.nombre, "numerico20")
    MgrTipoDeItem().asignarTipoDeAtrib(t.nombre, "texto45")
    
    t = TipoDeItem(nombre="TipoDeItem3", descripcion="tipo de item con atributo date y texto de 100 caracteres")
    MgrTipoDeItem().guardar(t)
    MgrTipoDeItem().asignarTipoDeAtrib(t.nombre, "date")
    MgrTipoDeItem().asignarTipoDeAtrib(t.nombre, "texto100")
    
    t = TipoDeItem(nombre="TipoDeItem4", descripcion="tipo de item con atributo date y texto de 45 caracteres")
    MgrTipoDeItem().guardar(t)
    MgrTipoDeItem().asignarTipoDeAtrib(t.nombre, "date")
    MgrTipoDeItem().asignarTipoDeAtrib(t.nombre, "texto45") 
    
    t = TipoDeItem(nombre="TipoDeItem5", descripcion="tipo de item con atributo numerico de precision 45")
    MgrTipoDeItem().guardar(t)
    MgrTipoDeItem().asignarTipoDeAtrib(t.nombre, "numerico45")
    
    t = TipoDeItem(nombre="TipoDeItem6", descripcion="tipo de item con atributo booleano y texto de 45 caracteres")
    MgrTipoDeItem().guardar(t)
    MgrTipoDeItem().asignarTipoDeAtrib(t.nombre, "booleano")  
    MgrTipoDeItem().asignarTipoDeAtrib(t.nombre, "texto45")    

    t = TipoDeItem(nombre="TipoDeItem7", descripcion="tipo de item con atributo numerico de precision de 20 digitos y texto de 100 caracteres ")
    MgrTipoDeItem().guardar(t)
    MgrTipoDeItem().asignarTipoDeAtrib(t.nombre, "numerico20")
    MgrTipoDeItem().asignarTipoDeAtrib(t.nombre, "texto100")
    
    print ":cargo tipo de item:"


def createFase():
    # proyecto 1
    p = MgrProyecto().filtrar("proyecto1")
    t = MgrTipoDeItem().filtrar("TipoDeItem1")
    f = Fase(nombre="proyecto1-fase1", descripcion="nueva fase", orden=1, proyectoId= p.idProyecto, tipoDeItemId=t.idTipoDeItem)
    MgrFase().guardar(f)
    
    p = MgrProyecto().filtrar("proyecto1")
    t = MgrTipoDeItem().filtrar("TipoDeItem1")
    f = Fase(nombre="proyecto1-fase2", descripcion="nueva fase", orden=2, proyectoId= p.idProyecto, tipoDeItemId=t.idTipoDeItem)
    MgrFase().guardar(f)
    
    p = MgrProyecto().filtrar("proyecto1")
    t = MgrTipoDeItem().filtrar("TipoDeItem2")
    f = Fase(nombre="proyecto1-fase3", descripcion="nueva fase", orden=3, proyectoId= p.idProyecto, tipoDeItemId=t.idTipoDeItem)
    MgrFase().guardar(f)
    
    p = MgrProyecto().filtrar("proyecto1")
    t = MgrTipoDeItem().filtrar("TipoDeItem3")
    f = Fase(nombre="proyecto1-fase4", descripcion="nueva fase", orden=4, proyectoId= p.idProyecto, tipoDeItemId=t.idTipoDeItem)
    MgrFase().guardar(f)
    
    # proyecto 2
    p = MgrProyecto().filtrar("proyecto2")
    t = MgrTipoDeItem().filtrar("TipoDeItem3")
    f = Fase(nombre="proyecto2-fase1", descripcion="nueva fase", orden=1, proyectoId= p.idProyecto, tipoDeItemId=t.idTipoDeItem)
    MgrFase().guardar(f)
    
    p = MgrProyecto().filtrar("proyecto2")
    t = MgrTipoDeItem().filtrar("TipoDeItem2")
    f = Fase(nombre="proyecto2-fase2", descripcion="nueva fase", orden=2, proyectoId= p.idProyecto, tipoDeItemId=t.idTipoDeItem)
    MgrFase().guardar(f)
    
    p = MgrProyecto().filtrar("proyecto2")
    t = MgrTipoDeItem().filtrar("TipoDeItem4")
    f = Fase(nombre="proyecto2-fase3", descripcion="nueva fase", orden=3, proyectoId= p.idProyecto, tipoDeItemId=t.idTipoDeItem)
    MgrFase().guardar(f)    
    
    p = MgrProyecto().filtrar("proyecto2")
    t = MgrTipoDeItem().filtrar("TipoDeItem2")
    f = Fase(nombre="proyecto2-fase4", descripcion="nueva fase", orden=4, proyectoId= p.idProyecto, tipoDeItemId=t.idTipoDeItem)
    MgrFase().guardar(f)    