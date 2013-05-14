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