# To change this template, choose Tools | Templates
# and open the template in the editor.

import unittest


class  TestProyectoCase(unittest.TestCase):
    #def setUp(self):
    #    self.foo = New_()
    #

    #def tearDown(self):
    #    self.foo.dispose()
    #    self.foo = None

    def testProyectoGuardar(self):
        from models import Proyecto
        from ctrl.mgrProject import MgrProject
        p=Proyecto("proyectoTest","test")
        MgrProject().guardar(p)
        print "Fin de prueba ProyectoGuardar: guardo proyectoTest" 
        
    def testProyectoGuardarVacio(self):
        from models import Proyecto
        from ctrl.mgrProject import MgrProject
        name =""
        p=Proyecto()
        MgrProject().guardar(p)
        print "Error: Fin de prueba ProjectGuardarVacio" 
        assert name == p.nombre

        
    def testProyectoGuardarDoble(self):
        from models import Proyecto
        from ctrl.mgrProject import MgrProject
        name="proyectoTest"
        p=Proyecto("proyectoTest","test")
        MgrProject().guardar(p)
        print "Error: Fin de Prueba ProjectGuardarDoble: "
        assert name == p.nombre
        
        
    
            
    def testProyectoBorrarInexistente(self):
        from models import Proyecto
        from ctrl.mgrProject import MgrProject
        name = "feo"
        p=Proyecto("proyectoTestfeo","test")
        MgrProject().borrar(p.nombre)
        print "Error: Fin de prueba USerBorrarInexistente: borro feo" 
        assert name == p.nombre
        
    


if __name__ == '__main__':
    unittest.main()

