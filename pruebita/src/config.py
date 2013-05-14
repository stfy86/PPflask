# To change this template, choose Tools | Templates
# and open the template in the editor.
import os
DEBUG = True

_basedir = os.path.abspath(os.path.dirname(__file__))

DATA_PATH = os.path.join(_basedir, 'data')
DEFAULT_TPL = 'static'

SECRET_KEY = 'secret devel key'

URL = 'http://localhost:5000/'
TITLE = 'Planificador de Proyecto'
VERSION = '0.1'
LANG = 'es'
LANG_DIRECTION = 'ltr'
YEAR = '2013'

SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.join(os.path.dirname(__file__), 'database.db')

del os


