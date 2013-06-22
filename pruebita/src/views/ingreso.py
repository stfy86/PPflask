from modulo import *
from flask import Flask, render_template, request, redirect, url_for, g, \
     session, flash, escape, request

                           
#------------------------------------------------------------------------------#
# INGRESO SISTEMA
#------------------------------------------------------------------------------#

@app.before_request
def check_user_status():
    """ Checkea estatus """
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])


@app.route('/')
def index():
    """ Pagina Principal """
    return render_template(app.config['DEFAULT_TPL']+'/index.html',
			    conf = app.config,
			    users = User.query.order_by(User.name.desc()).all(),)
                            

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Logueo al sistema """
    if g.user is None:
        error = None
        if request.method=='POST':
            u = User.query.filter(User.name == request.form['username'], 
                                  User.passwd == request.form['password']).first()
            if u is None:
                error = 'Nick o Password incorrecto.'
            else:
                print u.idUser
                session['logged_in'] = True
                session['user_id'] = u.idUser
                session['user_name'] = u.name
                flash('Usted se ha conectado: ' + u.name)
                return redirect(url_for('index'))
            
        return render_template(app.config['DEFAULT_TPL']+'/login.html',
                               conf = app.config,
                               form = LoginForm(request.form),
                               error = error)
    else:
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    """ Logout del sistema """
    if g.user is not None:
        session.pop('logged_in', None)
        session.pop('user_id', None)
        session.pop('user_name', None)
        session["__invalidate__"] = True
        flash('Usted se ha desconectado:')
    return redirect(url_for('index')) 



