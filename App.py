#Integrantes:
    #Flores Tabanico Jorge Hiram 
    #Juarez Vizcarra Victor Manuel 
    #Mazon Flores Juan Manuel
#Fecha:
    #07 de Mayo del 2022

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
@app.route("/citas/<accion>",methods=['POST', 'GET'])
@app.route("/citas/<accion>/<id>",methods=['POST', 'GET'])
@login_required
def citas(accion='',id=''):
    menus = ModelUser.extraermenu(current_user.tipo)
    citas=[]
    citas = ModelUser.extraerCitas(db)
    if accion=='':
        return render_template("citas.html",usermenu = menus,listacitas=citas)
    if accion=='agregar':   
        cursor = db.connection.cursor() 
        cursor2 = db.connection.cursor() 
        cursor.execute('SELECT idmascota,nombre FROM mascotas')  
        cursor2.execute('SELECT idservicio,servicio FROM servicios')  
        mascota = cursor.fetchall() 
        servicio= cursor2.fetchall() 
        if request.method == 'GET':
            return render_template("citas_agregar.html",usermenu = menus,listacitas = citas,mascota=mascota,servicio=servicio)
        if request.method == 'POST':
            mascota= request.form['mascota']
            lista_mascota=mascota.split()
            mascota=lista_mascota[0]
            servicio = request.form['servicio']
            lista_servicio=servicio.split()
            servicio=lista_servicio[0]
            fecha = request.form['fecha']
            hora = request.form['hora']
            valores=[mascota,servicio,fecha,hora]
            ModelUser.agregarCita(db,valores)
            flash('Cita añadida satisfactoriamente')
            return render_template("citas_agregar.html",usermenu = menus,listacitas = citas,mascota=mascota,servicio=servicio)
    if accion=='modificar':
        cursor = db.connection.cursor() 
        cursor2 = db.connection.cursor() 
        cursor.execute('SELECT idmascota,nombre FROM mascotas')  
        cursor2.execute('SELECT idservicio,servicio FROM servicios')  
        mascota = cursor.fetchall() 
        servicio= cursor2.fetchall() 
        if request.method == 'GET':
            data=ModelUser.extraerCita(db,id)
            return render_template('citas_modificar.html',usermenu = menus,listacitas = citas, cita = data[0],mascota=mascota,servicio=servicio)
        if request.method == 'POST':
            mascota= request.form['mascota']
            lista_mascota=mascota.split()
            mascota=lista_mascota[0]
            servicio = request.form['servicio']
            lista_servicio=servicio.split()
            servicio=lista_servicio[0]
            fecha = request.form['fecha']
            hora = request.form['hora']
            valores=[mascota,servicio,fecha,hora,id]
            ModelUser.actualizarCita(db,valores)
            data =  ModelUser.extraerCita(db,id)
            flash('Mascota modificada satisfactoriamente')
            return render_template("citas_modificar.html",usermenu = menus,listamascotas = citas, cita = data[0],mascota=mascota,servicio=servicio)
    if accion=='eliminar':
            ModelUser.eliminarCita(db,id)
            flash('Cita eliminada satisfactoriamente')
            return redirect("/citas")

@app.route("/mascotas")
@app.route("/mascotas/<accion>",methods=['POST', 'GET'])
@app.route("/mascotas/<accion>/<id>",methods=['POST', 'GET'])
@login_required
def mascotas(accion='',id=''):
    menus = ModelUser.extraermenu(current_user.tipo)
    mascotas = []
    mascotas = ModelUser.extraerlistamascotas(db)
    if accion=='':
        return render_template("mascotas.html",usermenu = menus,listamascotas = mascotas)
    if accion=='agregar':
        if request.method == 'GET':
            return render_template("mascotas_agregar.html",usermenu = menus,listamascotas = mascotas)
        if request.method == 'POST':
            idusuario = request.form['idusuario']
            tipo = request.form['tipo']
            nombre = request.form['nombre']
            valores=[idusuario,tipo,nombre]
            ModelUser.agregarMascota(db,valores)
            flash('Mascota añadida satisfactoriamente')
            return render_template("mascotas_agregar.html",usermenu = menus,listamascotas = mascotas)
    if accion=='modificar':
        if request.method == 'GET':
            data=ModelUser.extraerMascota(db,id)
            print(data[0])
            return render_template('mascotas_modificar.html',usermenu = menus,listamascotas = mascotas, mascota = data[0])
        if request.method == 'POST':
            idusuario = request.form['idusuario']
            tipo = request.form['tipo']
            nombre = request.form['nombre']
            valores=[idusuario,tipo,nombre,id]
            ModelUser.actualizarMascota(db,valores)
            data =  ModelUser.extraerMascota(db,id)
            flash('Mascota modificada satisfactoriamente')
            return render_template("mascotas_modificar.html",usermenu = menus,listamascotas = mascotas, mascota = data[0])
    if accion=='eliminar':
            ModelUser.eliminarMascota(db,id)
            flash('Mascota eliminada satisfactoriamente')
            return redirect("/mascotas")

