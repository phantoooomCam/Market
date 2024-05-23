from flask import Flask, render_template,request,redirect,url_for,session,Response
import pyodbc
from config import SQL_SERVER_CONFIG
from flask_session import Session
from datetime import timedelta
from datetime import datetime
from functools import wraps

#Configuracion de cookies---------------------------------------------------------
app = Flask(__name__,template_folder='templates')
app.secret_key = 'secret_password'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_COOKIE_SECURE'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

#Configuracion de requerimiento de sesion-------------------------------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('iniciar_sesion'))
        return f(*args, **kwargs)
    return decorated_function

Session(app)

#----------------------------------------------------------------

#Cerrar sesion despues de tiempo---------------------------------------
@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)
    if 'user' in session:
        if 'last_activity' in session:
            if datetime.now() - session['last_activity'] > app.permanent_session_lifetime:
                session.pop('user', None)
        session['last_activity'] = datetime.now()
        
        
#Configuracion con la base de datos
conn_str = (
    f"DRIVER=ODBC Driver 17 for SQL Server;"
    f"SERVER={SQL_SERVER_CONFIG['server']};"
    f"DATABASE={SQL_SERVER_CONFIG['database']};"
    f"Trusted_Connection={SQL_SERVER_CONFIG['trusted_connection']};"
)
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

#-----------------------------------------------------------------
#Direcciones Paginas web
@app.route('/',methods=['GET','POST'])
def index():
    return render_template('Upii-Market Landing.html')

@app.route('/registrarse', methods=['GET', 'POST'])
def registrarse():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        telefono = request.form['telefono']
        matricula = request.form['matricula']
        carrera = request.form['carrera']
        email = request.form['email']
        password = request.form['password']
        estado = 0
        
        query="INSERT INTO Usuario (nombre, apellido, telefono, matricula, carrera, email, contrasena, estado) VALUES (?, ?, ?, ?, ?, ?, ?, 0)"
        cursor.execute(query, (nombre, apellidos, int(telefono), int(matricula), carrera, email, password))
        conn.commit()  
        
    return render_template('Registrarse.html')


@app.route('/principal',methods=['GET','POST'])
def principal():
    user = session.get('user')
    if user:
        return render_template('Upii-Market.html')
    else:
        return redirect(url_for('iniciar_sesion'))


@app.route('/iniciar_sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'] 
        
        query = "SELECT * FROM Usuario WHERE email = ? AND contrasena = ?"
        cursor.execute(query, (email, password))
        
        user = cursor.fetchone()

        if user:
            column_names = [column[0] for column in cursor.description]
            user_data = dict(zip(column_names, user))
            session['user'] = user_data
            return redirect(url_for('principal'))
        else:
            error = 'Correo electrónico o contraseña incorrectos. Por favor, inténtelo de nuevo.'
            return render_template('Iniciar Sesion.html', error=error)
    else:
        return render_template('Iniciar Sesion.html')


#Secciones Pagina Princial----------------------------------------------------\
@app.route('/comidas',methods=['GET','POST'])
@login_required
def comidas():
    return render_template('Comidas.html')

@app.route('/material',methods=['GET','POST'])
@login_required
def material():
    return render_template('Materiales.html')

@app.route('/snacks',methods=['GET','POST'])
@login_required
def snacks():
    return render_template('Snacks.html')

@app.route('/otros',methods=['GET','POST'])
@login_required
def otros():
    return render_template('Otros.html')
@app.route('/selling',methods=['GET','POST'])
@login_required
def selling():
    return render_template('Selling.html')
@app.route('/shopping',methods=['GET','POST'])
@login_required
def shopping():
    return render_template('Shopping.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1433,debug=True)