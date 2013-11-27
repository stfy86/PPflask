from modulo import *

class MgrTipoDeItem():

    def listar(self):
        return TipoDeItem.query.all()
    
    def guardar(self, tipoDeItem):
        db.session.add(tipoDeItem)
        db.session.commit()
    
    def borrar(self,nombre):
        tipoDeItem = TipoDeItem.query.filter(TipoDeItem.nombre == nombre).first_or_404()
        db.session.delete(tipoDeItem)
        db.session.commit()
        
    def modificar(self, nombre, nombreNew, descripcionNew):
        tipoDeItem = TipoDeItem.query.filter(TipoDeItem.nombre == nombre).first_or_404()
        tipoDeItem.nombre = nombreNew
        tipoDeItem.descripcion = descripcionNew     
        db.session.commit()

    def filtrarXId(self, idTipoDeItem):
        return TipoDeItem.query.filter(TipoDeItem.idTipoDeItem == idTipoDeItem).first_or_404()
    
    def filtrar(self, nombre):
        return TipoDeItem.query.filter(TipoDeItem.nombre == nombre).first_or_404()
    
    def asignarTipoDeAtrib2(self, tipoDeItem, listaTipoDeAtrib=[None], listaSinTipoDeAtrib=[None]):
        for n in listaSinTipoDeAtrib:
            tipoDeAtrib = TipoDeAtributo.query.filter(TipoDeAtributo.nombre == n.nombre).first_or_404()
            tipoDeItem.atributosItem.remove(tipoDeAtrib) 
            db.session.commit()
        for u in listaTipoDeAtrib:
            tipoDeAtrib = TipoDeAtributo.query.filter(TipoDeAtributo.nombre == u).first_or_404()
            tipoDeItem.atributosItem.append(tipoDeAtrib) 
            db.session.commit()
            
    def asignarFase(self, nombre, opcion):
        tipoDeItem = TipoDeItem.query.filter(TipoDeItem.nombre == nombre).first_or_404()
        fase = Fase.query.filter(Fase.nombre == opcion).first_or_404()
        tipoDeItem.Fase = fase
        db.session.commit()
            
    def desasignarTipoDeAtrib(self, nombre, nombreTipoDeAtrib):
        MgrTipoDeItemXTipoDeAtrib().borrar(nombre, nombreTipoDeAtrib) 
                    
    def filtrarTipoDeAtrib(self, nombre):
        tipoDeItem = TipoDeItem.query.filter(TipoDeItem.nombre == nombre).first_or_404()
        return tipoDeItem.atributosItem
    
    def filtrarTipoDeItem(self, opcion):
        tipoDeItem = TipoDeItem.query.filter(TipoDeItem.nombre == opcion).first_or_404()
        return tipoDeItem.nombre
    
    def filtrarFase(self, nombre):
        tipoDeItem = TipoDeItem.query.filter(TipoDeItem.nombre == nombre).first_or_404     
        return tipoDeItem.Fase.idFase
    
    def asignarTipoDeAtrib(self, nombre, nombreTipoDeAtrib):
        tipoDeItem = TipoDeItem.query.filter(TipoDeItem.nombre == nombre).first_or_404()
        tipoDeAtrib= TipoDeAtributo.query.filter(TipoDeAtributo.nombre == nombreTipoDeAtrib).first_or_404()   
        if not tipoDeAtrib in tipoDeItem.atributosItem:
            tipoDeItem.atributosItem.append(tipoDeAtrib)
            db.session.commit()
            return ":asigno tipo de atributo a tipo de item:"
        else:
            return ":error: no asigno tipo de atributo a tipo de item"
        
    def desasignarTipoDeAtrib(self, nombre, nombreTipoDeAtrib):
        tipoDeItem = TipoDeItem.query.filter(TipoDeItem.nombre == nombre).first_or_404()
        tipoDeAtrib= TipoDeAtributo.query.filter(TipoDeAtributo.nombre == nombreTipoDeAtrib).first_or_404() 
        if tipoDeAtrib in tipoDeItem.atributosItem:
            tipoDeItem.atributosItem.remove(tipoDeAtrib)
            db.session.commit()
            return ":desasigno tipo de atributo de tipo de item:"
        else:
            return ":error: no desasigno tipo de atributo de tipo de item"

    def atributosDeTipoDeItem(self, tipoDeItem):
        return tipoDeItem.atributosItem
    
    def existe(self, tipoDeItem):
        t = TipoDeItem.query.filter(TipoDeItem.nombre == tipoDeItem.nombre).first()
        if t != None:
            return True
        else:
            return False

    def asignarAtributosItem(self, tipoDeItem, listaAtrib):
        for a in listaAtrib:
            tipoDeItem.atributosItem.append(a)
        db.session.commit()