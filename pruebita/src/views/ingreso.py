from modulo import *
from flask import Flask, render_template, request, redirect, url_for, g, \
     session, flash, escape, request, Response

                        
#------------------------------------------------------------------------------#
# INGRESO SISTEMA
#------------------------------------------------------------------------------#

@app.before_request
def check_user_status():
    """ Checkea estatus """
    g.user = None
    g.proyecto = None
    g.permisos = []
    g.rol = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])
    if 'proyecto_id' in session:
        g.proyecto = Proyecto.query.get(session['proyecto_id'])
    if 'rol_id' in session:
        g.rol = Rol.query.get(session['rol_id'])
        g.permisos = MgrRol().listarNombrePermisos(session['rol_id'])
       
        

@app.route('/')
def index():
    """ Pagina Principal """
    g.proyecto = None
    g.rol = None
    g.permisos = []
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
                if u.name == "admin":
                    return redirect(url_for('administracion'))
                else:
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
        session.pop('proyecto_id', None)
        session.pop('proyecto_nombre', None)
        session.pop('rol_id', None)
        session["__invalidate__"] = True
        flash('Usted se ha desconectado:')
    return redirect(url_for('index')) 

@app.route('/misProyectos')
def misProyectos():   
    """ Lista los Proyectos del Usuario """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        g.proyecto = None
        g.rol = None
        g.permisos = []
        flash("Proyectos del usuario: " + g.user.name)
        return render_template(app.config['DEFAULT_TPL']+'/misProyectos.html',
                           conf = app.config,
                           list = MgrProyecto().ambitoDeUser(g.user)) 

@app.route('/misModulos/<path:idProyecto>.html', methods=['GET','POST'])
def misModulos(idProyecto):   
    if g.user is None:
        return redirect(url_for('login'))
    else:
        g.proyecto = MgrProyecto().filtrarXId(idProyecto)
        session['proyecto_id'] = g.proyecto.idProyecto
        session['proyecto_nombre'] = g.proyecto.nombre
        g.rol = MgrUser().rolDeUser(g.user, session['proyecto_nombre'])
        session['rol_id'] = g.rol.idRol
        g.permisos = MgrRol().listarNombrePermisos(g.rol.idRol)
        return render_template(app.config['DEFAULT_TPL']+'/misModulos.html',
                           conf = app.config
                           ) 
