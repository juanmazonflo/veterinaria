from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from config import config

#Modelos
from models.ModelUser import ModelUser

#Entidades
from models.entities.User import User

app = Flask(__name__)

csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)


            
@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db,id)

@app.route("/")
def index():
    return redirect(url_for('login'))

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = User(0,request.form['username'],request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash("Invalid Password")
                return render_template('auth/login.html')
        else:
            flash("User not found")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/protected")
@login_required
def protected():
    return "<h1>Vista protegida</h1>"

@app.route("/registro", methods=['POST', 'GET'])
def registro():
    if request.method == 'POST':

        usuario = request.form['username']
        nombre = request.form['nombre']
        email = request.form['email']
        user = User(0,request.form['username'],request.form['password'],request.form['nombre'],request.form['email'])
        check = ModelUser.checkuser(db,user)
        if check:
            check = ModelUser.checkemail(db,user)
            if check:
                cur = db.connection.cursor()
                contrasena = generate_password_hash(request.form['password'])
                cur.execute('INSERT INTO usuarios (username,password,nombre, email, tipo) VALUES (%s,%s,%s,%s,"cliente")',(usuario,contrasena,nombre,email))
                db.connection.commit()
                return redirect(url_for('login'))
            else:
                flash("Email in Use")
                return render_template('auth/registro.html')
        else:
            flash("Username in Use")
            return render_template('auth/registro.html')
    else:
        return render_template('auth/registro.html')

@app.route("/passwordrecovery", methods=['POST', 'GET'])
def passwordrecovery():
    if request.method == 'POST':
        newpassword = request.form['newpassword']
        confirmpassword = request.form['confirmpassword']
        user = User(0,None,None,None,request.form['email'])
        check = ModelUser.checkuser(db,user)
    
        if check:
            check=ModelUser.checknewpasswords(newpassword,confirmpassword)
            if check:
                cur = db.connection.cursor()
                newpassword = generate_password_hash(request.form['newpassword'])
                cur.execute('UPDATE usuarios SET password = %s WHERE email = %s',(newpassword,request.form['email']))
                db.connection.commit()
                return redirect(url_for('login'))
        return render_template('auth/passwordrecovery.html')
    else:
        return render_template('auth/passwordrecovery.html')

usermenu = {}

@app.route("/home")
@login_required
def home():
    menus = ModelUser.extraermenu(current_user.tipo)
    return render_template("home.html",usermenu = menus)

@app.route("/citas")
@login_required
def citas():
    menus = ModelUser.extraermenu(current_user.tipo)
    return render_template("citas.html",usermenu = menus)

@app.route("/mascotas")
@login_required
def mascotas():
    menus = ModelUser.extraermenu(current_user.tipo)
    mascotas = []
    mascotas = ModelUser.extraerlistamascotas(db)
    return render_template("mascotas.html",usermenu = menus,listamascotas = mascotas)

@app.route("/usuarios")
@login_required
def usuarios():
    menus = ModelUser.extraermenu(current_user.tipo)
    usuarios = []
    usuarios = ModelUser.extraerlistausuarios(db)
    return render_template("usuarios.html",usermenu = menus,listausuarios = usuarios)

@app.route("/servicios")
@login_required
def servicios():
    menus = ModelUser.extraermenu(current_user.tipo)
    servicios = []
    servicios = ModelUser.extraerlistaservicios(db)
    return render_template("servicios.html",usermenu = menus,listaservicios = servicios)

@app.route("/informes")
@login_required
def informes():
    menus = ModelUser.extraermenu(current_user.tipo)
    return render_template("informes.html",usermenu = menus)

@app.route("/historial")
@login_required
def historial():
    menus = ModelUser.extraermenu(current_user.tipo)
    return render_template("historial.html",usermenu = menus)

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return "<h1>La página solicitada no existe</h1>"

if __name__ == "__main__":
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401,status_401)
    app.register_error_handler(404,status_404)
    app.run(debug=True)