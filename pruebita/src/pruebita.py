""" Main para cargar el sistema """
#------------------------------------------------------------------------------#
# IMPORTS
#------------------------------------------------------------------------------#
from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy
UPLOAD_FOLDER = '/home/silvana/Escritorio/PPflask/pruebita/src/uploads/'
#------------------------------------------------------------------------------#
# FLASK APP
#------------------------------------------------------------------------------#
# Flask application and config
app = Flask(__name__)
app.config.from_object('config')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

#------------------------------------------------------------------------------#
# MIDDLEWARE (to serve static files)
#------------------------------------------------------------------------------#
# Middleware to serve the static files
from werkzeug import SharedDataMiddleware
import os
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        '/': os.path.join(os.path.dirname(__file__), 'templates',
        app.config['DEFAULT_TPL'])
})
                                
#------------------------------------------------------------------------------#
# MAIN
#------------------------------------------------------------------------------#

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    from modulo import *
    from werkzeug.serving import run_simple
    run_simple('127.0.0.1', 8080, app, use_debugger=True, use_reloader=True)
