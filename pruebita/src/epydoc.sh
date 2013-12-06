#!/bin/sh

#configurar los paths

epydoc *.py 
cd ctrl/
epydoc *.py 
cd ..
cd models/
epydoc *.py
cd ..
cd views/
epydoc *.py
cd ..