@app.route("/usuarios")
@app.route("/usuarios/<accion>",methods=['POST', 'GET'])
@app.route("/usuarios/<accion>/<id>",methods=['POST', 'GET'])
@login_required
def usuarios(accion='',id=''):
    menus = ModelUser.extraermenu(current_user.tipo)
    usuarios = []
    usuarios = ModelUser.extraerlistausuarios(db)
    if accion=='':
        return render_template("usuarios.html",usermenu = menus,listausuarios = usuarios)
    if accion=='agregar':
        if request.method == 'GET':
            return redirect("/registro")
    if accion=='modificar':
        if request.method == 'GET':
            data=ModelUser.extraerUsuario(db,id)
            print(data[0])
            return render_template('usuarios_modificar.html',usermenu = menus,listausuarios = usuarios, usuario = data[0])
        if request.method == 'POST':
            username=request.form['username']
            password=request.form['password']
            newpassword=request.form['newpassword']
            confirmpassword=request.form['confirmpassword']
            nombre=request.form['nombre']
            email=request.form['email']
            tipo=request.form['tipo']
            user = User(0,username,password,nombre,email,tipo)
            check = ModelUser.checkuser(db,user)       
            if newpassword!='' and confirmpassword!='':                
                if check:
                    check=ModelUser.checknewpasswords(newpassword,confirmpassword)
                    if check:
                        password = generate_password_hash(request.form['newpassword'])
            valores=[username,password,nombre,email,tipo,id]
            ModelUser.actualizarUsuario(db,valores)
            data =  ModelUser.extraerUsuario(db,id)
            flash('Usuario modificada satisfactoriamente')
            return render_template("usuarios_modificar.html",usermenu = menus,listamascotas = usuarios, usuario= data[0])
    if accion=='eliminar':
            ModelUser.eliminarUsuario(db,id)
            flash('Usuario eliminado satisfactoriamente')
            return redirect("/usuarios")
    

@app.route("/servicios")
@app.route("/servicios/<accion>",methods=['POST', 'GET'])
@app.route("/servicios/<accion>/<id>",methods=['POST', 'GET'])
@login_required
def servicios(accion='',id=''):
    menus = ModelUser.extraermenu(current_user.tipo)
    servicios = []
    servicios = ModelUser.extraerlistaservicios(db)
    if accion=='':
        return render_template("servicios.html",usermenu = menus,listaservicios = servicios)
    if accion=='agregar':
        if request.method == 'GET':
            return render_template("servicios_agregar.html",usermenu = menus,listaservicios = servicios)
        if request.method == 'POST':
            servicio = request.form['servicio']
            precio = request.form['precio']
            valores=[servicio,precio]
            ModelUser.agregarServicio(db,valores)
            flash('Servicio añadido satisfactoriamente')
            return render_template("servicios_agregar.html",usermenu = menus,listaservicios = servicios)
    if accion=='modificar':
        if request.method == 'GET':
            data=ModelUser.extraerServicio(db,id)
            print(data[0])
            return render_template('servicios_modificar.html',usermenu = menus,listaservicio = servicios, servicio = data[0])
        if request.method == 'POST':
            servicio = request.form['servicio']
            precio = request.form['precio']
            valores=[servicio,precio,id]
            ModelUser.actualizarServicio(db,valores)
            data =  ModelUser.extraerServicio(db,id)
            flash('Servicio modificado satisfactoriamente')
            return render_template("servicios_modificar.html",usermenu = menus,listaservicio = servicios, servicio = data[0])
    if accion=='eliminar':
            ModelUser.eliminarServicio(db,id)
            flash('Servicio eliminado satisfactoriamente')
            return redirect("/servicios")

