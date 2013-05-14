# To change this template, choose Tools | Templates
# and open the template in the editor.

import unittest


class  TestFaseCase(unittest.TestCase):
    #def setUp(self):
    #    self.foo = New_()
    #

    #def tearDown(self):
    #    self.foo.dispose()
    #    self.foo = None

    def testFaseGuardar(self):
        from models import Fase
        from ctrl.mgrFase import MgrFase
        f=Fase("faseTest","rest",1)
        MgrFase().guardar(f)
        print "Fin de prueba FaseGuardar: guardo proyectoTest" 
        
    def testFaseGuardarVacio(self):
        from models import Fase
        from ctrl.mgrFase import MgrFase
        nombre =""
        p=Fase()
        MgrFase().guardar(p)
        print "Error: Fin de prueba FaseGuardarVacio" 
        assert nombre == f.nombre

        
    def testFaseGuardarDoble(self):
        from models import Fase
        from ctrl.mgrFase import MgrFase
        nombre = "faseTest"
        f=Fase(nombre,"fase inicial",1)
        MgrFase().guardar(f)
        print "Error: Fin de Prueba FaseGuardarDoble: "
        assert nombre == f.nombre
        
        
    
            
    def testFaseBorrarInexistente(self):
        from models import Fase
        from ctrl.mgrFase import MgrFase
        nombre = "faseTest"
        f=Fase(nombre,"fase inicial",1)
        MgrFase().borrar(f.nombre)
        print "Error: Fin de prueba USerBorrarInexistente: borro feo" 
        assert nombre == f.nombre
        
    


if __name__ == '__main__':
    unittest.main()

