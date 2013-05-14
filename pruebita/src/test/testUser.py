# To change this template, choose Tools | Templates
# and open the template in the editor.

import unittest


class  TestUserCase(unittest.TestCase):
    #def setUp(self):
    #    self.foo = New_()
    #

    #def tearDown(self):
    #    self.foo.dispose()
    #    self.foo = None

    def testUserGuardar(self):
        from models import User
        from ctrl.mgrUser import MgrUser
        name = "admin2"
        u =User("admin2","admin2","administrador","administrador","admin@gmail.com",1234,"usuario administrador")
        MgrUser().guardar(u)
        print "Fin de prueba USerGuardar: guardo admin2" 
        assert name == u.name
        
    def testUserGuardarVacio(self):
        from models import User
        from ctrl.mgrUser import MgrUser
        name =""
        u=User()
        MgrUser().guardar(u)
        print "Error: Fin de prueba UserGuardarVacio" 
        assert name == u.name
        
    def testUSerGuardarDoble(self):
        from models import User
        from ctrl.mgrUser import MgrUser
        name = "admin2"
        u =User("admin2","admin2","administrador","administrador","admin@gmail.com",1234,"usuario administrador")
        MgrUser().guardar(u)
        print "Error: Fin de Prueba UserGuardarDoble: "
        assert name == u.name
    
        
    def testUserBorrarInexistente(self):
        from models import User
        from ctrl.mgrUser import MgrUser
        name = "feo"
        u =User("feo","feo","feo","feo","feo@gmail.com",1234,"usuario feo")
        MgrUser().borrar(u.name)
        print "Error: Fin de prueba USerBorrarInexistente: borro feo" 
        assert name == u.name
    


if __name__ == '__main__':
    unittest.main()

