from flask import Flask, render_template,request,redirect,url_for,session,Response, flash
import pyodbc
import random
import string
from flask_mail import Mail, Message
from config import SQL_SERVER_CONFIG
from flask_session import Session
from datetime import timedelta
from datetime import datetime
from functools import wraps

import sqlite3

#Configuracion de imagenes
UPLOAD_FOLDER = 'path/to/upload/folder'  # Ruta donde se guardarán las imágenes
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Extensiones permitidas
def allowed_file(filename):
    """Función para verificar si el archivo tiene una extensión permitida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
            session['user']={
                'id':user[0],
                'nombre': user[1],
                'apellido': user[2],
                'telefono': user[3],
                'matricula': user[4],
                'carrera': user[5],
                'email': user[6],
                'estado': user[7]

            }
            return redirect(url_for('principal'))
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
    query = "SELECT * FROM Producto WHERE clasificacion = 'Comida'"
    cursor.execute(query)
    productos = cursor.fetchall()
    return render_template('Comidas.html', productos=productos)

@app.route('/material',methods=['GET','POST'])
@login_required
def material():
    query = "SELECT * FROM Producto WHERE clasificacion = 'Material'"
    cursor.execute(query)
    productos = cursor.fetchall()
    return render_template('Materiales.html', productos=productos)

@app.route('/snacks',methods=['GET','POST'])
@login_required
def snacks():
    query = "SELECT * FROM Producto WHERE clasificacion = 'Dulces'"
    cursor.execute(query)
    productos = cursor.fetchall()
    return render_template('Snacks.html', productos=productos)

@app.route('/otros',methods=['GET','POST'])
@login_required
def otros():
    query = "SELECT * FROM Producto WHERE clasificacion = 'Otros'"
    cursor.execute(query)
    productos = cursor.fetchall()
    return render_template('Otros.html', productos=productos)

@app.route('/selling',methods=['GET','POST'])
@login_required
def selling():
    return render_template('Selling.html')
@app.route('/shopping',methods=['GET','POST'])
@login_required
def shopping():
    return render_template('Shopping.html')

@app.route('/agregarproducto', methods=['GET','POST'])
@login_required
def aproducto():
    if request.method == 'POST':
        producto = request.form['producto']
        precio = request.form['precio']
        clasificacion = request.form['clasificacion']
        disponibilidad = request.form['disponibilidad']
        
        imagen_binaria= None
        user_id = session['user']['id']

        if 'imagenes' in request.files:
            archivo = request.files['imagenes']
            if archivo and allowed_file(archivo.filename):
                imagen_binaria = archivo.read()
                
        print("Producto:", producto)
        print("Precio:", float(precio))
        print("Clasificación:", clasificacion)
        print("Disponibilidad:", int(disponibilidad))
        print("Imagen binaria:", "Image uploaded" if imagen_binaria else "No image uploaded")

        
        query ="INSERT INTO Producto (nombre, clasificacion, precio, dispo, imagen, id_usuario) VALUES (?, ?, ?, ?, ?, ?)"

        cursor.execute(query,(producto,clasificacion,float(precio),int(disponibilidad),imagen_binaria, int(user_id)))
        conn.commit()
        
    return render_template('Agregar_producto.html')

@app.route('/vendedor',methods=['GET','POST'])
@login_required
def vendedor():
    return render_template('Upii-Market Vendedor.html')

#------------------Agregado por LALO
@app.route('/iniciarvendedor', methods=['GET','POST'])
@login_required
def login_vendedor():
    if request.method == 'POST':
        correo = request.form['email']
        contraseña = request.form['password']

        try:
            # Seleccionar usuario
            query = "SELECT * FROM Usuario WHERE email = ? AND contrasena = ? AND estado = 1"
            cursor.execute(query, (correo, contraseña))
            user = cursor.fetchone()

            if user:
                # Verificar que el usuario tenga el estado de vendedor (estado = 1)
                column_names = [column[0] for column in cursor.description]
                user_data = dict(zip(column_names, user))

                if user_data['estado'] == 1:
                    print("¡Cuenta tipo vendedor!")
                    session['user'] = user_data
                    return redirect(url_for('vendedor'))
                else:
                    error = 'Su cuenta aun no es tipo vendedor, por favor registrese'
                    return render_template('sing_up_vendedor.html', error=error)
            else:
                error = 'Correo o contraseña incorrectos'
                return render_template('sing_up_vendedor.html', error=error)

        except pyodbc.Error as e:
            print(f"Database error: {e}")
            error = 'Ha ocurrido un error con la base de datos'
            return render_template('sing_up_vendedor.html', error=error)
    else:
        return render_template('sing_up_vendedor.html')

@app.route('/cambiarvendedor', methods=['GET','POST'])
@login_required
def cambiar_vendedor():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        contraseña = request.form['contraseña']

        try:
            # Seleccionar usuario
            cursor.execute("SELECT * FROM Usuario WHERE nombre = ? AND email = ? AND contrasena = ? AND estado = 0", 
                           (nombre, correo, contraseña))
            user = cursor.fetchone()
            if user:
                # Actualizar estado del usuario
                cursor.execute("UPDATE Usuario SET estado = 1 WHERE nombre = ? AND email = ? AND contrasena = ?", 
                               (nombre, correo, contraseña))
                conn.commit()
                return redirect(url_for('login_vendedor'))
            else:
                error = 'Su cuenta no existe o ya es tipo vendedor'
                return render_template('sing_up_vendedor.html', error=error)

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            error = 'Ha ocurrido un error con la base de datos'
            return render_template('sing_up_vendedor.html', error=error)

    return render_template('sing_up_vendedor.html')

#-----------Cerrar sesion
@app.route('/cerrarsesion', methods=['POST'])
@login_required
def cerrar_sesion():
    if 'user' in session:
        session.pop('user', None)
        return render_template('Upii-Market Landing.html')

#-------------Olvide contraseña
def send_reset_email(email, token):
    msg = Message('Restablecer Contraseña - Tu Aplicación', recipients=[email])
    msg.body = f'''Para restablecer tu contraseña, visita el siguiente enlace:
    {url_for('reset_password', token=token, _external=True)}

    Si no solicitaste restablecer tu contraseña, ignora este mensaje y tu contraseña permanecerá sin cambios.
    '''
    email.send(msg)


@app.route('/olvidecontraseña', methods=['GET','POST'])
def olvide_contraseña():
    if request.method == 'POST':
        correo = request.form['email']
        
        # Verifica si el correo electrónico existe en tu base de datos
        try: 
            cursor.execute("SELECT * FROM Usuario WHERE nombre = ? AND email = ? AND contrasena = ? AND estado = 0", 
                           (correo))
            user = cursor.fetchone()
            
            # Aquí deberías agregar lógica para verificar y obtener el usuario por su correo electrónico
            # Por simplicidad, asumiré que obtienes el usuario de alguna manera
            
            # Generar un token temporal para restablecer la contraseña
            token = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))
            
            # Envía el correo electrónico con el enlace para restablecer la contraseña
            send_reset_email(correo, token)
            flash('Se ha enviado un correo electrónico con instrucciones para restablecer la contraseña.', 'success')
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            error = 'Ha ocurrido un error con la base de datos'
            return render_template('Iniciar Sesion.html', error=error)

        return redirect(url_for('login'))
    
    return render_template('recuperar_contraseña.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password():
    if 'reset_email' in session and 'reset_token' in session:
        correo = session['reset_email']
        token = session['reset_token']
        
        if request.method == 'POST':
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            
            if password == confirm_password:
                # Aquí deberías actualizar la contraseña en tu base de datos
                # Por simplicidad, imprimiré un mensaje de éxito
                print(f"Contraseña restablecida para {correo}: {password}")
                
                # Limpia las variables de sesión después de restablecer la contraseña
                session.pop('reset_email')
                session.pop('reset_token')
                
                flash('Contraseña restablecida con éxito. Inicia sesión con tu nueva contraseña.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Las contraseñas no coinciden.', 'error')
        
        return render_template('recuperar_contraseña.html', token=token)
    else:
        flash('No se ha solicitado un restablecimiento de contraseña válido.', 'error')
        return redirect(url_for('olvide_contraseña'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1433,debug=True)