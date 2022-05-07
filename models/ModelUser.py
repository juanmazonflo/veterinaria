from flask_login import current_user

from .entities.User import User
from .entities.Clases import *

class ModelUser():
    
    @classmethod
    def login(self,db,user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT idusuario, username, password FROM usuarios 
                    WHERE username = '{}'""".format(user.username)
            cursor.execute(sql)
            row=cursor.fetchone()
            if row != None:
                user=User(row[0],row[1],User.check_password(row[2],user.password))
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self,db,id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT idusuario, username, nombre, email, tipo FROM usuarios WHERE idusuario = {}".format(id)
            cursor.execute(sql)
            row=cursor.fetchone()
            if row != None:
                logged_user=User(row[0],row[1],None,row[2],row[3],row[4])
                return logged_user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def checkuser(self,db,user):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT idusuario, username FROM usuarios WHERE username = '{}'".format(user.username)
            cursor.execute(sql)
            row=cursor.fetchone()
            matchuser = False
            if row == None:
                matchuser = True
                return matchuser
            else:
                return matchuser
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def checkemail(self,db,user):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT idusuario, email FROM usuarios WHERE email = '{}'".format(user.email)
            cursor.execute(sql)
            row=cursor.fetchone()
            matchuser = False
            if row == None:
                matchuser = True
                return matchuser
            else:
                return matchuser
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def checknewpasswords(self,new,confirm):
        try:
            bandera = False
            if new == confirm:
                bandera = True
                return bandera
            else:
                return bandera
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def extraermenu(self,tipo):
        try:
            if tipo == "admin":
                usermenu = {"Home":"/home","Citas":"/citas","Mascotas":"/mascotas","Usuarios":"/usuarios","Servicios":"/servicios","Informes":"/informes","Recetas":"/recetas","Atencion":"/atencion","Medicinas":"/medicinas"}
            else:
                if tipo == "usuario":
                    usermenu = {"Home":"/home","Citas":"/citas","Mascotas":"/mascotas","Recetas":"/recetas","Atencion":"/atencion"}
                else:
                    if tipo == "cliente":
                        usermenu = {"Home":"/home","Citas":"/citas", "Mascotas":"/mascotas","Recetas":"/recetas","Atencion":"/atencion"}
            return usermenu
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def extraerlistausuarios(self,db):
        try:
            listausuarios = []
            cursor = db.connection.cursor()
            sql = "SELECT * FROM usuarios"
            cursor.execute(sql)
            row=cursor.fetchone()
            while row != None:
                    nuevouser=User(row[0],row[1],row[2],row[3],row[4],row[5])
                    listausuarios.append(nuevouser)
                    row=cursor.fetchone()
            return listausuarios
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def extraerUsuario(self,db,id):
        try:
            cur = db.connection.cursor()
            cur.execute('SELECT * FROM usuarios WHERE idusuario = %s', (id))
            data = cur.fetchall()
            cur.close()
            return data
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def actualizarUsuario(self,db,valores):
        try:
            cur = db.connection.cursor()
            cur.execute("UPDATE usuarios SET username=%s, password=%s, nombre=%s, email=%s, tipo=%s  WHERE idusuario = %s", (valores[0],valores[1],valores[2],valores[3],valores[4],valores[5]))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def eliminarUsuario(self,db,id):
        try:
            cur = db.connection.cursor()
            cur.execute('DELETE FROM usuarios WHERE idusuario = {0}'.format(id))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def extraerlistamascotas(self,db):
        try:
            listamascotas = []
            cursor = db.connection.cursor()
            sql = "SELECT m.idmascota, u.nombre, m.tipo, m.nombre FROM mascotas m INNER JOIN usuarios u ON m.idusuario = u.idusuario"
            cursor.execute(sql)
            row=cursor.fetchone()
            while row != None:
                    nuevamascota=Mascota(row[0],row[1],row[2],row[3])
                    listamascotas.append(nuevamascota)
                    row=cursor.fetchone()
            return listamascotas
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def agregarMascota(self,db,valores):
        try:
            cursor = db.connection.cursor()
            cursor.execute("INSERT INTO mascotas (idusuario, tipo, nombre) VALUES (%s,%s,%s)", (valores[0],valores[1],valores[2]))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def extraerMascota(self,db,id):
        try:
            cur = db.connection.cursor()
            cur.execute('SELECT * FROM mascotas WHERE idmascota = %s', (id))
            data = cur.fetchall()
            cur.close()
            return data
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def actualizarMascota(self,db,valores):
        try:
            cur = db.connection.cursor()
            cur.execute("UPDATE mascotas SET idusuario=%s, tipo=%s, nombre=%s  WHERE idmascota = %s", (valores[0], valores[1], valores[2],valores[3]))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def eliminarMascota(self,db,id):
        try:
            cur = db.connection.cursor()
            cur.execute('DELETE FROM mascotas WHERE idmascota = {0}'.format(id))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def extraerCitas(self,db):
        try:
            listacitas = []
            cursor = db.connection.cursor()
            sql = "SELECT c.idcita, m.nombre, s.servicio, fecha, hora FROM citas c INNER JOIN mascotas m ON m.idmascota = c.idmascota INNER JOIN servicios s ON s.idservicio = c.idservicio"
            cursor.execute(sql)
            row=cursor.fetchone()
            while row != None:
                    nuevacita=Citas(row[0],row[1],row[2],row[3],row[4])
                    listacitas.append(nuevacita)
                    row=cursor.fetchone()
            return listacitas
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def agregarCita(self,db,valores):
        try:
            cursor = db.connection.cursor()
            cursor.execute("INSERT INTO citas (idmascota,idservicio, fecha, hora) VALUES (%s,%s,%s,%s)", (valores[0],valores[1],valores[2],valores[3]))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def extraerCita(self,db,id):
        try:
            cur = db.connection.cursor()
            cur.execute('SELECT * FROM citas WHERE idcita = %s', (id))
            data = cur.fetchall()
            cur.close()
            return data
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def actualizarCita(self,db,valores):
        try:
            cur = db.connection.cursor()
            cur.execute("UPDATE citas SET idmascota=%s, idservicio=%s, fecha=%s, hora=%s  WHERE idcita = %s", (valores[0], valores[1], valores[2],valores[3],valores[4]))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def eliminarCita(self,db,id):
        try:
            cur = db.connection.cursor()
            cur.execute('DELETE FROM citas WHERE idcita= {0}'.format(id))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)


    @classmethod
    def extraerlistaservicios(self,db):
        try:
            listaservicios = []
            cursor = db.connection.cursor()
            sql = "SELECT * FROM servicios"
            cursor.execute(sql)
            row=cursor.fetchone()
            while row != None:
                    nuevoservicio=Servicio(row[0],row[1],row[2])
                    listaservicios.append(nuevoservicio)
                    row=cursor.fetchone()
            return listaservicios
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def agregarServicio(self,db,valores):
        try:
            cursor = db.connection.cursor()
            cursor.execute("INSERT INTO servicios (servicio,precio) VALUES (%s,%s)", (valores[0],valores[1]))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def extraerServicio(self,db,id):
        try:
            cur = db.connection.cursor()
            cur.execute('SELECT * FROM servicios WHERE idservicio = %s', (id))
            data = cur.fetchall()
            cur.close()
            return data
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def actualizarServicio(self,db,valores):
        try:
            cur = db.connection.cursor()
            cur.execute("UPDATE servicios SET servicio=%s, precio=%s  WHERE idservicio = %s", (valores[0], valores[1],valores[2]))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def eliminarServicio(self,db,id):
        try:
            cur = db.connection.cursor()
            cur.execute('DELETE FROM servicios WHERE idservicio= {0}'.format(id))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def extraerlistaMedicinas(self,db):
        try:
            listamedicinas = []
            cursor = db.connection.cursor()
            sql = "SELECT * FROM medicinas"
            cursor.execute(sql)
            row=cursor.fetchone()
            while row != None:
                    nuevomedicina=Medicinas(row[0],row[1],row[2],row[3],row[4])
                    listamedicinas.append(nuevomedicina)
                    row=cursor.fetchone()
            return listamedicinas
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def agregarMedicina(self,db,valores):
        try:
            cursor = db.connection.cursor()
            cursor.execute("INSERT INTO medicinas (descripcion,medida,presentacion,precio) VALUES (%s,%s,%s,%s)", (valores[0],valores[1],valores[2],valores[3]))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def extraerMedicina(self,db,id):
        try:
            cur = db.connection.cursor()
            cur.execute('SELECT * FROM medicinas WHERE idmedicina = %s', (id))
            data = cur.fetchall()
            cur.close()
            return data
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def actualizarMedicina(self,db,valores):
        try:
            cur = db.connection.cursor()
            cur.execute("UPDATE medicinas SET descripcion=%s,medida=%s,presentacion=%s, precio=%s  WHERE idmedicina = %s", (valores[0], valores[1],valores[2],valores[3],valores[4]))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def eliminarMedicina(self,db,id):
        try:
            cur = db.connection.cursor()
            cur.execute('DELETE FROM medicinas WHERE idmedicina= {0}'.format(id))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def extraerlistaRecetas(self,db):
        try:
            listarecetas = []
            cursor = db.connection.cursor()
            sql = "SELECT * FROM recetas"
            cursor.execute(sql)
            row=cursor.fetchone()
            while row != None:
                    nuevoreceta=Recetas(row[0],row[1],row[2],row[3])
                    listarecetas.append(nuevoreceta)
                    row=cursor.fetchone()
            return listarecetas
        except Exception as ex:
            raise Exception(ex)      
        
    @classmethod
    def agregarReceta(self,db,valores):
        try:
            cursor = db.connection.cursor()
            cursor.execute("INSERT INTO recetas (idmascota,fecha,descripcion) VALUES (%s,%s,%s)", (valores[0],valores[1],valores[2]))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def extraerReceta(self,db,id):
        try:
            cur = db.connection.cursor()
            cur.execute('SELECT * FROM recetas WHERE idreceta = %s', (id))
            data = cur.fetchall()
            cur.close()
            return data
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def actualizarReceta(self,db,valores):
        try:
            cur = db.connection.cursor()
            cur.execute("UPDATE recetas SET idmascota=%s,fecha=%s,descripcion=%s  WHERE idreceta = %s", (valores[0], valores[1],valores[2],valores[3]))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def eliminarReceta(self,db,id):
        try:
            cur = db.connection.cursor()
            cur.execute('DELETE FROM recetas WHERE idreceta= {0}'.format(id))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)
