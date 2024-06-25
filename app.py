from flask import Flask, render_template,request,redirect,url_for,session,Response, flash, make_response
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
from werkzeug.security import generate_password_hash, check_password_hash

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

# Configuración de correo electrónico
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Cambia esto por tu servidor SMTP
app.config['MAIL_PORT'] = 587  # Cambia esto según la configuración de tu servidor SMTP
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'upiimarket@gmail.com'  # Cambia esto por tu correo electrónico
app.config['MAIL_PASSWORD'] = 'uiaw ecpy bipq xeat'  # Cambia esto por tu contraseña
app.config['MAIL_DEFAULT_SENDER'] = 'upiimarket@gmail.com'

mail = Mail(app)

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    return no_cache

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
        cuenta = request.form['cuenta']
        email = request.form['email']
        password = request.form['password']
        estado = 0
        
        query="INSERT INTO Usuario (nombre, apellido, telefono, matricula, cuenta, email, contrasena, estado) VALUES (?, ?, ?, ?, ?, ?, ?, 0)"
        cursor.execute(query, (nombre, apellidos, int(telefono), int(matricula), cuenta, email, password))
        conn.commit()  
        
    return render_template('Registrarse.html')


@app.route('/principal',methods=['GET','POST'])
@nocache
def principal():
    user = session.get('user')
    if user:
        return render_template('Upii-Market.html')
    else:
        return redirect(url_for('iniciar_sesion'))


@app.route('/vendedor',methods=['GET','POST'])
@login_required
@nocache
def vendedor():
    user = session.get('user')
    if user:
        return render_template('Upii-Market Vendedor.html')
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
                'cuenta': user[5],
                'email': user[6],
                'estado': user[7]
            }
        if user[5] == 'Comprador':
            column_names = [column[0] for column in cursor.description]
            user_data = dict(zip(column_names, user))
            session['user'] = user_data
            return redirect(url_for('principal'))
        
        elif user[5] == 'Vendedor':
            column_names = [column[0] for column in cursor.description]
            user_data = dict(zip(column_names, user))
            session['user'] = user_data
            return redirect(url_for('vendedor'))
        else:
            error = 'Correo electrónico o contraseña incorrectos. Por favor, inténtelo de nuevo.'
            return render_template('Iniciar Sesion.html', error=error)
    else:
        return render_template('Iniciar Sesion.html')


#Secciones Pagina Princial----------------------------------------------------\
@app.route('/comidas',methods=['GET','POST'])
@login_required
@nocache
def comidas():
    query = "SELECT * FROM Producto WHERE clasificacion = 'Comida'"
    cursor.execute(query)
    productos = cursor.fetchall()
    return render_template('Comidas.html', productos=productos)

@app.route('/material',methods=['GET','POST'])
@login_required
@nocache
def material():
    query = "SELECT * FROM Producto WHERE clasificacion = 'Material'"
    cursor.execute(query)
    productos = cursor.fetchall()
    return render_template('Materiales.html', productos=productos)

@app.route('/snacks',methods=['GET','POST'])
@login_required
@nocache
def snacks():
    query = "SELECT * FROM Producto WHERE clasificacion = 'Dulces'"
    cursor.execute(query)
    productos = cursor.fetchall()
    return render_template('Snacks.html', productos=productos)

@app.route('/otros',methods=['GET','POST'])
@login_required
@nocache
def otros():
    query = "SELECT * FROM Producto WHERE clasificacion = 'Otros'"
    cursor.execute(query)
    productos = cursor.fetchall()
    return render_template('Otros.html', productos=productos)

@app.route('/selling',methods=['GET','POST'])
@login_required
@nocache
def selling():
    return render_template('Selling.html')
@app.route('/shopping',methods=['GET','POST'])
@login_required
@nocache
def shopping():
    return render_template('Shopping.html')

@app.route('/agregarproducto', methods=['GET','POST'])
@login_required
@nocache
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

