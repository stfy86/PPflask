"""
pruebita.wsgi
"""
activate_this = '/home/silvana/entorno/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
import sys
sys.path.insert(0, '/home/silvana/PPflask/pruebita/src')
from pruebita import app as application