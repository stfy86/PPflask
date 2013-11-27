from modulo import *
from sqlalchemy import or_, and_

class MgrProyecto():

    def guardar(self, project):
        if not self.existe(project):
            db.session.add(project)
            db.session.commit()
            return ":guardo el proyecto:"
        else:
            return ":no guardo el proyecto:"
      
    def borrar(self, project):
        if self.existe(project) and project.estado == "Finalizado":
            db.session.delete(project)
            db.session.commit()
            return ":borro proyecto:"
        else:
            return ":no borro proyecto: el estado del proyecto no es finalizado"
    
    def listar(self):
        return Proyecto.query.all()
     
    def filtrar(self, nombre):
        return Proyecto.query.filter(Proyecto.nombre == nombre).first_or_404()

    def listProjectPyF(self):
        return Proyecto.query.filter(or_(Proyecto.estado == "Pendiente", Proyecto.estado == "Finalizado")).all()
    
    def listarActivo(self):
        return Proyecto.query.filter(Proyecto.estado == "Activo").all()        

    def listarFinalizado(self):
        return Proyecto.query.filter(Proyecto.estado == "Finalizado").all()  
    
    def listarPendiente(self):
        return Proyecto.query.filter(Proyecto.estado == "Pendiente").all()  

    def modificar(self, nombre, descripcionNew, presupuestoNew):
        project = self.filtrar(nombre)
        if project.estado == "Pendiente":
            project.descripcion = descripcionNew
            project.presupuesto = presupuestoNew
            db.session.commit()
            return ":se modifico los datos del proyecto:"
        else:
            return ":NO modifico el proyecto de estado Pendiente:"
         
    def modificarOrden(self, project, fase, faseNew):
        if (project.estado == "Pendiente") and (fase in  self.fasesDeProyecto(project.nombre)) and (faseNew in  self.fasesDeProyecto(project.nombre)):
            aux = fase.orden
            fase.orden = faseNew.orden
            faseNew.orden = aux
            db.session.commit()
            return ":se modifico el orden:"
        else:
            return ":NO se puede modificar el orden"
        
    def estado(self, nombre, estadoNew):
        proyecto = self.filtrar(nombre)
        if estadoNew == "Activo" and self.proyectoIniciado(nombre):
            proyecto.estado = estadoNew        
            db.session.commit()
            return ":modifico el estado a Activo:"
        if estadoNew == "Finalizado" and self.proyectoFinalizado(nombre):
            proyecto.estado = estadoNew        
            db.session.commit()
            return ":modifico el estado Finalizado:"
        if estadoNew == "Inactivo":
            proyecto.estado = estadoNew        
            db.session.commit()
            return ":modifico el estado a Inactivo:"
        
        return":no modifico el estado:"
            
    def proyectoIniciado(self, nombre):
        """ Retorna true si todas las fases del proyecto estan en estado desarrollo """
        proyecto = self.filtrar(nombre)
        for fase in proyecto.listafases:
            if fase.estado != "Desarrollo":
                return False
        return True
        
    def proyectoFinalizado(self, nombre):
        """ Retorna true si todas las fases del proyecto estan en estado finalizado """
        proyecto = self.filtrar(nombre)
        for fase in proyecto.listafases:
            if fase.estado != "Finalizado":
                return False
        return True

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
        r = Rol.query.filter(and_(Rol.nombre == rol.nombre, Rol.ambito == rol.ambito)).first_or_404()
        p = self.filtrar(proyecto.nombre)
        u = User.query.filter(User.name == nameLider).first_or_404()
        if ((p.estado == "Pendiente") and (r in u.roles) and (u in p.users)):
            u.roles.remove(r)
            p.users.remove(u)
            db.session.commit()
            return ":desasigno el lider =>" + u.name + " al proyecto =>" + p.nombre +":"
        else:
            return ":error: no desasigno el lider "
        
    def asignarLider(self, proyecto, rol, nameLider):
        r = Rol.query.filter(and_(Rol.nombre == rol.nombre, Rol.ambito == rol.ambito)).first_or_404()
        p = self.filtrar(proyecto.nombre)
        u = User.query.filter(User.name == nameLider).first_or_404()
        if ((p.estado == "Pendiente") and (r in u.roles) and (u in p.users) and (u.estado == "Activo")):
            return ":error: no se asigno el lider"
        else:
            u.roles.append(r)
            p.users.append(u)
            db.session.commit()
            return ":asigno el lider =>" + u.name + " al proyecto =>" + p.nombre +":"
        
    def asignarUsuario(self, proyecto,  user, rol):
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

    
    
    def desasignarUsuario(self, proyecto, user, rol):
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
        proyecto = self.filtrar(nombre)
        return proyecto.users

    def filtrarXId(self, idProyecto):
        return Proyecto.query.filter(Proyecto.idProyecto == idProyecto).first_or_404()
    
    
    def fasesDeProyecto(self, nombre):
        proyecto = self.filtrar(nombre)
        return proyecto.listafases
    
    def nroDeFaseDeProyecto(self, nombre):
        proyecto = self.filtrar(nombre)
        cont = 0
        for i in proyecto.listafases:
            if i != None:
                cont = cont +  1
        return cont
    
    def ordenarFase(self, proyecto, fase):
        for i in proyecto.listafases:    
            f = Fase.query.filter(Fase.idFase == i.idFase).first()
            if f.orden > fase.orden and fase.orden != f.orden:
                f.orden = f.orden - 1
                db.session.commit()
        return ":ordeno las fases:"
    

    def fasesDeProyectosPendiente(self):
        proyectosPendientes = self.listarPendiente()
        fasesPendiente = []
        for p in proyectosPendientes:
            fasesPendiente.extend(self.fasesDeProyecto(p.nombre))
        return fasesPendiente
    

    def importarFase(self, proyecto, fase):
        if self.faseRepetida(proyecto, fase.nombre):
            return ":NO se puede importar fase:"
        else:          
            faseNew = Fase(nombre=fase.nombre, descripcion=fase.descripcion, orden= self.nroDeFaseDeProyecto(proyecto.nombre) + 1, proyectoId= proyecto.idProyecto, tipoDeItemId=fase.tipoDeItemId)
            db.session.add(faseNew)
            proyecto.listafases.append(faseNew)
            db.session.commit()
            return ":importo fase:"
        
                
    def faseRepetida(self, proyecto, nombreFase):           
        for n in proyecto.listafases:
            if n.nombre == nombreFase:
                return True
        return False
    
    def iniciarProyecto(self, proyecto):
        if proyecto.estado == "Pendiente" and self.sePuedeIniciar(proyecto):
            for i in proyecto.listafases:    
                f = Fase.query.filter(Fase.idFase == i.idFase).first()
                f.estado = "Activo" 
                db.session.commit()
            proyecto.estado = "Activo"
            db.session.commit()
            return ":se inicio el proyecto:"
        else:
            return ":NO se puede iniciar el proyecto:"
        
    def sePuedeIniciar(self, proyecto):
        if self.nroDeFaseDeProyecto(proyecto.nombre) > 0:           
            for i in proyecto.listafases:    
                f = Fase.query.filter(Fase.idFase == i.idFase).first()
                if (f.estado == "Finalizado" or f.estado == "Activo") and f.tipoDeItemId == None:
                    return False
            return True
        else:
            return False      
        
    def fasesActivasDeProyecto(self, nombre):
        proyecto = self.filtrar(nombre)
        return Fase.query.filter(and_(Fase.estado == "Activo", Fase.proyectoId == proyecto.idProyecto)).all()

    def existe(self, proyecto):
        p = Proyecto.query.filter(Proyecto.nombre == proyecto.nombre).first()
        if p != None:
            return True
        else:
            return False
        
    
    
    def ambitoDeUser(self, name):
        #user = self.filtrar(name)
        list = []
        for rol in name.roles:
            if not rol.ambito == "none project":
                proyecto = self.filtrar(rol.ambito)
                #li.extend(["two", "elements"])
                list.append([proyecto, rol.nombre])    
        return list
    
                
    def getLider(self, nombre):
        p = self.filtrar(nombre)
        r = Rol.query.filter(and_(Rol.nombre == "LiderDeProyecto", Rol.ambito == nombre)).first_or_404()
        for u in p.users:
            if r in u.roles:
                return u.name
        return None
    
    def getUserLider(self, idProyecto):
        p = self.filtrarXId(idProyecto)
        r = Rol.query.filter(and_(Rol.nombre == "LiderDeProyecto", Rol.ambito == p.nombre)).first_or_404()
        for u in p.users:
            if r in u.roles:
                user = User.query.filter(User.name == u.name).first()
                return user
        return None
    
    def finalizarProyecto(self, proyecto):
        if proyecto.estado == "Activo" and self.sePuedeFinalizar(proyecto):
            proyecto.estado = "Finalizado"
            db.session.commit()
            return ":se finalizo el proyecto:"
        else:
            return ":NO se puede finalizar el proyecto:"
        
    def sePuedeFinalizar(self, proyecto):
        for i in proyecto.listafases:    
            f = Fase.query.filter(Fase.idFase == i.idFase).first()
            if f.estado != "Finalizado":
                return False
        return True
        