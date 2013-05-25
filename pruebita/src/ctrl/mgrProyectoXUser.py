from pruebita import db, app

class MgrProyectoXUser():

    def guardar(self, proyectoNombre, userName):
        """ asigna a un proyecto un usuario"""
        from models import Proyecto, User, users
        proyecto = Proyecto.query.filter(Proyecto.nombre == proyectoNombre).first_or_404()
        usuario = User.query.filter(User.name == userName).first_or_404() 
        proyecto.users.append(usuario)
        db.session.commit()         
    
    def borrar(self, proyectoNombre, userName):
        """ deasigna a un proyecto un usuario"""
        from models import Proyecto, User, users
        proyecto = Proyecto.query.filter(Proyecto.nombre == proyectoNombre).first_or_404()
        usuario = User.query.filter(User.name == userName).first_or_404() 
        proyecto.users.remove(usuario)
        db.session.commit()   

