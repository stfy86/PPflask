from modulo import *

class MgrComite():

    def guardar(self, comite):
        db.session.add(comite)
        db.session.commit()
        
    def borrar(self, comite):
        proyecto = Proyecto.query.filter(Proyecto.idProyecto == comite.proyectoId).first_or_404()
        if proyecto.estado == "Pendiente":
            db.session.delete(comite)
            db.session.commit()
            return ":borro el comite:"
        else:
            return ":no borro el comite:"
    
    def modificar(self, nombre, descripcionNew, cantMiembroNew):
        comite = Comite.query.filter(Comite.nombre == nombre).first_or_404()
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

    
    def asignarUsuario(self, nombreProyecto,  nameUser):
        proyecto = Proyecto.query.filter(Proyecto.nombre == nombreProyecto).first_or_404()
        comite = Comite.query.filter(Comite.proyectoId == proyecto.idProyecto).first_or_404()
        user = User.query.filter(User.name == nameUser).first_or_404()
        miembrosAsig = 0
        for u in comite.miembros:
            miembrosAsig = miembrosAsig + 1
        if miembrosAsig > comite.cantMiembro:
            return ":error: se supero la cantidad de miembros del comite"
        elif user in proyecto.users:
            comite.miembros.append(user)
            db.session.commit()
            return ":asigno el usuario =>" + user.name + " al comite =>" + comite.nombre + " del proyecto =>" + proyecto.nombre + ":" 
        else:
            return ":error: el usuario que desea asignar al comite no es miembro del proyecto"



    def desasignarUsuario(self, nombreProyecto,  nameUser):
        proyecto = Proyecto.query.filter(Proyecto.nombre == nombreProyecto).first_or_404()
        comite = Comite.query.filter(Comite.proyectoId == proyecto.idProyecto).first_or_404()
        user = User.query.filter(User.name == nameUser).first_or_404()
        if(user in proyecto.users):
            comite.miembros.remove(user)
            db.session.commit()
            return ":desasigno el usuario =>"+ user.name +" del comite =>" + comite.nombre + " del proyecto =>" + proyecto.nombre + ":"
        else:
            return ":error: el usuario no es miembro del comite"

    def searchXProyecto(self, nombreProyecto):
        proyecto = Proyecto.query.filter(Proyecto.nombre == nombreProyecto).first_or_404()
        comite = Comite.query.filter(Comite.proyectoId == proyecto.idProyecto).first_or_404()
        return comite.miembros

    def filtrarXProyecto(self, nombreProyecto):
        proyecto = Proyecto.query.filter(Proyecto.nombre == nombreProyecto).first_or_404()
        comite = Comite.query.filter(Comite.proyectoId == proyecto.idProyecto).first_or_404()
        return comite
    
    def nroMiembros(self, nombreProyecto):
        proyecto = Proyecto.query.filter(Proyecto.nombre == nombreProyecto).first_or_404()
        comite = Comite.query.filter(Comite.proyectoId == proyecto.idProyecto).first_or_404()
        nro = 0
        for u in comite.miembros:
            nro = nro +1
        return nro

    def search(self, nombreProyecto):
        proyecto = Proyecto.query.filter(Proyecto.nombre == nombreProyecto).first_or_404()
        comite = Comite.query.filter(Comite.proyectoId == proyecto.idProyecto).first_or_404()
        return comite
