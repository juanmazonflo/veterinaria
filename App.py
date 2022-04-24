from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'veterinaria'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'veterinaria'
mysql = MySQL(app)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/registro")
def registro():
    return render_template('/registro.html')

@app.route("/addregistro" , methods=['POST'])
def addregistro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO usuarios (nombre, email, telefono, usuario, contraseña, tipo) VALUES (%s,%s,%s,%s,%s,"cliente")',(nombre,email,telefono,usuario,contrasena))
        mysql.connection.commit()

        return "Recibido"

@app.route("/login")
def login():
    return render_template('login.html')
    

@app.route("/loggedin", methods=['POST'])
def loggedin():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        cur = mysql.connection.cursor()
        cur.execute('')
        return "Recibido"


if __name__ == "__main__":
    app.run(debug=True)