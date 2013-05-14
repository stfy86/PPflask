from pruebita import db, app

class MgrUser():

    def listar(self):
        """ listar usuarios """
        from models import User
        return User.query.all()
    
    def guardar(self, usuario):
        """ guarda un registro usuario """
        db.session.add(usuario)
        db.session.commit()
    
    def estado(self, nombre, estadoNew):
        """ guarda el nuevo estado del usuario """
        from models import User
        user = User.query.filter(User.name == nombre).first_or_404()
        user.estado = estadoNew        
        db.session.commit()
    
    def borrar(self,nombre):
        """ borra un registro usuario x name"""
        from models import User
        user = User.query.filter(User.name == nombre).first_or_404()
        db.session.delete(user)
        db.session.commit()
        
    def modificar(self, nombre, nameNew, passwordNew, nombreNew, apellidoNew,
                    emailNew, telefonoNew, obsNew):
        """ modificar un registro de usuario"""
        from models import User
        user = User.query.filter(User.name == nombre).first_or_404()
        user.name = nameNew
        user.password = passwordNew
        user.nombre = nombreNew
        user.apellido = apellidoNew
        user.email = emailNew
        user.telefono = telefonoNew
        user.obs = obsNew        
        db.session.commit()
        
    def filtrar(self, nombre):
        """ filtrar proyecto por nombre """
        from models import User
        return User.query.filter(User.name == nombre).first_or_404()
    
         
    
