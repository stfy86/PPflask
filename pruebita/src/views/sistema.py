from modulo import *
from flask import Flask, render_template, request, redirect, url_for, g, \
     session, flash, escape, request
     
                           
#------------------------------------------------------------------------------#
# MODULO DE SISTEMA
#------------------------------------------------------------------------------#

@app.route('/administracion', methods=['GET','POST'])
def administracion():
    """ Modulo Administracion """
    return render_template(app.config['DEFAULT_TPL']+'/administracion.html',
			    conf = app.config,)

@app.route('/gestion', methods=['GET','POST'])
def gestion():
    """ Modulo Gestion """
    return render_template(app.config['DEFAULT_TPL']+'/gestion.html',
			    conf = app.config,)

@app.route('/desarrollo', methods=['GET','POST'])
def desarrollo():
    """ Modulo Desarrollo """
    return render_template(app.config['DEFAULT_TPL']+'/desarrollo.html',
			    conf = app.config,)

