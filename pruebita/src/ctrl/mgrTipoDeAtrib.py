from modulo import *

class MgrTipoDeAtrib():

    def listar(self):
        return TipoDeAtributo.query.all()
    
    def guardar(self, tipoDeAtributo):
        db.session.add(tipoDeAtributo)
        db.session.commit()
    
    def verificar_borrar(self,nombre):
        tipoDeAtributo = TipoDeAtributo.query.filter(TipoDeAtributo.nombre == nombre).first_or_404()
        item = TipoDeItem.query.all()
        idAtrib= tipoDeAtributo.idTipoDeAtributo
        for i in item:
            if tipoDeAtributo in i.atributosItem:
                hola = 1
            else:
                hola = 2
        return hola
                #db.session.delete(tipoDeAtributo)
                #db.session.commit()
                
    def borrar(self,nombre):
        tipoDeAtributo = TipoDeAtributo.query.filter(TipoDeAtributo.nombre == nombre).first_or_404()
        db.session.delete(tipoDeAtributo)
        db.session.commit()
        
    def modificar(self, nombre, nombreNew, tipoDeDatoNew, descripcionNew,
        detalleNew, filenameNew, archivoNew):
        atrib = TipoDeAtributo.query.filter(TipoDeAtributo.nombre == nombre).first_or_404()
        atrib.nombre = nombreNew
        atrib.tipoDeDato = tipoDeDatoNew
        atrib.detalle = detalleNew
        atrib.descripcion = descripcionNew
        atrib.filename = filenameNew
        atrib.archivo = archivoNew
        db.session.commit()

    def modificarArchivo(self, nombre, nombreNew, descripcionNew,
        detalleNew):
        atrib = TipoDeAtributo.query.filter(TipoDeAtributo.nombre == nombre).first_or_404()
        atrib.nombre = nombreNew
        atrib.detalle = detalleNew
        atrib.descripcion = descripcionNew
        db.session.commit()
        
    def filtrar(self, nombre):
        return TipoDeAtributo.query.filter(TipoDeAtributo.nombre == nombre).first_or_404()
    
    def descargar_archivo(self, nombre):
        atrib = TipoDeAtributo.query.filter(TipoDeAtributo.nombre == nombre).first_or_404()
        archivo = atrib.filename
        arc = open(archivo, "w")
        arc.write(atrib.archivo)
        arc.close()
        return atrib
    
    def descargar(self, nombre):
        """Funcion que recibe el nombre de tipo de atributo y descarga el archivo"""
        atrib = TipoDeAtributo.query.filter(TipoDeAtributo.nombre == nombre).first_or_404()
        archivo = atrib.filename
        return send_from_directory(app.config['UPLOAD_FOLDER'],
                               archivo)
    
    def listaAtrib(self, lista):
        lis = []
        for i in lista:
            atrib = TipoDeAtributo.query.filter(TipoDeAtributo.idTipoDeAtributo == i ).first_or_404()
            lis.append(atrib)
        return lis