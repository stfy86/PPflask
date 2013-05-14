# To change this template, choose Tools | Templates
# and open the template in the editor.

#------------------------------------------------------------------------------#
# IMPORTS
#------------------------------------------------------------------------------#
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, g, \
     session, flash
from werkzeug.routing import Rule
from flaskext.sqlalchemy import SQLAlchemy
from wtforms import Form, TextField, TextAreaField, FileField, PasswordField, \
     validators, IntegerField, SelectField, SubmitField

#------------------------------------------------------------------------------#
# FLASK APP
#------------------------------------------------------------------------------#
# Flask application and config
app = Flask(__name__)
app.config.from_object('config')
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
# MODELS
#------------------------------------------------------------------------------#


class User(db.Model):
    """ Modelo de Usuario """
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    passwd = db.Column(db.String(30))
    nombre = db.Column(db.String(50))
    apellido = db.Column(db.String(50))
    email = db.Column(db.String(50))
    telefono = db.Column(db.Integer)
    obs = db.Column(db.String(100))
    estado = db.Column(db.String(20), default ='Inactivo')

     

    def __init__(self, name=None, passwd=None):
        self.name = name
        self.passwd = passwd
    
    def __init__(self,name=None, passwd=None, nombre=None, apellido=None, email=None, telefono=None, obs=None):
        self.name = name
        self.passwd = passwd
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.obs = obs
    

#------------------------------------------------------------------------------#
# FORMS
#------------------------------------------------------------------------------#

class CreateFormUser(Form):
    """ Form used to create a new Usuario"""
    name = TextField('Name', [validators.required()])
    password = TextField('Password', [validators.required()])
    nombre = TextField('Nombre', [validators.required()])
    apellido = TextField('Apellido', [validators.required()])
    email = TextField('Email', [validators.required()])
    telefono = IntegerField('Telefono', [validators.required()])
    estado = db.Column(db.String(20), default ='inactivo')
    obs = TextField('Obs', [validators.required()])


class LoginForm(Form):
    """Form used to login into the system"""
    username = TextField('Nick', [validators.required()])
    password = PasswordField('Password', [validators.required()])


class EditStateForm(Form):
    estado = SelectField("Estado", choices = [
        ("Activo", "Activo"),
        ("Inactivo", "Inactivo")])
    submit = SubmitField("POST")
    
#------------------------------------------------------------------------------#
# CONTROLLERS
#------------------------------------------------------------------------------#

@app.before_request
def check_user_status():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])


@app.route('/')
def index():
        return render_template(app.config['DEFAULT_TPL']+'/index.html',
			    conf = app.config,
			    users = User.query.order_by(User.name.desc()).all(),)
                            

@app.route('/administracion', methods=['GET','POST'])
def administracion():
     return render_template(app.config['DEFAULT_TPL']+'/administracion.html',
			    conf = app.config,)



@app.route('/admin', methods=['GET','POST'])
def admin():
     return render_template(app.config['DEFAULT_TPL']+'/admin.html',
			    conf = app.config,)
                            

@app.route('/gestion', methods=['GET','POST'])
def gestion():
     return render_template(app.config['DEFAULT_TPL']+'/gestion.html',
			    conf = app.config,)

@app.route('/rolPermiso', methods=['GET','POST'])
def rolPermiso():
     return render_template(app.config['DEFAULT_TPL']+'/rolPermiso.html',
			    conf = app.config,)
                            


@app.route('/list', methods=['GET','POST'])
def list():
     return render_template(app.config['DEFAULT_TPL']+'/list.html',
                           conf = app.config,
                           list = User.query.all(),)                            



@app.route('/addUser', methods=['GET','POST'])
def addUser():
    if request.method == 'POST':
		user = User(name = request.form['name'], passwd = request.form['password'],
                nombre = request.form['nombre'], apellido = request.form['apellido'],
                email = request.form['email'], telefono = request.form['telefono'], 
                obs = request.form['obs'])    
		db.session.add(user)
		db.session.commit()
                
                flash('Se ha creado correctamente el usuario')
		return redirect(url_for('admin'))
    return render_template(app.config['DEFAULT_TPL']+'/formUser.html',
			       conf = app.config,
			       form = CreateFormUser())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is None:
        error = None
        if request.method=='POST':
            u = User.query.filter(User.name == request.form['username'], 
                                  User.passwd == request.form['password']).first()
            if u is None:
                error = 'Nick o Password incorrecto.'
            else:
                print u.id
                session['logged_in'] = True
                session['user_id'] = u.id
                session['user_name'] = u.name
                flash('Usted se ha conectado')
                return redirect(url_for('index'))
            
        return render_template(app.config['DEFAULT_TPL']+'/login.html',
                               conf = app.config,
                               form = LoginForm(request.form),
                               error = error)
    else:
        return redirect(url_for('index'))



@app.route('/deleteUser/<path:nombre>.html')
def deleteUser(nombre):
        user = User.query.filter(User.name == nombre).first_or_404()
        db.session.delete(user)
        db.session.commit()
        flash('Se ha borrado correctamente')
        return redirect(url_for('admin'))


@app.route('/listDelete')
def listDelete():
    if g.user is None:
        return redirect(url_for('login'))
    else:
        return render_template(app.config['DEFAULT_TPL']+'/delete.html',
                           conf = app.config,
                           list = User.query.all(),)  
    

@app.route('/listState')
def listState():
    if g.user is None:
        return redirect(url_for('login'))
    else:
        return render_template(app.config['DEFAULT_TPL']+'/listState.html',
                           conf = app.config,
                           list = User.query.all(),) 
                           

@app.route('/edit/<path:nombre>.html', methods=['GET','POST'])
def editState(nombre):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        user = User.query.filter(User.name == nombre).first_or_404()
        form = EditStateForm(request.form, estado = user.estado)
	if request.method == 'POST' and form.validate():
                user.estado = request.form['estado']
                db.session.commit()
		return redirect(url_for('admin'))
	return render_template(app.config['DEFAULT_TPL']+'/editState.html',
			       conf = app.config,
			       form = EditStateForm())

@app.route('/listEdit')
def listEdit():
    if g.user is None:
        return redirect(url_for('login'))
    else:
        return render_template(app.config['DEFAULT_TPL']+'/listEdit.html',
                           conf = app.config,
                           list = User.query.all(),) 

@app.route('/editUser/<path:nombre>.html', methods=['GET','POST'])
def editUser(nombre):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        user = User.query.filter(User.name == nombre).first_or_404()
        form = CreateFormUser(request.form, name = user.name, 
               password = user.passwd, nombre = user.nombre,
               apellido = user.apellido, email = user.email,
               telefono = user.telefono, obs = user.obs)
	if request.method == 'POST' and form.validate():
            user.name = request.form['name']
            user.passwd = request.form['password']
            user.nombre = request.form['nombre'] 
            user.apellido = request.form['apellido']
            user.email = request.form['email']
            user.telefono = request.form['telefono'] 
            user.obs = request.form['obs']
            db.session.commit()
            flash('Se ha modificado correctamente el usuario')
            return redirect(url_for('admin'))
	return render_template(app.config['DEFAULT_TPL']+'/editUser.html',
			       conf = app.config,
			       form = form)

@app.route('/logout')
def logout():
    if g.user is not None:
        session.pop('logged_in', None)
        session.pop('user_id', None)
        session.pop('user_name', None)
        flash('Usted se ha desconectado')
    return redirect(url_for('index'))

#------------------------------------------------------------------------------#
# MAIN
#------------------------------------------------------------------------------#
if __name__ == '__main__':
    app.run()


