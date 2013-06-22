from modulo import *

class MgrProyecto():

    def guardar(self,project):
        db.session.add(project)
        db.session.commit()
        
    def borrar(self,nombre):
        project = Proyecto.query.filter(Proyecto.nombre == nombre).first_or_404()
        db.session.delete(project)
        db.session.commit()
    
    def modificar(self, nombre, descripcionNew, presupuestoNew):
        project = Proyecto.query.filter(Proyecto.nombre == nombre).first_or_404()
        if project.estado == "Activo":
            project.descripcion = descripcionNew
            project.presupuesto = presupuestoNew
            db.session.commit()
            return ":se modifico los datos del proyecto:"
        else:
            return ":error: no se puede modificar los datos del proyecto"
         
    def listar(self):
        return Proyecto.query.all()
       
    def filtrar(self, nombre):
        return Proyecto.query.filter(Proyecto.nombre == nombre).first_or_404()

    def estado(self, nombre, estadoNew):
        proyecto = Proyecto.query.filter(Proyecto.nombre == nombre).first_or_404()
        proyecto.estado = estadoNew        
        db.session.commit()
    
    def asignarFase(self, nombre, nombreFase, descripcionFase, ordenFase, tipoDeItemIdFase):
        proyecto = Proyecto.query.filter(Proyecto.nombre == nombre).first_or_404()
        fase = Fase(nombre = nombreFase, descripcion = descripcionFase, orden = ordenFase , proyectoId= proyecto.idProyecto, tipoDeItemId = tipoDeItemIdFase )    
        tipoDeItem = TipoDeItem.query.filter(TipoDeItem.idTipoDeItem == tipoDeItemIdFase).first_or_404()
        for n in proyecto.listafases:
            if n.nombre == fase.nombre:
                return ":error: nombre de fase repetida"

        if(fase not in proyecto.listafases):
            db.session.add(fase)
            proyecto.listafases.append(fase)
            db.session.commit()
            return ":asigno fase =>" +fase.nombre + " al proyecto =>" + proyecto.nombre + " con el tipo de item  =>" + tipoDeItem.nombre + ":"
        else:
            return ":error:"
        
    def deasignarLider(self, proyecto, rol, nameLider):
        r = Rol.query.filter(Rol.nombre == rol.nombre, Rol.ambito == rol.ambito).first_or_404()
        p = Proyecto.query.filter(Proyecto.nombre == proyecto.nombre).first_or_404()
        u = User.query.filter(User.name == nameLider).first_or_404()
        if ((p.estado == "Activo") and (r in u.roles) and (u in p.users)):
            u.roles.remove(r)
            p.users.remove(u)
            db.session.commit()
            return ":desasigno el lider =>" + u.name + " al proyecto =>" + p.nombre +":"
        else:
            return ":error: no desasigno el lider "
        
    def asignarLider(self, proyecto, rol, nameLider):
        r = Rol.query.filter(Rol.nombre == rol.nombre, Rol.ambito == rol.ambito).first_or_404()
        p = Proyecto.query.filter(Proyecto.nombre == proyecto.nombre).first_or_404()
        u = User.query.filter(User.name == nameLider).first_or_404()
        p.estado = "Activo"
        u.estado = "Activo"
        if ((r in u.roles) and (u in p.users)):
            return ":error: no se asigno el lider"
        else:
            u.roles.append(r)
            p.users.append(u)
            db.session.commit()
            return ":asigno el lider =>" + u.name + " al proyecto =>" + p.nombre +":"
        
    def asignarUsuario(self, nombre,  nameUser, nombreRol):
        # verifica q exista  el proyecto, el usuario y el rol de proyecto
        proyecto = Proyecto.query.filter(Proyecto.nombre == nombre).first_or_404()
        user = User.query.filter(User.name == nameUser).first_or_404()
        rol = Rol.query.filter(Rol.nombre == nombreRol, Rol.ambito == nombre).first_or_404()
        if((rol not in user.roles) and (user not in proyecto.users)):
            user.estado = "Activo"
            # asigna el rol al usuario
            user.roles.append(rol)
            # asigna el usuario al proyecto 
            proyecto.users.append(user)
            db.session.commit()
            return ":asigno el usuario =>" + user.name + "al proyecto =>" + proyecto.nombre +" con el rol =>"+ rol.nombre + ":"
        else:
            return ":error:"

    
    
    def desasignarUsuario(self, nombre,  nameUser, nombreRol):
        # verifica q exista  el proyecto, el usuario y el rol de proyecto
        proyecto = Proyecto.query.filter(Proyecto.nombre == nombre).first_or_404()
        user = User.query.filter(User.name == nameUser).first_or_404()
        rol = Rol.query.filter(Rol.nombre == nombreRol, Rol.ambito == nombre).first_or_404()
        
        if((not rol.nombre == "LiderDeProyecto" ) and (rol in user.roles) and (user in proyecto.users)):
            # desasigna el rol al usuario
            user.roles.remove(rol)
            # deasigna del proyecto el usuario 
            proyecto.users.remove(user)
            db.session.commit()
            return ":desasigno usuario =>" + user.name + " del proyecto =>" + proyecto.nombre + " con el rol =>" + rol.nombre + ":"
        elif not user in proyecto.users:
            return ":error: el usuario no es miembro del proyecto"
        elif rol.nombre == "LiderDeProyecto" :
            return ":error: no se permite eliminar un lider de proyecto"        
        elif not rol in user.roles:
            return ":error: no existe el rol en el proyecto"
        else:
            return ":error:"

    def usersDeProyecto(self, nombre):
        proyecto = Proyecto.query.filter(Proyecto.nombre == nombre).first_or_404()
        return proyecto.users

    def filtrarXId(self, idProyecto):
        return Proyecto.query.filter(Proyecto.idProyecto == idProyecto).first_or_404()
    
    
    def fasesDeProyecto(self, nombre):
        proyecto = Proyecto.query.filter(Proyecto.nombre == nombre).first_or_404()
        return proyecto.listafases
    
    def nroDeFaseDeProyecto(self, nombre):
        proyecto = Proyecto.query.filter(Proyecto.nombre == nombre).first_or_404()
        cont = 0
        for i in proyecto.listafases:
            if i != None:
                cont = cont +  1
        return cont
    
    def filtrarItemSolicitud(self, nombre):
        from models.solicitud import *
        from models.comite import *
        from models.proyecto import *
        
        solicitud = Solicitud.query.filter(Solicitud.nombre == nombre).first_or_404()
        proyecto = solicitud.Comite.Proyecto
        
        itemsSolicitud = []
        
        for f in proyecto.listafases:
            for lb in f.listaLineaBase:
                if lb.estado == 'Aprobado':
                    itemsSolicitud.extend(lb.itemsLB)
                    
        return itemsSolicitud