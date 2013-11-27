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
    per =  MgrPermiso().filtrarXModulo("ModuloGestion")
    r = Rol(nombre="LiderDeProyecto", descripcion="rol de lider", ambito= p.nombre, permisos=per)
    MgrRol().guardar(r)
    MgrProyecto().asignarLider(proyecto = p , rol = r, nameLider = "lory")
    p = MgrProyecto().filtrar("proyecto1")
    c = Comite(nombre="comite-proyecto1", descripcion="comite de cambio", cantMiembro=3, proyectoId=p.idProyecto)
    MgrComite().guardar(c)
    u = MgrProyecto().getUserLider(p.idProyecto)
    MgrComite().asignarUsuario(p,u)

    p = Proyecto(nombre="proyecto2", descripcion="sistema 2", presupuesto=20000)
    MgrProyecto().guardar(p)
    per =  MgrPermiso().filtrarXModulo("ModuloGestion")
    r = Rol(nombre="LiderDeProyecto", descripcion="rol de lider", ambito= p.nombre, permisos=per)
    MgrRol().guardar(r)
    MgrProyecto().asignarLider(proyecto = p , rol = r, nameLider = "vavi")
    p = MgrProyecto().filtrar("proyecto2")
    c = Comite(nombre="comite-proyecto2", descripcion="comite de cambio", cantMiembro=4, proyectoId=p.idProyecto)
    MgrComite().guardar(c)
    u = MgrProyecto().getUserLider(p.idProyecto)
    MgrComite().asignarUsuario(p,u)

    p = Proyecto(nombre="proyecto3", descripcion="sistema 3", presupuesto=30000)
    MgrProyecto().guardar(p)
    per =  MgrPermiso().filtrarXModulo("ModuloGestion")
    r = Rol(nombre="LiderDeProyecto", descripcion="rol de lider", ambito= p.nombre, permisos=per)
    MgrRol().guardar(r)
    MgrProyecto().asignarLider(proyecto = p , rol = r, nameLider = "guille")
    p = MgrProyecto().filtrar("proyecto3")
    c = Comite(nombre="comite-proyecto3", descripcion="comite de cambio", cantMiembro=5, proyectoId=p.idProyecto)
    MgrComite().guardar(c)
    u = MgrProyecto().getUserLider(p.idProyecto)
    MgrComite().asignarUsuario(p,u)

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
    per =  MgrPermiso().filtrarXModulo("ModuloAdministracion")
    r = Rol(nombre="Administrador", descripcion="rol de administrador", ambito= "none project", permisos=per)
    MgrRol().guardar(r)
       
    per =  MgrPermiso().filtrarXModulo("ModuloDesarrollo")   
    r = Rol(nombre="Desarrollador", descripcion="rol de desarrollador", ambito= "none project", permisos = per)
    MgrRol().guardar(r)
    
    per =  MgrPermiso().filtrarXModulo("ModuloGestion")
    r = Rol(nombre="LiderDeProyecto", descripcion="rol de lider", ambito= "none project", permisos=per)
    MgrRol().guardar(r)
  
    per = []
    r = Rol(nombre="Invitado", descripcion="invitado del sistema", ambito= "none project", permisos=per)
    MgrRol().guardar(r)
    print ":cargo los roles del sistema con los permisos:"

    
def createPermiso():
    """ Carga permisos predefinidos """
    # Permisos del Sistema
    p = Permiso("ModuloAdministracion","permite acceder al modulo de administracion",1)
    MgrPermiso().guardar(p)
    p = Permiso("ModuloGestion","permite acceder al modulo de gestion",2)
    MgrPermiso().guardar(p)
    p = Permiso("ModuloDesarrollo","permite acceder al modulo de desarrollo",3)
    MgrPermiso().guardar(p)
    
    
    #Administrador
    p = Permiso("AdmUsuario","Permite crear/modificar/eliminar/cambiar de estado un usuario dentro de un proyecto",1)
    MgrPermiso().guardar(p)
    p = Permiso("AdmAtributo","Permite crear/modificar/eliminar un tipo de atributo",1)
    MgrPermiso().guardar(p)
    p = Permiso("AdmComite","Permite crear/modificar un comite de cambio en un proyecto",1)
    MgrPermiso().guardar(p)
    p = Permiso("AdmProyecto","Permite crear/modificar/eliminar/modificar estado/asignar lider un proyecto en el sistema",1)
    MgrPermiso().guardar(p)
   
    #Lider
    p = Permiso("GesUsuarioComite","Permite asignar/desasignar usuarios al comite de cambio de un proyecto",2)
    MgrPermiso().guardar(p)
    p = Permiso("Calculo","Permite generar el calculo de costo e impacto",2)
    MgrPermiso().guardar(p)
    p = Permiso("GesProyecto","Permite gestionar un proyecto, iniciar o finalizar",2)
    MgrPermiso().guardar(p)
    p = Permiso("GesFase","Permite gestionar las fases de un proyecto",2)
    MgrPermiso().guardar(p)
    p = Permiso("GesLB","Permite gestinar la LB dentro de una fase de un proyecto",2)
    MgrPermiso().guardar(p)
    p = Permiso("GesTiposDeItem","Permite crear/modificar/eliminar los tipos de item de una fase",2)
    MgrPermiso().guardar(p)
    p = Permiso("GesUserProyecto","Permite asignar/desasignar usuarios a un proyecto del sistema",2)
    MgrPermiso().guardar(p)
    p = Permiso("GesRolProyecto","Permite crear/modificar/eliminar/configurar un rol",2)
    MgrPermiso().guardar(p)

    #desarrollador
    p = Permiso("DesCambio","Permite realizar cambio",3)
    MgrPermiso().guardar(p)
    p = Permiso("DesSolicitud","Permite realizar una solicitud",3)
    MgrPermiso().guardar(p)
    p = Permiso("DesReporte","Permite desarrollar un reporte de un proyecto, fase e item",3)
    MgrPermiso().guardar(p)
    p = Permiso("DesItemFase","Permite desarrollar un item en una fase",3)
    MgrPermiso().guardar(p)
    p = Permiso("DesItem","Permite realizar un item",3)
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
    
def asignarRol():
    rol = MgrRol().search("Invitado", "none project")
    user = MgrUser().filtrar("stfy")
    MgrUser().addRol(user, rol)
    user = MgrUser().filtrar("lory")
    MgrUser().addRol(user, rol)
    user = MgrUser().filtrar("vavi")
    MgrUser().addRol(user, rol)
    user = MgrUser().filtrar("guille")
    MgrUser().addRol(user, rol)
    rol = MgrRol().search("Administrador", "none project")
    user = MgrUser().filtrar("admin")
    MgrUser().addRol(user, rol)
    
    print ":creo invitados:"    
