# To change this template, choose Tools | Templates
# and open the template in the editor.
from flask.ext.script import Manager, Option
from pruebita import app, db

manager = Manager(app)

@manager.command
def initdb():
    db.create_all()
   
@manager.option('-u','--user', dest='user', default='admin', help='Username')
@manager.option('-p','--password', dest='password', default='password', help='Password')
@manager.option('-n','--nombre', dest='nombre', default='nombre', help='Nombre')
@manager.option('-a','--apellido', dest='apellido', default='apellido', help='Apellido')
@manager.option('-e','--email', dest='email', default='email', help='Email')
@manager.option('-t','--telefono', dest='telefono', default='telefono', help='Telefono')
@manager.option('-o','--obs', dest='obs', default='obs', help='Obs')
def createUser(user, password, nombre, apellido, email, telefono, obs):
    """Creo el usuario: user""" 
    from pruebita import User
    u=User(user, password, nombre, apellido, email,telefono, obs)
    db.session.add(u)
    db.session.commit()
   

@manager.command
def dropdb():
    """Elimino la base de datos."""
    db.drop_all()


if __name__ == '__main__':
    manager.run()


