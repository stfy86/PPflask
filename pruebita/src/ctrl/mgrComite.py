""" Clase que maneja comite """
from modulo import *

class MgrComite():

    def guardar(self, comite):
        """ Guarda un comite si el proyecto esta en estado pendiente
        y el nombre del comite no se repite """
        proyecto = Proyecto.query.filter(Proyecto.idProyecto == comite.proyectoId).first_or_404()
        if proyecto.estado == "Pendiente" and not self.existe(comite) :
            db.session.add(comite)
            db.session.commit()
            return ":guardo el comite:"
        else:
            return ":NO guardo el comite:"
        
    def borrar(self, comite):
        """ Borra el comite si el proyecto esta en estado pendiente y si el comite existe """
        proyecto = Proyecto.query.filter(Proyecto.idProyecto == comite.proyectoId).first_or_404()
        if  proyecto.estado == "Pendiente" and self.existe(comite):
            db.session.delete(comite)
            db.session.commit()
            return ":borro el comite:"
        else:
            return ":NO borro el comite:"
    
    def modificar(self, comite, descripcionNew, cantMiembroNew):
        """ Edita el comite si el proyecto esta en estado pendiente y si el comite existe """
        proyecto = Proyecto.query.filter(Proyecto.idProyecto == comite.proyectoId).first_or_404()
        if proyecto.estado == "Pendiente" and self.existe(comite):
            comite.descripcion = descripcionNew
            comite.cantMiembro = cantMiembroNew
            db.session.commit()
            return ":modifico el comite:"
        else:
            return ":NO modifico el comite:"
    
    def listar(self):
        """ Lista todos los comite"""
        return Comite.query.all()
       
    def filtrar(self, nombre):
        """ Busca por nombre de comite """
        return Comite.query.filter(Comite.nombre == nombre).first_or_404()

    def filtrarXId(self, idComite):
        """ Busca por Id de comite"""
        return Comite.query.filter(Comite.idComite == idComite).first_or_404()

    def asignarUsuario(self, proyecto,  user):
        """ Asigna usuario al comite, solo si:
        1. El proyecto esta en estado Pendiente
        2. No se supera la cantidad de miembros del comite
        3. El usuario que se quiere asignar es miembro actual del proyecto"""
        comite = Comite.query.filter(Comite.proyectoId == proyecto.idProyecto).first_or_404()
        if proyecto.estado == "Pendiente":            
            if self.nroMiembros(proyecto.nombre) == comite.cantMiembro:
                return ":NO asigno el usuario: se supero la cantidad de miembros del comite"
            if user in proyecto.users:
                comite.miembros.append(user)
                db.session.commit()
                return ":asigno el usuario =>" + user.name + " al comite =>" + comite.nombre + " del proyecto =>" + proyecto.nombre + ":" 
            else:
                return ":NO asigno el usuario: el usuario que desea asignar al comite no es miembro del proyecto"
        else:
            return ":No asigno el usuario: el proyecto no tiene estado pendiente"


    def desasignarUsuario(self, proyecto,  user):
        """ Desasigna un usuario del comite de un proyecto """
        comite = self.search(proyecto.nombre)
        if user in proyecto.users:
            comite.miembros.remove(user)
            db.session.commit()
            return ":desasigno el usuario =>"+ user.name +" del comite =>" + comite.nombre + " del proyecto =>" + proyecto.nombre + ":"
        else:
            return ":No desasigno el usuario: el usuario no es miembro del comite"

    def miembrosComite(self, nombreProyecto):
        """ Lista de miembros del comite del proyecto """
        comite = self.search(nombreProyecto)
        return comite.miembros

    
    def nroMiembros(self, nombreProyecto):
        """ Retorna el numero de usuarios del comite del proyecto """
        nro = 0
        for u in self.miembrosComite(nombreProyecto):
            nro = nro +1
        return nro

    def search(self, nombreProyecto):
        """ Busca el comite del proyecto"""
        proyecto = Proyecto.query.filter(Proyecto.nombre == nombreProyecto).first_or_404()
        comite = Comite.query.filter(Comite.proyectoId == proyecto.idProyecto).first_or_404()
        return comite
    
    def filtrarXIdProyecto(self, idProyecto):  
        """ Filtra comite por id del Proyecto """
        return Comite.query.filter(Comite.proyectoId == idProyecto).all()

    def existe(self, comite):
        """ Retorna True si el comite ya existe y False en caso contrario """
        c = Comite.query.filter(Comite.nombre == comite.nombre).first()
        if c != None:
            return True
        else:
            return False
        
    def esUsuario(self, comite, user):
        """Retorna True si el usuario es miembro del comite """
        if user in comite.miembros:
            return True
        else:
            return False