# To change this template, choose Tools | Templates
# and open the template in the editor.

import unittest


class  TestItemCase(unittest.TestCase):
    #def setUp(self):
    #    self.foo = New_()
    #

    #def tearDown(self):
    #    self.foo.dispose()
    #    self.foo = None

    def testItemGuardar(self):
        from models import Item
        from ctrl.mgrItem import MgrItem
        nombre = "item1"
        u =Item("item1",1,10,100)
        MgrItem().guardar(u)
        print "Fin de prueba testItemGuardar: guardo item1" 
        assert nombre == u.nombre
        
    def testItemGuardarVacio(self):
        from models import Item
        from ctrl.mgrItem import MgrItem
        nombre =""
        u=Item()
        MgrItem().guardar(u)
        print "Error: Fin de prueba testItemGuardarVacio" 
        assert nombre == u.nombre
        
    def testItemGuardarDoble(self):
        from models import Item
        from ctrl.mgrItem import MgrItem
        nombre = "item1"
        u =Item("item1",1,10,100)
        MgrItem().guardar(u)
        print "Error: Fin de Prueba testItemGuardarDoble: "
        assert nombre == u.nombre
        
        
    def testItemBorrarInexistente(self):
        from models import Item
        from ctrl.mgrItem import MgrItem
        nombre = "item2"
        u =Item("item2",1,15,150)
        MgrItem().borrar(u.nombre)
        print "Error: Fin de prueba testItemBorrarInexistente: borro item2" 
        assert nombre == u.nombre
    


if __name__ == '__main__':
    unittest.main()

