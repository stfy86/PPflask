#!/bin/sh

#configurar los paths
DESDE= /home/silvana/Escritorio/ProyectoIS2/pruebita/src

cd $DESDE
epydoc $DESDE/manage.py
mv $DESDE/html $DESDE/docsManage/
epydoc $DESDE/pruebita.py
mv $DESDE/html $DESDE/docsPruebita/
epydoc $DESDE/form.py
mv $DESDE/html $DESDE/docsForm/
epydoc $DESDE/models.py
mv $DESDE/html $DESDE/docsModel/
