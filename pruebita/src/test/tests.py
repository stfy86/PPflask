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
        u = User(name="stfy", passwd="stfy", nombre="estefanis", apellido="zamora", email="stfy@gmail.com", telefono=1111, obs="usuario nuevo")
        print MgrUser().guardar(u)
        
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