@app.route("/medicinas")
@app.route("/medicinas/<accion>",methods=['POST', 'GET'])
@app.route("/medicinas/<accion>/<id>",methods=['POST', 'GET'])
@login_required
def medicinas(accion='',id=''):
    menus = ModelUser.extraermenu(current_user.tipo)
    medicinas = []
    medicinas = ModelUser.extraerlistaMedicinas(db)
    if accion=='':
        return render_template("medicinas.html",usermenu = menus,listamedicinas = medicinas)
    if accion=='agregar':
        if request.method == 'GET':
            return render_template("medicinas_agregar.html",usermenu = menus,listamedicinas = medicinas)
        if request.method == 'POST':
            descripcion = request.form['descripcion']
            medida = request.form['medida']
            precio = request.form['precio']
            presentacion = request.form['presentacion']
            valores=[descripcion,medida,presentacion,precio]
            ModelUser.agregarMedicina(db,valores)
            flash('Medicina añadida satisfactoriamente')
            return render_template("mascotas_agregar.html",usermenu = menus,listamedicinas = medicinas)
    if accion=='modificar':
        if request.method == 'GET':
            data=ModelUser.extraerMedicina(db,id)
            print(data[0])
            return render_template('medicinas_modificar.html',usermenu = menus,listamedicinas = medicinas, medicina = data[0])
        if request.method == 'POST':
            descripcion = request.form['descripcion']
            precio = request.form['precio']
            medida = request.form['medida']
            presentacion = request.form['presentacion']
            valores=[descripcion,medida,presentacion,precio,id]   
            ModelUser.actualizarMedicina(db,valores)
            data =  ModelUser.extraerMedicina(db,id)
            flash('Medicina modificada satisfactoriamente')
            return render_template("medicinas_modificar.html",usermenu = menus,listamascotas = medicinas, medicina = data[0])
    if accion=='eliminar':
            ModelUser.eliminarMedicina(db,id)
            flash('Medicina eliminada satisfactoriamente')
            return redirect("/medicinas")

@app.route("/recetas")
@app.route("/recetas/<accion>",methods=['POST', 'GET'])
@app.route("/recetas/<accion>/<id>",methods=['POST', 'GET'])
@login_required
def recetas(accion='',id=''):
    menus = ModelUser.extraermenu(current_user.tipo)
    recetas = []
    recetas = ModelUser.extraerlistaRecetas(db)
    if accion=='':
        return render_template("recetas.html",usermenu = menus,listarecetas = recetas)
    if accion=='agregar':
        if request.method == 'GET':
            return render_template("recetas_agregar.html",usermenu = menus,listarecetas = recetas)
        if request.method == 'POST':
            idmascota =request.form['idmascota']
            fecha=request.form['fecha']
            descripcion=request.form['descripcion']
            valores=[idmascota,fecha,descripcion]
            ModelUser.agregarReceta(db,valores)
            flash('Receta añadida satisfactoriamente')
            return render_template("recetas_agregar.html",usermenu = menus,listarecetas = recetas)
    if accion=='modificar':
        if request.method == 'GET':
            data=ModelUser.extraerReceta(db,id)
            print(data[0])
            return render_template('recetas_modificar.html',usermenu = menus,listamedicinas = recetas, receta = data[0])
        if request.method == 'POST':
            idmascota =request.form['idmascota']
            fecha=request.form['fecha']
            descripcion=request.form['descripcion']
            valores=[idmascota,fecha,descripcion]
            valores=[idmascota,idmascota,fecha,descripcion]
            ModelUser.actualizarReceta(db,valores)
            data =  ModelUser.extraerReceta(db,id)
            flash('Receta modificada satisfactoriamente')
            return render_template("recetas_modificar.html",usermenu = menus,listamascotas = recetas, receta = data[0])
    if accion=='eliminar':
            ModelUser.eliminarReceta(db,id)
            flash('Receta eliminada satisfactoriamente')
            return redirect("/recetas")

@app.route("/atencion")
@login_required
def atencion():
    menus = ModelUser.extraermenu(current_user.tipo)
    return render_template("atencion.html",usermenu = menus)

@app.route("/informes")
@login_required
def informes():
    menus = ModelUser.extraermenu(current_user.tipo)
    return render_template("informes.html",usermenu = menus)

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