from pruebita import db, app

class MgrTipoDeItem():

    def listar(self):
        """ listar items """
        from models import TipoDeItem
        return TipoDeItem.query.all()
    
    def guardar(self, tipoDeItem):
        """ guarda un registro tipoDeItem """
        db.session.add(tipoDeItem)
        db.session.commit()
    
    def borrar(self,nombre):
        """ borra un registro tipoDeItem x name"""
        from models import TipoDeItem
        tipoDeItem = TipoDeItem.query.filter(TipoDeItem.nombre == nombre).first_or_404()
        db.session.delete(tipoDeItem)
        db.session.commit()
        
    def modificar(self, nombre, nombreNew, descripcionNew):
        """ modificar un registro de tipo de item"""
        from models import TipoDeItem
        tipoDeItem = TipoDeItem.query.filter(TipoDeItem.nombre == nombre).first_or_404()
        tipoDeItem.nombre = nombreNew
        tipoDeItem.descripcion = descripcionNew     
        db.session.commit()

    def filtrar(self, nombre):
        """ filtrar proyecto por nombre """
        from models import TipoDeItem
        return TipoDeItem.query.filter(TipoDeItem.nombre == nombre).first_or_404()
    
    def asignarTipoDeAtrib2(self, nombre, listaTipoDeAtrib=[None], listaSinTipoDeAtrib=[None]):
        """ asigna un permiso a un rol """
        from models import TipoDeItem
        from ctrl.mgrTipoDeItemXTipoDeAtrib import MgrTipoDeItemXTipoDeAtrib
        # asigna al rol el permiso 
        for n in listaSinTipoDeAtrib:
            MgrTipoDeItemXTipoDeAtrib().borrar(nombre, n.nombre) 
        for u in listaTipoDeAtrib:
            MgrTipoDeItemXTipoDeAtrib().guardar(nombre, u)
            
    def asignarFase(self, nombre, opcion):
        """ asigna una fase a un tipo de item """
        from models import TipoDeItem, Fase
        tipoDeItem = TipoDeItem.query.filter(TipoDeItem.nombre == nombre).first_or_404()
        fase = Fase.query.filter(Fase.nombre == opcion).first_or_404()
        tipoDeItem.Fase = fase
        db.session.commit()
            
    def desasignarTipoDeAtrib(self, nombre, nombreTipoDeAtrib):
        """ asigna un permiso a un rol """
        from ctrl.mgrTipoDeItemXTipoDeAtrib import MgrTipoDeItemXTipoDeAtrib
        # asigna al rol el permiso 
        MgrTipoDeItemXTipoDeAtrib().borrar(nombre, nombreTipoDeAtrib) 
                    
    def filtrarTipoDeAtrib(self, nombre):
        """ filtrar rol por nombre """
        from models import TipoDeItem
        tipoDeItem = TipoDeItem.query.filter(TipoDeItem.nombre == nombre).first_or_404()
        return tipoDeItem.atributosItem
    
    def filtrarTipoDeItem(self, opcion):
        """ filtrar rol por nombre """
        from models import TipoDeItem
        tipoDeItem = TipoDeItem.query.filter(TipoDeItem.nombre == opcion).first_or_404()
        return tipoDeItem.nombre
    
    def filtrarFase(self, nombre):
        """ filtrar rol por nombre """
        from models import TipoDeItem, Fase
        tipoDeItem = TipoDeItem.query.filter(TipoDeItem.nombre == nombre).first_or_404     
        return tipoDeItem.Fase.idFase