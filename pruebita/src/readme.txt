###################################
            iteracion 1
###################################
run1: manage.py initdb 
run2: manage.py createUser -u admin -p admin -n administrador -a administrador -e admin@gmail.com -t 1234 -o usuario
run3: pruebita.py runserver
  
###################################
            iteracion 2
###################################
run1: manage.py initdb 
run2: manage.py createAdministrador
run3: manage.py createRol
run4: manage.py createPermiso
run5: pruebita.py runserver

  
###################################
            iteracion 3
###################################

para la ejecutar 
# comentar en config.py la linea 21 y 23
run1: manage.py initdb 
run2: pruebita.py runserver

para la prueba 
# comentar en config.py la linea 20 y 24
run1: manage.py initdb 
run2: testX.py # donde X puede ser Atrib, Fase, Item, Proyecto o User

para la documentacion
run1: epydoc.sh
