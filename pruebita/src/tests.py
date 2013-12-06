#!virtualenv/bin/python
import os
import unittest
import tempfile
from flask import jsonify, json
from flask import Flask

from pruebita import db, app
from modulo import *

class TestCase(unittest.TestCase):
    
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@localhost:5432/databasePrueba'
        self.db = db
        self.app = app.test_client() 
        db.create_all()
     
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # usuarios   
    def testUsuario(self):
        print "Test Crear Usuario"
        u = User(name="stfy", passwd="stfy", nombre="estefanis", apellido="zamora", email="stfy@gmail.com", telefono=1111, obs="usuario nuevo")
        print MgrUser().guardar(u)
        u = User(name="admin", passwd="admin", nombre="administrador", apellido="administrador", email="admin@gmail.com", telefono=1234, obs="administrador del sistema")
        print MgrUser().guardar(u)
        print "Test Modificar un usuario"
        u = MgrUser().filtrar("stfy")
        print MgrUser().modificar(u,passwordNew = "stfy", confirmacionNew ="stfy", nombreNew="estefanis", apellidoNew="zamora", emailNew = "stfy@gmail.com", telefonoNew = 222222, obsNew="usuario modif")
        print "Test Crear Usuario Doble"
        uRepetido = User(name="stfy", passwd="stfy", nombre="estefanis", apellido="zamora", email="stfy@gmail.com", telefono=1111, obs="usuario nuevo")
        print MgrUser().guardar(uRepetido)
        
    
    def testProyecto(self):
        print "Guardar Proyecto"
        p=Proyecto("proyectoTest","test")
        MgrProyecto().guardar(p)
        print "Fin de prueba ProyectoGuardar: guardo proyectoTest" 
        
        print "Guardar Vacio"
        name =""
        p=Proyecto()
        MgrProyecto().guardar(p)
        print "Fin de prueba ProjectGuardarVacio" 
        assert name == p.nombre
        
        print "Guardar proyecto doble"
        name="proyectoTest"
        pRepetido=Proyecto("proyectoTest","test")
        MgrProyecto().guardar(pRepetido)
        print "Fin de Prueba ProjectGuardarDoble: "
        assert name == p.nombre

        print "Borrar proyecto inexistente"
        name = "feo"
        p=Proyecto("proyectoTestfeo","test")
        MgrProyecto().borrar(p.nombre)
        print "Error: Fin de prueba ProyectoBorrarInexistente:" 
        assert name == p.nombre
    
    def testFase(self):
        
        p=Proyecto("proyectoTest","test")
        MgrProyecto().guardar(p)
        p = MgrProyecto().filtrar("proyectoTest")        
        
        f=Fase("faseTest","rest",1, p.idProyecto)
        MgrFase().guardar(f)
        print "Fin de prueba FaseGuardar" 
        
        nombre =""
        p=Fase()
        MgrFase().guardar(p)
        print "Error: Fin de prueba FaseGuardarVacio" 
        assert nombre == f.nombre
        
        nombre = "faseTest"
        f=Fase(nombre,"fase inicial",1, p.idProyecto)
        MgrFase().guardar(f)
        print "Error: Fin de Prueba FaseGuardarDoble: "
        assert nombre == f.nombre
      
        nombre = "faseTest1"
        f=Fase(nombre,"fase inicial",1 ,p.idProyecto)
        MgrFase().borrar(f.nombre)
        print "Error: Fin de prueba FaseBorrarInexistente:" 
        assert nombre == f.nombre
    
    def testAtrib(self):
        nombre = "atrib1"
        u =TipoDeAtributo("atrib1","numerico","30","atrib numerico precision 30")
        MgrTipoDeAtrib().guardar(u)
        print "Fin de prueba testAtribGuardar: guardo atrib1" 
        assert nombre == u.nombre
        
        nombre =""
        u=TipoDeAtributo()
        MgrTipoDeAtrib().guardar(u)
        print "Error: Fin de prueba testTipoDeAtribGuardarVacio" 
        assert nombre == u.nombre
        
        nombre = "atrib1"
        u =TipoDeAtributo("atrib1","numerico","30","atrib numerico precision 30")
        MgrTipoDeAtrib().guardar(u)
        print "Error: Fin de Prueba testTipoDeAtribGuardarDoble: "
        assert nombre == u.nombre
        
        nombre = "feo"
        u =TipoDeAtributo("feo","texto","30","atrib texto precision 30")
        MgrTipoDeAtrib().borrar(u.nombre)      
        print "Error: Fin de prueba testTipoDeAtribBorrarInexistente:" 
        assert nombre == u.nombre
    

    
    # login - logout    
    def login(self, username, password):
        print "login"
        final= {'username':username,'password':password}
        data = json.dumps(final)
        return self.app.post('/login', data=data, 
            follow_redirects=True)

    def logout(self):
        print "logout"
        return self.app.get('/logout', follow_redirects=True)
    
    def testLoginLogout(self):
        print "longin - logout"
        rv = self.login('stfy', 'stfy')
        dato = json.loads(rv.data)
        print "Esta logueado como",dato["usuario"]
        rv = self.logout()

    

if __name__ == '__main__':
    unittest.main()
