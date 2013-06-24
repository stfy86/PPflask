from modulo import *

class MgrComite():

    def guardar(self, comite):
        proyecto = Proyecto.query.filter(Proyecto.idProyecto == comite.proyectoId).first_or_404()
        if proyecto.estado == "Pendiente":
            db.session.add(comite)
            db.session.commit()
            return ":borro el comite:"
        else:
            return ":no borro el comite:"
        
    def borrar(self, comite):
        proyecto = Proyecto.query.filter(Proyecto.idProyecto == comite.proyectoId).first_or_404()
        if proyecto.estado == "Pendiente":
            db.session.delete(comite)
            db.session.commit()
            return ":borro el comite:"
        else:
            return ":no borro el comite:"
    
    def modificar(self, comite, descripcionNew, cantMiembroNew):
        proyecto = Proyecto.query.filter(Proyecto.idProyecto == comite.proyectoId).first_or_404()
        if proyecto.estado == "Pendiente":
            comite.descripcion = descripcionNew
            comite.cantMiembro = cantMiembroNew
            db.session.commit()
            return ":modifico el comite:"
        else:
            return ":no modifico el comite:"
    
    def listar(self):
        return Comite.query.all()
       
    def filtrar(self, nombre):
        return Comite.query.filter(Comite.nombre == nombre).first_or_404()

    def filtrarXId(self, idComite):
        return Comite.query.filter(Comite.idComite == idComite).first_or_404()

    def asignarUsuario(self, nombreProyecto,  nameUser):
        comite = self.search(nombreProyecto)
        proyecto = Proyecto.query.filter(Proyecto.idProyecto == comite.idComite).first_or_404()
        user = User.query.filter(User.name == nameUser).first_or_404()
        
        if self.nroMiembros(proyecto.nombre) == comite.cantMiembro:
            return ":error: se supero la cantidad de miembros del comite"
        if user in proyecto.users and proyecto.estado == "Pendiente":
            comite.miembros.append(user)
            db.session.commit()
            return ":asigno el usuario =>" + user.name + " al comite =>" + comite.nombre + " del proyecto =>" + proyecto.nombre + ":" 
        else:
            return ":error: el usuario que desea asignar al comite no es miembro del proyecto"



    def desasignarUsuario(self, nombreProyecto,  nameUser):
        comite = self.search(nombreProyecto)
        user = User.query.filter(User.name == nameUser).first_or_404()     
        if(user in proyecto.users):
            comite.miembros.remove(user)
            db.session.commit()
            return ":desasigno el usuario =>"+ user.name +" del comite =>" + comite.nombre + " del proyecto =>" + proyecto.nombre + ":"
        else:
            return ":error: el usuario no es miembro del comite"

    def miembrosComite(self, nombreProyecto):
        comite = self.search(nombreProyecto)
        return comite.miembros

    
    def nroMiembros(self, nombreProyecto):
        comite = self.search(nombreProyecto)
        nro = 0
        for u in comite.miembros:
            nro = nro +1
        return nro

    def search(self, nombreProyecto):
        proyecto = Proyecto.query.filter(Proyecto.nombre == nombreProyecto).first_or_404()
        comite = Comite.query.filter(Comite.proyectoId == proyecto.idProyecto).first_or_404()
        return comite
    
    def listarPorProyecto(self, nombreProyecto):
        proyecto = Proyecto.query.filter(Proyecto.nombre == nombreProyecto).first_or_404()
        comite = Comite.query.filter(Comite.proyectoId == proyecto.idProyecto).all()
        return comite
