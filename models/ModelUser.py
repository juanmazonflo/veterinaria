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
                usermenu = {"Home":"/home","Citas":"/citas","Mascotas":"/mascotas","Usuarios":"/usuarios","Servicios":"/servicios","Informes":"/informes","Historial":"/historial"}
            else:
                if tipo == "usuario":
                    usermenu = {"Home":"/home","Citas":"/citas","Mascotas":"/mascotas","Usuarios":"/usuarios","Servicios":"/servicios","Informes":"/informes","Historial":"/historial"}
                else:
                    if tipo == "cliente":
                        usermenu = {"Home":"/home","Citas":"/citas", "Mascotas":"/mascotas","Historial":"/historial","Historial":"/historial"}
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