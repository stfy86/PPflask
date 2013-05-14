# To change this template, choose Tools | Templates
# and open the template in the editor.

import unittest


class  TestAtribCase(unittest.TestCase):
    #def setUp(self):
    #    self.foo = New_()
    #

    #def tearDown(self):
    #    self.foo.dispose()
    #    self.foo = None

    def testAtribGuardar(self):
        from models import TipoDeAtributo
        from ctrl.mgrTipoDeAtrib import MgrTipoDeAtrib
        nombre = "atrib1"
        u =TipoDeAtributo("atrib1","numerico","30","atrib numerico precision 30")
        MgrTipoDeAtrib().guardar(u)
        print "Fin de prueba testAtribGuardar: guardo atrib1" 
        assert nombre == u.nombre
        
    def testTipoDeAtribGuardarVacio(self):
        from models import TipoDeAtributo
        from ctrl.mgrTipoDeAtrib import MgrTipoDeAtrib
        nombre =""
        u=TipoDeAtributo()
        MgrTipoDeAtrib().guardar(u)
        print "Error: Fin de prueba testTipoDeAtribGuardarVacio" 
        assert nombre == u.nombre
        
    def testTipoDeAtribGuardarDoble(self):
        from models import TipoDeAtributo
        from ctrl.mgrTipoDeAtrib import MgrTipoDeAtrib
        nombre = "atrib1"
        u =TipoDeAtributo("atrib1","numerico","30","atrib numerico precision 30")
        MgrTipoDeAtrib().guardar(u)
        print "Error: Fin de Prueba testTipoDeAtribGuardarDoble: "
        assert nombre == u.nombre
        
        
    def testTipoDeAtribBorrarInexistente(self):
        from models import TipoDeAtributo
        from ctrl.mgrTipoDeAtrib import MgrTipoDeAtrib
        nombre = "feo"
        u =TipoDeAtributo("feo","texto","30","atrib texto precision 30")
        MgrTipoDeAtrib().borrar(u.nombre)
      
        print "Error: Fin de prueba testTipoDeAtribBorrarInexistente: borro atrib2" 
        assert nombre == u.nombre
    


if __name__ == '__main__':
    unittest.main()

