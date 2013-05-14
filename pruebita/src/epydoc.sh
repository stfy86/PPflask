#!/bin/sh

#configurar los paths
DESDE= /home/silvana/PPflask/pruebita/src

cd $DESDE
epydoc $DESDE/manage.py
epydoc $DESDE/pruebita.py
epydoc $DESDE/form.py
epydoc $DESDE/models.py

mv $DESDE/html $DESDE/docs/
