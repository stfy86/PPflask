#!/bin/sh

#configurar los paths
DESDE = /home/silvana/Escritorio/PPflask/pruebita/src

cd $DESDE
epydoc manage.py form.py poblarBD.py
