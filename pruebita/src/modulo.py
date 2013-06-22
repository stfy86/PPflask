#------------------------------------------------------------------------------#
# IMPORTS
#------------------------------------------------------------------------------#
from flask import Flask, request, send_file
from pruebita import app, db
from form import *
# paquete models
from models.comite import Comite, miembros
from models.fase import Fase
from models.item import Item
from models.lineaBase import LineaBase, itemsLB
from models.permiso import Permiso
from models.proyecto import Proyecto, users
from models.relacion import Relacion
from models.rol import Rol, permisos
from models.solicitud import Solicitud, itemsSolicitud
from models.tipoDeAtributo import TipoDeAtributo
from models.tipoDeItem import TipoDeItem, atributosItem
from models.user import User, roles
# paquete ctrl
from ctrl.mgrFase import MgrFase
from ctrl.mgrItem import MgrItem
from ctrl.mgrPermiso import MgrPermiso
from ctrl.mgrProyecto import MgrProyecto
from ctrl.mgrRol import MgrRol
from ctrl.mgrTipoDeAtrib import MgrTipoDeAtrib
from ctrl.mgrUser import MgrUser
from ctrl.mgrComite import MgrComite
from ctrl.mgrRolXPermiso import MgrRolXPermiso
from ctrl.mgrTipoDeItem import MgrTipoDeItem
# paquete views
from views.ingreso import *
from views.administracion import *
from views.gestion import *
from views.desarrollo import *
from views.sistema import *