#------------------Agregado por LALO
@app.route('/iniciarvendedor', methods=['GET','POST'])
@login_required
@nocache
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
@nocache
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
@nocache
@login_required
def cerrar_sesion():
    if 'user' in session:
        session.pop('user', None)
    response = make_response(render_template('Upii-Market Landing.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'  # HTTP 1.1
    response.headers['Pragma'] = 'no-cache'  # HTTP 1.0
    response.headers['Expires'] = '0'  # Proxies
    return response

#-------------Olvide contraseña
def send_reset_email(email, token):
    print("Recibido por send_reset_email")
    msg = Message('Restablecer Contraseña - Tu Aplicación', recipients=[email])
    msg.body = f'''Para restablecer tu contraseña ingresa el siguiente token:{token}
    
    Si no solicitaste restablecer tu contraseña, ignora este mensaje y tu contraseña permanecerá sin cambios.
    '''
    mail.send(msg)
    print("mensaje enviado")


@app.route('/olvidecontraseña', methods=['GET','POST'])
def olvide_contraseña():
    if request.method == 'POST':
        correo = request.form['email']
        
        # Verifica si el correo electrónico existe en tu base de datos
        try: 
            cursor.execute("SELECT * FROM Usuario WHERE email = ?", 
                           (correo))
            user = cursor.fetchone()
            
            print("Capture los datos")
            if user:
                id_user = user[0]
                print("Existe el usuario")
                # Generar un token temporal para restablecer la contraseña
                token = ''.join(random.choice(string.digits) for _ in range(5))
                print(token)
                print(type(token))
                cursor.execute("INSERT INTO Token (token, id_email) VALUES (?, ?)", (int(token), id_user))
                conn.commit()
                
                # Envía el correo electrónico con el enlace para restablecer la contraseña
                send_reset_email(email=correo, token=token)
                print("Se ha enviado a send_reset_email")
                flash('Se ha enviado un correo electrónico con instrucciones para restablecer la contraseña.', 'success')
                print("Se ha enviado a send_reset_email")
                return render_template('recuperar_contraseña.html', mostrar_token = True)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            error = 'Ha ocurrido un error con la base de datos'
            return render_template('Iniciar Sesion.html', error=error)

        return render_template('recuperar_contraseña.html')
    
    return render_template('recuperar_contraseña.html')

@app.route('/get_token', methods=['GET','POST'])
def get_token():
    if request.method == 'POST':
        Token = int(request.form['token'])

        # Verifica si el correo electrónico existe en tu base de datos
        try: 
            cursor.execute("SELECT * FROM Token WHERE token = ?", 
                           (Token))
            Token_data = cursor.fetchone()
            print("Existe el token")
            if Token_data:
                print("Se habilitará el cambiar contraseña")
                session['token'] = int(Token)

                return render_template('recuperar_contraseña.html', mostrar_form = True)
            else:
                return render_template('recuperar_contraseña.html')
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            error = 'Ha ocurrido un error con la base de datos'
            return render_template('Iniciar Sesion.html', error=error)

    return render_template('recuperar_contraseña.html')

@app.route('/reset_password/token', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        nueva = request.form['new_password']
        correo = request.form['correo']
        token_global = session.get('token')

        print(correo)
        print(nueva)
        print(token_global)
        try:
            cursor.execute("SELECT * FROM Usuario WHERE email = ?", 
                           (correo))
            user = cursor.fetchone()

            if user:
                cursor.execute("SELECT * FROM Token WHERE token = ?",
                                (token_global))
                token_data = cursor.fetchone()
                print(type(token_data))
                id_user = user[0]
                print(f"Existe el usuario {id_user}")
                if token_data:
                    print("Existe el token")
                    cursor.execute("UPDATE Usuario SET contrasena = ? WHERE id = ?",
                                    (nueva, int(id_user)))
                    conn.commit()
                    print("Se hizo el UPDATE")

                    cursor.execute("DELETE FROM Token WHERE token = ?", (int(token_global),))
                    conn.commit()
                    # Token válido, mostrar el formulario
                    flash('Contraseña restablecida correctamente. Inicia sesión con tu nueva contraseña.', 'success')
                        
                    return render_template('recuperar_contraseña.html', confirmacion=True)
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            error = 'Ha ocurrido un error con la base de datos'
            return render_template('Iniciar Sesion.html', error=error)

    return render_template('recuperar_contraseña.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1433,debug=True)